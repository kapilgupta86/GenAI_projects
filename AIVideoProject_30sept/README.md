# AI Video Agent (AIVideoProject_30sept)

This folder contains a set of scripts that generate a lipsynced video from a single image and a text script by using the open-source Wav2Lip codebase together with TTS and command-line audio/video tools. The document below only states features and behavior that are present in the repository code (no speculation).

---

## Quick summary (what this code actually does)
- Converts text (inline script or text file) to speech using gTTS.
- Optionally processes and enhances the generated audio (two different approaches exist in different agent scripts).
- Calls Wav2Lip's `inference.py` (the repository is expected at `Wav2Lip/`) to produce a lip-synced video from a single image + audio.
- Provides multiple agent scripts for different use-cases:
  - `simple_ai_video_agent.py`  minimal flow: TTS -> Wav2Lip (no audio enhancement).
  - `ai_video_agent.py`  TTS -> audio enhancement using librosa + noisereduce (fallbacks included) -> Wav2Lip.
  - `enhanced_ai_video_agent.py`  TTS variants for "male" voices, pitch shifting (ffmpeg rubberband or asetrate fallback), ffmpeg-based audio enhancement, simple voice characteristics transfer fallbacks -> Wav2Lip.
  - `indian_ai_video_agent.py`  script-file based flow with language detection (Hindi / English / mixed), per-segment TTS, normalization and concatenation (mono 24k PCM),ffmpeg-based voice enhancement tuned in code, HD Wav2Lip invocation and optional upscaling to FHD.

There are helper shell scripts to prepare environment and to patch or normalize audio:
- `setup_ubuntu_k8s.sh`  an Ubuntu 22.04 setup script that installs OS packages, Python packages, clones Wav2Lip and downloads required model files (used to prepare a pod or host).
- `patch_wav2lip_audio.sh`  writes a patched `Wav2Lip/audio.py` (compat layers) and tests importing it.
- `fix_librosa.sh`  installs a specific librosa version (0.8.1) to address compatibility.
- `normalize_and_concat.sh`  normalizes segment WAV files to mono 24k PCM and concatenates them with optional pauses.

Sample inputs exist in the folder, e.g. `mixed_script.txt`, `hindi_script.txt`, `indian_english_script.txt`, and some example videos.

---

## Key features (from the implemented code)
- Text-to-speech using gTTS (the scripts import `gtts` and write mp3/wav).
- Multiple audio processing strategies:
  - librosa + noisereduce + soundfile (in `ai_video_agent.py`).
  - ffmpeg-based EQ/compand/volume processing and pitch shifting (in `enhanced_ai_video_agent.py` and `indian_ai_video_agent.py`).
- Simple voice characteristics transfer (rudimentary) in `enhanced_ai_video_agent.py` (creates base TTS then pitch-shifts).
- Language detection (Hindi/English/mixed) and per-sentence segmentation in `indian_ai_video_agent.py`.
- Concatenation of per-segment WAV files into a single normalized mono 24k WAV (ffmpeg concat demuxer) in the Indian agent code.
- Wav2Lip invocation via subprocess: the agents call `python3 inference.py` in the `Wav2Lip` directory and expect specific files:
  - `Wav2Lip/inference.py`
  - `Wav2Lip/checkpoints/wav2lip_gan.pth`
  - `Wav2Lip/face_detection/detection/sfd/s3fd.pth`
- Several defensive/fallback behaviors:
  - Audio enhancement fallbacks to copying original audio if processing fails.
  - Pitch-shift falls back from `rubberband` filter to `asetrate`+`aresample` if rubberband fails.
  - File existence checks and helpful console messages throughout.

---

## High-level design / pipeline (common pattern)
1. Input:
   - Inline script text (agents accept `--script`) or a script text file (Indian agent accepts `--script-file`).
   - Single face image (`--image`).
2. TTS:
   - Use gTTS to generate speech (mp3 or wav).
   - In the Indian agent, gTTS outputs mp3 and ffmpeg converts to mono PCM 24k WAV.
