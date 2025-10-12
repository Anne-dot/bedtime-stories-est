#!/usr/bin/env python3
"""
Trim excessive silence from the end of MP3 files
"""
import os
import subprocess
import shutil

SOURCE_FOLDER = "Õhtujutt"
BACKUP_FOLDER = "Õhtujutt_originaalid"
PROCESSED_FILE = "õhtujutt_processed_files.txt"
MAX_END_SILENCE = 3  # seconds

def detect_silence_at_end(filepath):
    """Detect silence at the end of audio file"""
    cmd = [
        'ffmpeg', '-i', filepath,
        '-af', 'silencedetect=n=-50dB:d=1',
        '-f', 'null', '-'
    ]

    result = subprocess.run(cmd, capture_output=True, text=True)

    # Parse last silence_end from stderr
    lines = result.stderr.split('\n')
    last_silence = None

    for line in lines:
        if 'silence_end:' in line:
            parts = line.split('silence_end:')[1].split('|')
            end_time = float(parts[0].strip())
            duration = float(parts[1].split(':')[1].strip())
            last_silence = {'end': end_time, 'duration': duration}

    return last_silence

def get_audio_duration(filepath):
    """Get total duration of audio file"""
    cmd = ['ffprobe', '-i', filepath, '-show_entries', 'format=duration', 
           '-v', 'quiet', '-of', 'csv=p=0']
    result = subprocess.run(cmd, capture_output=True, text=True)
    return float(result.stdout.strip())

def trim_file(input_path, output_path, duration):
    """Trim file to specified duration"""
    cmd = [
        'ffmpeg', '-i', input_path,
        '-t', str(duration),
        '-acodec', 'copy',
        '-y', output_path
    ]
    subprocess.run(cmd, capture_output=True)

def load_processed_files():
    """Load list of already processed files"""
    if os.path.exists(PROCESSED_FILE):
        with open(PROCESSED_FILE, 'r') as f:
            return set(line.strip() for line in f)
    return set()

def mark_as_processed(filename):
    """Mark a file as processed"""
    with open(PROCESSED_FILE, 'a') as f:
        f.write(filename + '\n')

def main():
    # Create backup folder
    os.makedirs(BACKUP_FOLDER, exist_ok=True)

    # Load already processed files
    processed_files = load_processed_files()

    # Add all files from backup folder to processed list
    if os.path.exists(BACKUP_FOLDER):
        for backup_file in os.listdir(BACKUP_FOLDER):
            if backup_file.endswith('.mp3') and backup_file not in processed_files:
                mark_as_processed(backup_file)
                processed_files.add(backup_file)
    
    # Get all MP3 files
    mp3_files = [f for f in os.listdir(SOURCE_FOLDER) if f.endswith('.mp3')]
    
    print(f"Found {len(mp3_files)} MP3 files")
    print(f"Checking for excessive silence at end (>{MAX_END_SILENCE}s)...\n")
    
    fixed_count = 0

    for idx, filename in enumerate(sorted(mp3_files), 1):
        filepath = os.path.join(SOURCE_FOLDER, filename)

        print(f"[{idx}/{len(mp3_files)}] {filename}")

        # Skip empty files (placeholders for problematic stories)
        if os.path.getsize(filepath) == 0:
            print(f"   → Empty placeholder file, skipping\n")
            continue

        # Skip if already processed
        if filename in processed_files:
            print(f"   → Already processed, skipping\n")
            continue

        # Get total duration
        total_duration = get_audio_duration(filepath)

        # If file is longer than 1 hour, trim to 1 hour first (fast)
        if total_duration > 3600:
            print(f"   File too long ({int(total_duration)}s), trimming to 1 hour first...")
            temp_path = filepath + ".temp.mp3"
            trim_file(filepath, temp_path, 3600)
            # Replace original with trimmed version for analysis
            os.replace(temp_path, filepath)
            total_duration = 3600

        # Detect silence at end
        last_silence = detect_silence_at_end(filepath)
        
        if last_silence:
            silence_start = last_silence['end'] - last_silence['duration']
            end_silence_duration = total_duration - silence_start
            
            if end_silence_duration > MAX_END_SILENCE:
                print(f"✂️  {filename}")
                print(f"   Total: {int(total_duration)}s, End silence: {int(end_silence_duration)}s")
                
                # Move original to backup
                backup_path = os.path.join(BACKUP_FOLDER, filename)
                shutil.move(filepath, backup_path)
                
                # Trim and save with original name
                new_duration = silence_start + MAX_END_SILENCE
                trim_file(backup_path, filepath, new_duration)
                
                print(f"   → Trimmed to {int(new_duration)}s (removed {int(end_silence_duration - MAX_END_SILENCE)}s)\n")
                fixed_count += 1
        else:
            # No significant silence detected
            pass

        # Mark as processed
        mark_as_processed(filename)
        processed_files.add(filename)
    
    print(f"\n{'='*60}")
    print(f"✓ Done! Fixed {fixed_count} files")
    print(f"Originals backed up to: {BACKUP_FOLDER}/")
    print(f"{'='*60}")

if __name__ == "__main__":
    main()
