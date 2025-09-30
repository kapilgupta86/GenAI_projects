#!/usr/bin/env bash
set -e

echo "Normalizing existing segment_*.wav to true PCM WAV and concatenating..."

# Normalize segments to mono 24k PCM16
for f in segment_*.wav; do
  [ -f "$f" ] || continue
  out="wav_$f"
  ffmpeg -y -i "$f" -ac 1 -ar 24000 -c:a pcm_s16le "$out"
done

# 0.5s silence clip (optional)
ffmpeg -y -f lavfi -t 0.5 -i anullsrc=r=24000:cl=mono -c:a pcm_s16le silence.wav

# Build concat list with pauses
rm -f audio_list.txt
for f in $(ls -1 wav_segment_*.wav); do
  echo "file '$f'" >> audio_list.txt
  last=$(ls -1 wav_segment_*.wav | tail -1)
  if [ "$f" != "$last" ]; then echo "file 'silence.wav'" >> audio_list.txt; fi
done

# Concatenate
ffmpeg -y -f concat -safe 0 -i audio_list.txt -c:a pcm_s16le base_audio.wav

echo "Done -> base_audio.wav"

