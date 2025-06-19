#!/usr/bin/env python3

import os
import subprocess
import sys
from pathlib import Path

VIDEO_EXTENSIONS = {'.mp4', '.avi', '.mov', '.mkv', '.wmv', '.flv', '.webm', '.m4v', '.3gp'}

def check_ffmpeg():
    try:
        subprocess.run(['ffmpeg', '-version'], capture_output=True, check=True)
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False

def convert_video_to_gif(input_path, output_path, fps=10, scale=1280):
    try:
        palette_path = input_path.with_suffix('.palette.png')
        print(f"Converting {input_path.name} to {output_path.name}...")
        palette_cmd = [
            'ffmpeg',
            '-i', str(input_path),
            '-vf', f'fps={fps},scale={scale}:-1:flags=lanczos,palettegen',
            '-y',
            str(palette_path)
        ]
        palette_result = subprocess.run(palette_cmd, capture_output=True, text=True)
        if palette_result.returncode != 0:
            print(f"✗ Failed to generate palette for {input_path.name}: {palette_result.stderr}")
            return False
        gif_cmd = [
            'ffmpeg',
            '-i', str(input_path),
            '-i', str(palette_path),
            '-lavfi', f'fps={fps},scale={scale}:-1:flags=lanczos[x];[x][1:v]paletteuse',
            '-y',
            str(output_path)
        ]
        gif_result = subprocess.run(gif_cmd, capture_output=True, text=True)
        if palette_path.exists():
            palette_path.unlink()
        if gif_result.returncode == 0:
            print(f"✓ Successfully converted {input_path.name}")
            return True
        else:
            print(f"✗ Failed to convert {input_path.name}: {gif_result.stderr}")
            return False
    except Exception as e:
        print(f"✗ Error converting {input_path.name}: {str(e)}")
        return False

def main():
    if not check_ffmpeg():
        print("Error: ffmpeg is not installed or not found in PATH")
        sys.exit(1)
    current_dir = Path.cwd()
    print(f"Processing videos in: {current_dir}")
    video_files = [f for f in current_dir.iterdir() if f.is_file() and f.suffix.lower() in VIDEO_EXTENSIONS]
    if not video_files:
        print("No video files found in the current directory.")
        return
    print(f"Found {len(video_files)} video file(s)")
    successful_conversions = 0
    failed_conversions = 0
    for video_file in video_files:
        gif_file = video_file.with_suffix('.gif')
        if gif_file.exists():
            print(f"⚠ Skipping {video_file.name} - {gif_file.name} already exists")
            continue
        if convert_video_to_gif(video_file, gif_file):
            successful_conversions += 1
        else:
            failed_conversions += 1
    print(f"\nConversion complete!")
    print(f"✓ Successful: {successful_conversions}")
    if failed_conversions > 0:
        print(f"✗ Failed: {failed_conversions}")

if __name__ == "__main__":
    main()
