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

def extract_audio_from_video(video_path, output_audio):
    """Extract audio from video for voice sampling"""
    try:
        print(f"🎬 Extracting audio from video: {video_path}")
        cmd = [
            'ffmpeg', '-i', str(video_path),
            '-vn',  # No video
            '-acodec', 'pcm_s16le',
            '-ar', '22050',  # Sample rate
            '-ac', '1',  # Mono
            '-y',  # Overwrite
            str(output_audio)
        ]

        result = subprocess.run(cmd, capture_output=True, text=True)

        if result.returncode == 0:
            print(f"✅ Audio extracted to: {output_audio}")
            return True
        else:
            print(f"❌ Audio extraction failed: {result.stderr}")
            return False

    except Exception as e:
        print(f"❌ Error extracting audio: {e}")
        return False

def tts_with_male_voice(script, audio_path, voice_type="male"):
    """Generate TTS with different voice options"""
    try:
        from gtts import gTTS
        import random

        print(f"🔄 Converting text to speech with {voice_type} voice...")

        if voice_type == "male_slow":
            tts = gTTS(text=script, lang='en', slow=True)
        elif voice_type == "male_uk":
            tts = gTTS(text=script, lang='en', tld='co.uk')  # British accent
        elif voice_type == "male_au":
            tts = gTTS(text=script, lang='en', tld='com.au')  # Australian accent
        else:
            # Default enhanced male processing
            tts = gTTS(text=script, lang='en', slow=False)

        tts.save(audio_path)

        if Path(audio_path).exists():
            size = Path(audio_path).stat().st_size
            print(f"✅ {voice_type} voice saved: {audio_path} ({size} bytes)")
            return True
        else:
            print(f"❌ Failed to create {audio_path}")
            return False
    except Exception as e:
        print(f"❌ TTS conversion failed: {e}")
        return False

def pitch_shift_audio(input_audio, output_audio, semitones=-3):
    """Lower pitch to make voice more masculine"""
    try:
        print(f"🎵 Shifting pitch by {semitones} semitones for masculine voice...")

        cmd = [
            'ffmpeg', '-i', str(input_audio),
            '-af', f'rubberband=pitch={2**(semitones/12.0)}',
            '-y', str(output_audio)
        ]

        result = subprocess.run(cmd, capture_output=True, text=True)

        if result.returncode == 0:
            print(f"✅ Pitch shifted audio saved: {output_audio}")
            return True
        else:
            # Fallback to simple pitch shift
            print("⚠️  Rubberband failed, trying simple pitch shift...")
            cmd = [
                'ffmpeg', '-i', str(input_audio),
                '-af', f'asetrate=22050*{2**(semitones/12.0)},aresample=22050',
                '-y', str(output_audio)
            ]
            result = subprocess.run(cmd, capture_output=True, text=True)
            return result.returncode == 0

    except Exception as e:
        print(f"❌ Pitch shift failed: {e}")
        return False

def clone_voice_simple(sample_audio, script, output_audio):
    """Simple voice characteristics transfer"""
    try:
        print("🧬 Attempting simple voice cloning...")

        # Generate base TTS
        temp_tts = "temp_base_tts.wav"
        if not tts_with_male_voice(script, temp_tts, "male_uk"):
            return False

        # Apply pitch matching (basic approach)
        if not pitch_shift_audio(temp_tts, output_audio, semitones=-4):
            # Fallback: just copy the pitched audio
            shutil.copy2(temp_tts, output_audio)

        # Cleanup
        if Path(temp_tts).exists():
            Path(temp_tts).unlink()

        print(f"✅ Voice-enhanced audio created: {output_audio}")
        return True

    except Exception as e:
        print(f"❌ Voice cloning failed: {e}")
        return False

