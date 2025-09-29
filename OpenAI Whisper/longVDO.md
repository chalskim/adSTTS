# Handling Long Audio Files with OpenAI Whisper

This document explains how to modify the Whisper STT implementation to handle long audio files efficiently by processing them in chunks.

## Problem

When processing long audio files with OpenAI Whisper, several issues can occur:
1. **Memory exhaustion**: Large audio files consume significant RAM during processing
2. **Performance degradation**: Processing very large files can be extremely slow
3. **GPU memory issues**: Large files may exceed GPU memory limits

## Solution

The solution is to process large audio files in smaller chunks and then combine the transcriptions. This approach:
1. Reduces memory usage
2. Provides more responsive feedback during processing
3. Prevents system resource exhaustion

## Implementation Details

### 1. Intelligent Detection of Large Files

The enhanced script uses two criteria to detect when to switch to chunked processing:

1. **Duration-based**: Files longer than 30 minutes
2. **Size-based**: Files larger than 100 MB

```python
# Get file info
file_info = sf.info(file_path)
duration = file_info.duration

# Get file size
file_size = os.path.getsize(file_path)  # in bytes
file_size_mb = file_size / (1024 * 1024)

# For long files (>30 minutes) OR large files (>100 MB), process in chunks
if duration > 1800 or file_size_mb > 100:  # 30 minutes OR 100 MB
    return transcribe_long_audio(file_path, model_size)
```

This dual approach ensures that both very long files and very large files (which might be short but high-quality) are handled appropriately.

### 2. Output Organization

All transcriptions are saved to an `output` folder with consistent naming:
- The output folder is automatically created if it doesn't exist
- Files are named with the same base name as the input file plus `_transcription.txt`
- Example: `my_audio.mp3` → `output/my_audio_transcription.txt`

### 3. Chunked Processing Function

The [transcribe_long_audio](file:///Users/zing1977gmail.com/src/STTtest/OpenAI Whisper/whisper_stt.py#L49-L107) function handles the chunked processing:

```python
def transcribe_long_audio(file_path, model_size="base", chunk_duration=600):
    """
    Transcribe long audio files by processing in chunks
    """
```

### 4. Key Features

- **Intelligent detection**: Uses both duration and file size criteria
- **Automatic chunking**: Files are divided into 10-minute chunks by default
- **Stereo to mono conversion**: Automatically handles stereo files
- **Error handling**: Continues processing even if individual chunks fail
- **Progress reporting**: Shows which chunk is being processed
- **Memory efficiency**: Processes one chunk at a time
- **Organized output**: Saves transcriptions to a dedicated output folder

## Usage

The usage remains the same as the original script:

```bash
python whisper_stt.py <audio_file_path> [model_size]
```

For large files, the script will automatically:
1. Detect that it's a large file (by duration or size)
2. Process it in chunks
3. Combine all transcriptions
4. Save the complete transcription to the `output` folder

## Configuration

You can adjust the thresholds and chunk duration:

```python
# Duration threshold (in seconds)
duration_threshold = 1800  # 30 minutes

# File size threshold (in MB)
size_threshold = 100  # 100 MB

# Chunk duration (in seconds)
chunk_duration = 600  # 10 minutes
```

## Benefits

1. **Memory efficient**: Only one chunk is loaded into memory at a time
2. **Progress tracking**: Users can see which chunk is being processed
3. **Fault tolerance**: If one chunk fails, processing continues with other chunks
4. **Automatic detection**: No need to manually specify when to use chunked processing
5. **Seamless integration**: Works transparently with existing workflows
6. **Dual criteria**: Handles both long duration and large size files
7. **Organized output**: Consistent file organization in dedicated output folder

## Limitations

1. **Context loss**: Very long sentences that span chunk boundaries may be split
2. **Processing time**: Still requires significant time for very long files
3. **Model loading**: The model is loaded once but used for all chunks

## Best Practices

1. **Choose appropriate chunk sizes**: 5-15 minutes usually works well
2. **Use smaller models for large files**: `base` or `small` models for very large files
3. **Monitor system resources**: Watch memory usage during processing
4. **Consider hardware**: GPU processing is faster but requires more memory

## Example Output

When processing a large file, you'll see output like:
```
Audio file info - Duration: 45.5 minutes, Size: 125.3 MB
Large audio file detected. Processing in chunks...
Processing long audio file in 10.0-minute chunks...
Loading Whisper base model...
Processing chunk 1/5...
Processing chunk 2/5...
Processing chunk 3/5...
Processing chunk 4/5...
Processing chunk 5/5...

Transcription:
==================================================
[Complete transcription of the large audio file]
==================================================

Transcription saved to: output/large_audio_transcription.txt
```