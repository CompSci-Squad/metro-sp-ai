#!/bin/bash

# Update package lists
echo "Updating package lists..."
sudo apt-get update

# Install OpenCV dependencies
echo "Installing OpenCV dependencies..."
sudo apt-get install -y \
    build-essential \
    cmake \
    git \
    pkg-config \
    libjpeg-dev \
    libtiff-dev \
    libpng-dev \
    libavcodec-dev \
    libavformat-dev \
    libswscale-dev \
    libv4l-dev \
    libgtk-3-dev \
    libatlas-base-dev \
    gfortran \
    python3-dev \
    libgl1-mesa-glx \
    libglib2.0-0 \
    libsm6 \
    libxrender1 \
    libxext6

# Clean up
echo "Cleaning up..."
sudo apt-get clean && sudo rm -rf /var/lib/apt/lists/*

echo "OpenCV dependencies installed successfully!"
