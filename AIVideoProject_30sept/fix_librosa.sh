#!/bin/bash
echo "🔧 Fixing librosa compatibility..."
pip install librosa==0.8.1
echo "✅ Fixed! librosa version:" 
python3 -c "import librosa; print(librosa.__version__)"