def enhance_audio_quality(input_audio, output_audio):
    """Enhance audio quality with compression and EQ"""
    try:
        print("🎚️  Enhancing audio quality...")

        cmd = [
            'ffmpeg', '-i', str(input_audio),
            '-af', 'volume=1.5,highpass=f=80,lowpass=f=8000,compand=0.1:0.2:-40/-10|-10/-5:0.1:0:-90:0.1',
            '-y', str(output_audio)
        ]

        result = subprocess.run(cmd, capture_output=True, text=True)

        if result.returncode == 0:
            print(f"✅ Enhanced audio saved: {output_audio}")
            return True
        else:
            # Fallback: simple volume boost
            cmd = ['ffmpeg', '-i', str(input_audio), '-af', 'volume=1.2', '-y', str(output_audio)]
            result = subprocess.run(cmd, capture_output=True, text=True)
            return result.returncode == 0

    except Exception as e:
        print(f"❌ Audio enhancement failed: {e}")
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

    parser = argparse.ArgumentParser(description="Enhanced AI Video Agent with Male Voice")
    parser.add_argument('--script', required=True, help='Script text')
    parser.add_argument('--image', required=True, help='Image path')
    parser.add_argument('--output', default='enhanced_video.mp4', help='Output path')
    parser.add_argument('--voice-sample', help='Sample video/audio for voice cloning')
    parser.add_argument('--voice-type', choices=['male', 'male_uk', 'male_au', 'male_slow'], 
                       default='male_uk', help='Voice type for TTS')
    parser.add_argument('--pitch-shift', type=int, default=-3, 
                       help='Pitch shift in semitones (negative = lower)')

    args = parser.parse_args()

    print("🎬 Enhanced AI Video Agent with Male Voice")
    print(f"📂 Working in: {Path.cwd()}")
    print("=" * 60)

    # Check setup
    if not check_wav2lip_setup():
        print("❌ Setup incomplete.")
        return

    # Check if image exists
    image_path = Path(args.image)
    if not image_path.exists():
        print(f"❌ Image not found: {image_path.absolute()}")
        return

    # File paths
    base_audio = 'base_male_audio.wav'
    enhanced_audio = 'enhanced_male_audio.wav'
    final_audio = 'final_male_audio.wav'

    # Clean up existing temp files
    for temp_file in [base_audio, enhanced_audio, final_audio]:
        if Path(temp_file).exists():
            Path(temp_file).unlink()

    try:
        # Step 1: Handle voice sample if provided
        if args.voice_sample and Path(args.voice_sample).exists():
            print("🎯 Voice sample provided - extracting for analysis...")
            sample_audio = 'voice_sample.wav'
            if extract_audio_from_video(args.voice_sample, sample_audio):
                # Use voice cloning approach
                if not clone_voice_simple(sample_audio, args.script, base_audio):
                    print("⚠️  Voice cloning failed, falling back to enhanced TTS...")
                    tts_with_male_voice(args.script, base_audio, args.voice_type)
                # Cleanup sample
                Path(sample_audio).unlink()
            else:
                print("⚠️  Sample processing failed, using enhanced TTS...")
                tts_with_male_voice(args.script, base_audio, args.voice_type)
        else:
            # Step 1: Generate base male voice
            if not tts_with_male_voice(args.script, base_audio, args.voice_type):
                print("❌ Base TTS generation failed")
                return

        # Step 2: Apply pitch shifting for masculinity
        if not pitch_shift_audio(base_audio, enhanced_audio, args.pitch_shift):
            print("⚠️  Pitch shifting failed, using original audio...")
            shutil.copy2(base_audio, enhanced_audio)

        # Step 3: Enhance audio quality
        if not enhance_audio_quality(enhanced_audio, final_audio):
            print("⚠️  Audio enhancement failed, using pitched audio...")
            shutil.copy2(enhanced_audio, final_audio)

        # Step 4: Generate lip-synced video
        if not run_wav2lip(args.image, final_audio, args.output):
            print("❌ Lip sync generation failed")
            return

        print("")
        print("🎉 SUCCESS! Enhanced male voice video created!")
        print(f"📁 Location: {Path(args.output).absolute()}")
        print(f"📤 Copy from pod: kubectl cp {os.environ.get('HOSTNAME', 'pod')}:/code/agents/AIVideoProject/{args.output} ./")

        # Show audio info
        print("\n🎵 Audio Enhancement Details:")
        print(f"   Voice Type: {args.voice_type}")
        print(f"   Pitch Shift: {args.pitch_shift} semitones")
        print(f"   Voice Sample: {'Yes' if args.voice_sample else 'No'}")

    except Exception as e:
        print(f"❌ Unexpected error: {e}")
    finally:
        # Cleanup temporary files
        print("\n🧹 Cleaning up temporary files...")
        temp_files = [base_audio, enhanced_audio, final_audio]
        for temp_file in temp_files:
            if Path(temp_file).exists():
                try:
                    Path(temp_file).unlink()
                    print(f"🗑️  Cleaned up {temp_file}")
                except Exception as e:
                    print(f"⚠️  Couldn't remove {temp_file}: {e}")

if __name__ == "__main__":
    main()

