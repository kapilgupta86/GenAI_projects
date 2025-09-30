import os
import subprocess
import sys
from pathlib import Path
import shutil

def check_wav2lip_setup():
    """Check if Wav2Lip is properly set up"""
    required_files = [
        "Wav2Lip/inference.py",
        "Wav2Lip/checkpoints/wav2lip_gan.pth", 
        "Wav2Lip/face_detection/detection/sfd/s3fd.pth"
    ]

    print("🔍 Checking Wav2Lip setup...")
    missing_files = []
    for file_path in required_files:
        if Path(file_path).exists():
            size = Path(file_path).stat().st_size / (1024*1024)  # MB
            print(f"✅ {file_path} ({size:.1f}MB)")
        else:
            print(f"❌ Missing: {file_path}")
            missing_files.append(file_path)

    return len(missing_files) == 0

def tts_from_script(script, audio_path):
    """Convert text to speech using gTTS"""
    try:
        from gtts import gTTS
        print(f"🔄 Converting text to speech: '{script[:50]}...'")
        tts = gTTS(text=script, lang='en', slow=False)
        tts.save(audio_path)

        # Verify the file was actually created
        if Path(audio_path).exists():
            size = Path(audio_path).stat().st_size
            print(f"✅ Audio saved to {audio_path} ({size} bytes)")
            return True
        else:
            print(f"❌ Failed to create {audio_path}")
            return False
    except Exception as e:
        print(f"❌ TTS conversion failed: {e}")
        return False

def enhance_audio(input_audio, output_audio):
    """Enhance audio quality with fallback"""
    try:
        import librosa
        import noisereduce as nr
        import soundfile as sf

        print("🔄 Enhancing audio quality...")

        # Check if input file exists
        if not Path(input_audio).exists():
            print(f"❌ Input audio file not found: {input_audio}")
            return False

        print(f"📂 Loading audio from: {Path(input_audio).absolute()}")

        # Load audio with error handling
        try:
            audio, sr = librosa.load(input_audio, sr=None)
            print(f"✅ Audio loaded: {len(audio)} samples at {sr}Hz")
        except Exception as e:
            print(f"❌ Failed to load audio with librosa: {e}")
            # Fallback: just copy the file
            print("🔄 Using fallback: copying original audio...")
            shutil.copy2(input_audio, output_audio)
            if Path(output_audio).exists():
                print(f"✅ Audio copied to {output_audio}")
                return True
            else:
                print(f"❌ Failed to copy audio")
                return False

        # Try noise reduction
        try:
            reduced_noise = nr.reduce_noise(y=audio, sr=sr)
            print("✅ Noise reduction applied")
        except Exception as e:
            print(f"⚠️  Noise reduction failed: {e}")
            print("🔄 Using original audio without enhancement...")
            reduced_noise = audio

        # Save enhanced audio
        try:
            output_path = Path(output_audio).absolute()
            print(f"💾 Saving enhanced audio to: {output_path}")
            sf.write(str(output_path), reduced_noise, sr)

            # Verify the file was created
            if output_path.exists():
                size = output_path.stat().st_size
                print(f"✅ Enhanced audio saved: {output_path} ({size} bytes)")
                return True
            else:
                print(f"❌ Enhanced audio file not created")
                return False

        except Exception as e:
            print(f"❌ Failed to save enhanced audio: {e}")
            # Final fallback: copy original
            print("🔄 Final fallback: copying original audio...")
            shutil.copy2(input_audio, output_audio)
            return Path(output_audio).exists()

    except Exception as e:
        print(f"❌ Audio enhancement completely failed: {e}")
        # Ultimate fallback: copy the original file
        print("🔄 Ultimate fallback: copying original audio file...")
        try:
            shutil.copy2(input_audio, output_audio)
            return Path(output_audio).exists()
        except Exception as copy_error:
            print(f"❌ Even file copy failed: {copy_error}")
            return False

