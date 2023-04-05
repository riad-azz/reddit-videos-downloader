#!/bin/bash

# Update package list and install dependencies
apt-get update && apt-get install -y \
    wget \
    tar \
    xz-utils

# Download and extract FFmpeg binaries
wget https://johnvansickle.com/ffmpeg/releases/ffmpeg-release-amd64-static.tar.xz
tar xf ffmpeg-release-amd64-static.tar.xz

# Move the extracted binaries to /usr/local/bin/
mv ffmpeg-*-static/ffmpeg /usr/local/bin/
mv ffmpeg-*-static/ffprobe /usr/local/bin/

# Clean up downloaded files and temporary files
rm -rf ffmpeg-*-static*
apt-get remove -y wget tar xz-utils
apt-get autoremove -y
