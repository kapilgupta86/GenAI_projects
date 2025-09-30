import os
import subprocess
import sys
from pathlib import Path

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

def run_wav2lip(image_path, audio_path, output_path):
    """Run Wav2Lip inference"""
    try:
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

        result = subprocess.run(cmd, cwd='Wav2Lip', capture_output=True, text=True)

        if result.returncode == 0:
            if abs_output_path.exists():
                size = abs_output_path.stat().st_size / (1024*1024)  # MB
                print(f"✅ Video generated successfully: {abs_output_path} ({size:.1f}MB)")
                return True
            else:
                print(f"❌ Output file not created despite success code")
                return False
        else:
            print(f"❌ Wav2Lip failed with return code: {result.returncode}")
            if result.stdout:
                print("STDOUT:", result.stdout)
            if result.stderr:
                print("STDERR:", result.stderr)
            return False

    except Exception as e:
        print(f"❌ Error running Wav2Lip: {e}")
        return False

def main():
    import argparse

    parser = argparse.ArgumentParser(description="AI Video Agent - Simple Version")
    parser.add_argument('--script', required=True, help='Script text')
    parser.add_argument('--image', required=True, help='Image path')
    parser.add_argument('--output', default='output_video.mp4', help='Output path')

    args = parser.parse_args()

    print("🎬 AI Video Agent (Simple Version - No Audio Enhancement)")
    print(f"📂 Working in: {Path.cwd()}")
    print("=" * 60)

    # Check setup
    if not check_wav2lip_setup():
        print("❌ Setup incomplete. Download the missing model files first.")
        return

    # Check if image exists
    image_path = Path(args.image)
    if not image_path.exists():
        print(f"❌ Image not found: {image_path.absolute()}")
        return

    temp_audio = 'simple_audio.wav'

    # Clean up any existing temp files
    if Path(temp_audio).exists():
        Path(temp_audio).unlink()

    try:
        # Step 1: Text to Speech (no enhancement)
        if not tts_from_script(args.script, temp_audio):
            print("❌ Text-to-speech failed")
            return

        print("⚡ Skipping audio enhancement to avoid version conflicts")

        # Step 2: Lip Sync directly with TTS audio
        if not run_wav2lip(args.image, temp_audio, args.output):
            print("❌ Lip sync generation failed")
            return

        print("")
        print("🎉 SUCCESS! Video created in Kubernetes pod!")
        print(f"📁 Location: {Path(args.output).absolute()}")
        print(f"📤 Copy from pod: kubectl cp {os.environ.get('HOSTNAME', 'pod')}:/code/agents/AIVideoProject/{args.output} ./")

    except Exception as e:
        print(f"❌ Unexpected error: {e}")
    finally:
        # Cleanup
        if Path(temp_audio).exists():
            try:
                Path(temp_audio).unlink()
                print(f"🗑️  Cleaned up {temp_audio}")
            except:
                pass

if __name__ == "__main__":
    main()