def run_wav2lip(image_path, audio_path, output_path):
    """Run Wav2Lip inference with better error reporting"""
    try:
        # Verify inputs exist
        abs_image_path = Path(image_path).absolute()
        abs_audio_path = Path(audio_path).absolute()
        abs_output_path = Path(output_path).absolute()

        if not abs_image_path.exists():
            print(f"❌ Image file not found: {abs_image_path}")
            return False

        if not abs_audio_path.exists():
            print(f"❌ Audio file not found: {abs_audio_path}")
            return False

        print(f"🔄 Running Wav2Lip lip sync...")
        print(f"📸 Image: {abs_image_path}")
        print(f"🔊 Audio: {abs_audio_path}")
        print(f"🎬 Output: {abs_output_path}")

        cmd = [
            'python3', 'inference.py',
            '--checkpoint_path', 'checkpoints/wav2lip_gan.pth',
            '--face', str(abs_image_path),
            '--audio', str(abs_audio_path),
            '--outfile', str(abs_output_path),
            '--pads', '0', '10', '0', '0'
        ]

        print(f"🚀 Command: {' '.join(cmd)}")
        print(f"📂 Working directory: {Path('Wav2Lip').absolute()}")

        result = subprocess.run(cmd, cwd='Wav2Lip', capture_output=True, text=True)

        print(f"📊 Return code: {result.returncode}")

        if result.stdout:
            print("📄 STDOUT:")
            print(result.stdout)

        if result.stderr:
            print("📄 STDERR:")
            print(result.stderr)

        if result.returncode == 0:
            # Verify output file exists
            if abs_output_path.exists():
                size = abs_output_path.stat().st_size / (1024*1024)  # MB
                print(f"✅ Video generated successfully: {abs_output_path} ({size:.1f}MB)")
                return True
            else:
                print(f"❌ Output file not created despite success code")
                return False
        else:
            print(f"❌ Wav2Lip failed with return code: {result.returncode}")
            return False

    except Exception as e:
        print(f"❌ Error running Wav2Lip: {e}")
        return False

def main():
    import argparse

    parser = argparse.ArgumentParser(description="AI Video Agent - Kubernetes Pod (Fixed)")
    parser.add_argument('--script', required=True, help='Script text')
    parser.add_argument('--image', required=True, help='Image path')
    parser.add_argument('--output', default='output_video.mp4', help='Output path')
    parser.add_argument('--check-only', action='store_true', help='Only check setup')
    parser.add_argument('--debug', action='store_true', help='Show debug info')

    args = parser.parse_args()

    print("🎬 AI Video Agent (Fixed Version)")
    print(f"📂 Working in: {Path.cwd()}")
    print("=" * 50)

    if args.debug:
        print("🔧 DEBUG INFO:")
        print(f"Python version: {sys.version}")
        print(f"Current directory: {Path.cwd()}")
        print(f"Directory contents: {list(Path.cwd().iterdir())}")
        print("=" * 50)

    # Check setup
    if not check_wav2lip_setup():
        print("❌ Setup incomplete. Download the missing model files first.")
        return

    if args.check_only:
        print("🎉 Setup is complete! Ready to generate videos.")
        return

    # Check if image exists
    image_path = Path(args.image)
    if not image_path.exists():
        print(f"❌ Image not found: {image_path.absolute()}")
        print("💡 Copy image to pod: kubectl cp your_photo.jpg pod-name:/code/agents/AIVideoProject/")
        return

    temp_audio = 'temp_audio.wav'
    enhanced_audio = 'enhanced_audio.wav'

    # Clean up any existing temp files
    for temp_file in [temp_audio, enhanced_audio]:
        if Path(temp_file).exists():
            Path(temp_file).unlink()
            print(f"🗑️  Removed existing {temp_file}")

    try:
        # Step 1: Text to Speech
        if not tts_from_script(args.script, temp_audio):
            print("❌ Text-to-speech failed")
            return

        # Step 2: Audio Enhancement (with fallback)
        if not enhance_audio(temp_audio, enhanced_audio):
            print("❌ Audio enhancement failed")
            return

        # Step 3: Lip Sync
        if not run_wav2lip(args.image, enhanced_audio, args.output):
            print("❌ Lip sync generation failed")
            return

        print("")
        print("🎉 SUCCESS! Video created in Kubernetes pod!")
        print(f"📁 Location: {Path(args.output).absolute()}")
        print(f"📤 Copy from pod: kubectl cp {os.environ.get('HOSTNAME', 'pod')}:/code/agents/AIVideoProject/{args.output} ./")

    except KeyboardInterrupt:
        print("\n⚠️  Process interrupted by user")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        if args.debug:
            import traceback
            traceback.print_exc()
    finally:
        # Cleanup temporary files
        print("\n🧹 Cleaning up temporary files...")
        for temp_file in [temp_audio, enhanced_audio]:
            if Path(temp_file).exists():
                try:
                    Path(temp_file).unlink()
                    print(f"🗑️  Cleaned up {temp_file}")
                except Exception as e:
                    print(f"⚠️  Couldn't remove {temp_file}: {e}")

if __name__ == "__main__":
    main()