3. (Optional) Voice processing/enhancement:
   - Either Python audio processing (librosa + noisereduce) or ffmpeg audio filters (EQ/compand/volume).
   - Optional pitch shifting to create "male" voice tone.
   - Optional simple voice "cloning" attempt (rudimentary).
4. Lip-sync:
   - Run Wav2Lip inference (`inference.py`) as a subprocess inside `Wav2Lip/` with the generated audio and input image.
5. Output:
   - Video file (default names vary by script).
   - Temporary files are cleaned up at the end of each script's run.

Agent differences:
- Simple agent: skips audio enhancement.
- AI agent: uses librosa + noisereduce if available, with fallbacks.
- Enhanced agent: more options around male voice TTS and pitch.
- Indian agent: focuses on correct handling of Hindi / English / mixed scripts, segment-wise TTS and concatenation, and HD Wav2Lip invocation (includes flags such as `--resize_factor` and `--nosmooth` in its run).

---

## Low-level design (implementation details you can rely on)
- Wav2Lip checks:
  - Each agent has a `check_wav2lip_setup()` function that checks presence of:
    - `Wav2Lip/inference.py`
    - `Wav2Lip/checkpoints/wav2lip_gan.pth`
    - `Wav2Lip/face_detection/detection/sfd/s3fd.pth`
- Text-to-speech:
  - `gTTS` is used (imported as `from gtts import gTTS`).
  - Agents save TTS output to MP3 or WAV paths, then verify file creation.
- Audio enhancement (examples and function names found in code):
  - `ai_video_agent.py` contains `enhance_audio()` which tries:
    - `librosa.load(...)`
    - `noisereduce.reduce_noise(...)`
    - `soundfile` (`sf.write(...)`) to save enhanced audio
    - Falls back to copying input audio if processing fails.
  - `enhanced_ai_video_agent.py` contains:
    - `tts_with_male_voice(...)`
    - `pitch_shift_audio(...)`  uses ffmpeg with `rubberband` filter then fallback to `asetrate`+`aresample`.
    - `clone_voice_simple(...)`  basic pipeline: generate base TTS then pitch-shift and copy as fallback.
    - `enhance_audio_quality(...)`  ffmpeg audio filters chain (volume, highpass/lowpass, compand).
  - `indian_ai_video_agent.py` contains:
    - `generate_indian_male_tts(...)`  gTTS then ffmpeg convert to PCM s16le mono 24000 Hz.
    - `process_mixed_script_audio(...)`  generates segment WAVs per sentence.
    - `concatenate_audio_files(...)`  normalizes each file to mono 24k and uses ffmpeg concat demuxer; optionally inserts a 0.5s silence clip.
    - `enhance_indian_male_voice(...)`  ffmpeg filter chain tuned for the repo's "Indian male" preset.
- Wav2Lip invocation:
  - All agents use subprocess to run `python3 inference.py` inside `Wav2Lip` directory with arguments including:
    - `--checkpoint_path checkpoints/wav2lip_gan.pth`
    - `--face <image>`
    - `--audio <audio>`
    - `--outfile <output>`
    - `--pads` (padding values differ slightly across agents)
  - The Indian agent has `run_wav2lip_hd()` which adds flags such as `--resize_factor 1` and `--nosmooth`.
- FFmpeg/ffprobe usage:
  - For extraction, conversions, pitch shifting, enhancement, concatenation, normalization, and to probe durations.
  - Indian agent uses sample rate `24000` and mono (explicit).
- Temporary files:
  - Agents create temporary files (names differ). They attempt to remove them in `finally` blocks.
- Shell scripts:
  - `setup_ubuntu_k8s.sh` installs system packages, pip packages, clones Wav2Lip and downloads required model files with `wget`/`curl`. It also runs small Python checks for installed packages.
  - `patch_wav2lip_audio.sh` writes a patched `Wav2Lip/audio.py` and runs a quick import test.

---

## How to run (examples consistent with the code)
Important precondition: the Wav2Lip repository must be present at `Wav2Lip/` relative to where you run the agents and the required model files must be in the indicated paths.

Examples (run from this folder or adjust paths):

- Quick check (exists check only):
  - python3 ai_video_agent.py --script "Hello world" --image photo.jpg --check-only

