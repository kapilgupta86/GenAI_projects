#!/bin/bash
# Ubuntu 22.04 Setup Script for AI Video Agent in Kubernetes Pod
# Save as setup_ubuntu_k8s.sh and run: bash setup_ubuntu_k8s.sh

set -e  # Exit on any error

echo "🎬 Setting up AI Video Agent in Kubernetes Pod (Ubuntu 22.04)"
echo "============================================================="

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

print_status() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

print_info() {
    echo -e "${YELLOW}🔄 $1${NC}"
}

# Check available space
print_info "Checking available space..."
df -h /code
echo ""

# Step 1: Update package lists
print_info "Updating package lists..."
apt update

# Step 2: Install system dependencies
print_info "Installing system dependencies..."
apt install -y \
    python3 \
    python3-pip \
    python3-dev \
    python3-venv \
    git \
    wget \
    curl \
    ffmpeg \
    build-essential \
    cmake \
    pkg-config \
    libavcodec-dev \
    libavformat-dev \
    libswscale-dev \
    libv4l-dev \
    libxvidcore-dev \
    libx264-dev \
    libjpeg-dev \
    libpng-dev \
    libtiff-dev \
    libatlas-base-dev \
    gfortran \
    libhdf5-dev \
    libprotobuf-dev \
    libgoogle-glog-dev \
    libgflags-dev \
    libgphoto2-dev \
    libeigen3-dev \
    libhdf5-serial-dev \
    protobuf-compiler \
    liblapack-dev \
    libopenblas-dev \
    portaudio19-dev \
    python3-pyaudio

print_status "System dependencies installed"

# Step 3: Upgrade pip
print_info "Upgrading pip..."
python3 -m pip install --upgrade pip

# Step 4: Install Python packages
print_info "Installing Python packages (this may take a few minutes)..."

# Install PyTorch CPU version
python3 -m pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu

# Install other required packages
python3 -m pip install \
    opencv-python \
    opencv-contrib-python \
    librosa \
    noisereduce \
    gtts \
    soundfile \
    moviepy \
    requests \
    Pillow \
    numpy \
    scipy \
    matplotlib \
    imageio \
    imageio-ffmpeg \
    numba

print_status "Python packages installed"

# Step 5: Clone Wav2Lip repository
print_info "Downloading Wav2Lip..."
if [ ! -d "Wav2Lip" ]; then
    git clone https://github.com/Rudrabha/Wav2Lip.git
    print_status "Wav2Lip repository cloned"
else
    print_warning "Wav2Lip directory already exists"
fi

cd Wav2Lip

# Install Wav2Lip requirements
if [ -f "requirements.txt" ]; then
    print_info "Installing Wav2Lip requirements..."
    python3 -m pip install -r requirements.txt
    print_status "Wav2Lip requirements installed"
fi

# Step 6: Create model directories
print_info "Creating model directories..."
mkdir -p checkpoints
mkdir -p face_detection/detection/sfd

# Step 7: Download models with better error handling
print_info "Downloading AI models..."

# Download face detection model
if [ ! -f "face_detection/detection/sfd/s3fd.pth" ]; then
    print_info "Downloading face detection model (90MB)..."
    wget --timeout=30 --tries=3 \
         "https://www.adrianbulat.com/downloads/python-fan/s3fd-619a316812.pth" \
         -O "face_detection/detection/sfd/s3fd.pth" || {
        print_error "Failed to download face detection model"
        exit 1
    }
    print_status "Face detection model downloaded"
else
    print_warning "Face detection model already exists"
fi

# Download Wav2Lip model
if [ ! -f "checkpoints/wav2lip_gan.pth" ]; then
    print_info "Downloading Wav2Lip model (400MB - this will take a few minutes)..."
    wget --timeout=60 --tries=2 \
         "https://huggingface.co/Kedreamix/Linly-Talker/resolve/main/checkpoints/wav2lip_gan.pth" \
         -O "checkpoints/wav2lip_gan.pth" || {
        print_warning "Primary download failed, trying alternative..."
        curl -L --max-time 300 \
             "https://huggingface.co/Kedreamix/Linly-Talker/resolve/main/checkpoints/wav2lip_gan.pth" \
             -o "checkpoints/wav2lip_gan.pth" || {
            print_error "Failed to download Wav2Lip model from all sources"
            exit 1
        }
    }
    print_status "Wav2Lip model downloaded"
else
    print_warning "Wav2Lip model already exists"
fi

cd ..  # Back to /code

# Step 8: Verify installation
print_info "Verifying installation..."

# Check Python packages
python3 -c "
import sys
print(f'Python version: {sys.version}')

try:
    import torch
    print('✅ PyTorch:', torch.__version__)
except ImportError as e:
    print('❌ PyTorch failed:', e)
    sys.exit(1)

try:
    import cv2
    print('✅ OpenCV:', cv2.__version__)
except ImportError as e:
    print('❌ OpenCV failed:', e)
    sys.exit(1)

try:
    import librosa
    print('✅ Librosa:', librosa.__version__)
except ImportError as e:
    print('❌ Librosa failed:', e)
    sys.exit(1)

try:
    import noisereduce
    print('✅ noisereduce installed')
except ImportError as e:
    print('❌ noisereduce failed:', e)
    sys.exit(1)

try:
    from gtts import gTTS
    print('✅ gTTS installed')
except ImportError as e:
    print('❌ gTTS failed:', e)
    sys.exit(1)

try:
    import soundfile
    print('✅ soundfile installed')
except ImportError as e:
    print('❌ soundfile failed:', e)
    sys.exit(1)

print('\n🎉 All Python packages working correctly!')
" || {
    print_error "Python package verification failed"
    exit 1
}

# Check required files
declare -a required_files=(
    "Wav2Lip/inference.py"
    "Wav2Lip/checkpoints/wav2lip_gan.pth"
    "Wav2Lip/face_detection/detection/sfd/s3fd.pth"
)

all_good=true
echo ""
print_info "Checking required files..."
for file in "${required_files[@]}"; do
    if [ -f "$file" ]; then
        size=$(du -h "$file" | cut -f1)
        print_status "$file ($size)"
    else
        print_error "Missing: $file"
        all_good=false
    fi
done

if [ "$all_good" = true ]; then
    echo ""
    echo "🎉 SETUP COMPLETE IN KUBERNETES POD! 🎉"
    echo "======================================"
    echo ""
    echo "Your AI Video Agent is ready to use!"
    echo ""
    echo "Next steps:"
    echo "1. Add a photo to /code directory: your_photo.jpg"
    echo "2. Run: python3 ai_video_agent.py --script "Hello from Kubernetes!" --image your_photo.jpg"
    echo ""
    echo "Pod-specific notes:"
    echo "- All files are in /code directory"
    echo "- Models are downloaded and ready"
    echo "- Use 'kubectl cp' to transfer files to/from pod"
    echo ""
    echo "Example file transfer:"
    echo "kubectl cp local_photo.jpg pod-name:/code/photo.jpg"
    echo "kubectl cp pod-name:/code/output_video.mp4 ./output_video.mp4"
else
    print_error "Setup incomplete. Please check the missing files above."
    exit 1
fi

