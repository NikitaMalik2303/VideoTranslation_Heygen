#!/bin/bash

# Usage:
#   ./replace_audio.sh input_video.mp4 new_audio.wav output_video.mp4
#   main/replace_audio.sh data/input/Tanzania-2.mp4 data/output/translated_audio_2.wav data/output/Tanzania-German_2.mp4

INPUT_VIDEO="$1"
NEW_AUDIO="$2"
OUTPUT_VIDEO="$3"

if [ ! -f "$INPUT_VIDEO" ]; then
    echo "Error: Input video not found: $INPUT_VIDEO"
    exit 1
fi

if [ ! -f "$NEW_AUDIO" ]; then
    echo "Error: New audio not found: $NEW_AUDIO"
    exit 1
fi

if [ -z "$OUTPUT_VIDEO" ]; then
    OUTPUT_VIDEO="output_with_new_audio.mp4"
fi

echo "Replacing audio in video..."
echo "Input Video:  $INPUT_VIDEO"
echo "New Audio:    $NEW_AUDIO"
echo "Output Video: $OUTPUT_VIDEO"


ffmpeg -y \
    -i "$INPUT_VIDEO" \
    -i "$NEW_AUDIO" \
    -map 0:v -map 1:a \
    -c:v copy \
    -c:a aac \
    -b:a 192k \
    -shortest \
    "$OUTPUT_VIDEO"

echo "Done!"
echo "New video created at: $OUTPUT_VIDEO"