- Simple agent (no enhancement):
  - python3 simple_ai_video_agent.py --script "Hello from Simple Agent" --image photo.jpg --output output_video.mp4

- AI agent (librosa + noisereduce enhancement):
  - python3 ai_video_agent.py --script "Hello from AI Agent" --image photo.jpg --output output_video.mp4
  - Use `--debug` to print diagnostics

- Enhanced (male voice + pitch shift):
  - python3 enhanced_ai_video_agent.py --script "Hello" --image photo.jpg --voice-type male_uk --pitch-shift -3 --output enhanced_video.mp4
  - To supply a voice sample for the basic cloning attempt: `--voice-sample sample_video.mp4`

- Indian agent (script file, mixed language support, HD/FHD):
  - python3 indian_ai_video_agent.py --script-file mixed_script.txt --image photo.jpg --output indian_hd_video.mp4 --quality hd --add-pauses

If you prefer to prepare an Ubuntu environment (or a Kubernetes pod based on Ubuntu 22.04), the repository includes `setup_ubuntu_k8s.sh`. Read that script before running  it installs packages and downloads the Wav2Lip repo and models.

---

## Limitations (explicitly present in the code)
- Wav2Lip dependency and models:
  - The agents require the external Wav2Lip codebase and big model files:
    - `Wav2Lip/checkpoints/wav2lip_gan.pth` (large download)
    - `Wav2Lip/face_detection/detection/sfd/s3fd.pth`
  - The code checks for these files and will not proceed if they are missing.
- gTTS requires network access (it uses Google's TTS service).
- Performance:
  - The scripts call Wav2Lip and ffmpeg as subprocesses; CPU-only execution is supported but will be slow. The included `setup_ubuntu_k8s.sh` demonstrates installing a CPU PyTorch wheel.
- Voice cloning:
  - The "voice cloning" in `enhanced_ai_video_agent.py` is a very simple heuristic (TTS + pitch shifts). It is not a neural voice cloning pipeline and will not produce high-fidelity clones.
- System/tooling assumptions:
  - Scripts assume a Unix-like environment with `ffmpeg`, `ffprobe`, `python3`, `wget`, `curl`, etc.
  - `pitch_shift_audio` may require the rubberband filter (`rubberband`)  the code falls back to `asetrate` if rubberband-based filter usage fails.
- Compatibility issues:
  - The repository contains helper scripts (`patch_wav2lip_audio.sh`, `fix_librosa.sh`) to handle known compatibility problems (e.g., newer numpy/librosa APIs). Those are present because the code may encounter compatibility issues in some environments.
- No production orchestration/UI:
  - The code is script-based; there is no web interface, API server, or production-grade orchestration implemented in the Python code itself. The `setup_ubuntu_k8s.sh` is an environment setup script  it does not itself deploy or manage Kubernetes objects.

---

## Technology selection (the actual stack used in code and scripts)
- Python 3 (agent scripts are Python 3 scripts).
- gTTS (Google Text-to-Speech) for TTS.
- Wav2Lip (external repository called via subprocess).
- FFmpeg / ffprobe (extensively used for audio/video conversion, pitch shifting, concatenation, extracting audio from sample videos).
- librosa, noisereduce, soundfile (used in `ai_video_agent.py` for audio processing).
- numpy, scipy (used inside audio processing or patched audio modules).
- PyTorch and OpenCV are referenced/verified in the `setup_ubuntu_k8s.sh` script (Wav2Lip uses PyTorch).
- Shell tools: wget, curl, git, bash (helper installation scripts rely on them).

---

## Files of interest in this folder
- Python agents:
  - ai_video_agent.py
  - simple_ai_video_agent.py
  - enhanced_ai_video_agent.py
  - indian_ai_video_agent.py
- Helper scripts:
  - setup_ubuntu_k8s.sh
  - patch_wav2lip_audio.sh
  - fix_librosa.sh
  - normalize_and_concat.sh
- Example inputs / assets:
  - mixed_script.txt
  - hindi_script.txt
  - indian_english_script.txt
  - sample mp4 files present for demos (k8s_video.mp4, male_voice_video.mp4, mixed_hindi_english_video.mp4)
  - photo.jpg, silence.wav
