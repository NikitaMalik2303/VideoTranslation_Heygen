# Video Translation from English to German

This project implements a full pipeline for video translation and dubbing from English to German, including:

* Translating subtitles
* Generating German speech using Coqui XTTS (voice cloning)
* Automatically time-aligning speech to match the original English timing
* Merging all segments into a final synchronized audio track
* Replacing original video audio with the new German narration

# Pipeline Summary

1) Translating to German subtitles
* Uses MarianMT for Translation 

2) Voice Cloning
* Uses Coqui XTTS v2 to extract reference voice from english video and then and synthesize german audio per timestamp.

3) Merging all voice segments together
* To preserve the narration flow, I use fixed pitch preserving time streching using Rubberband. This helped to adjust the longer length of german sentences to fit in the same window as english. I used limited streching to avoid generating robotic voice (+-5%).

* Padding/Trimming: If the audio is slightly longer than the window, it is trimmed and it is padded with silence if it is shorter than the window,

4) Merging audio and video
* Replaces the original audio with the general video maintains the timestamps synchornization. 

# Limitations of the approach used
* The strech limit prevents extreme duration mismatch. 
* Segment-wise XTTS generation and pitch modifications introduces slight tone differences between segments.
* Emotional cues from the video are not preserved

* The natural flow of the method could have been improved by tracking the silence in the original audio. However, since the original english srt file doesn't include it. I skipped the part.

# Installation and Setup

1) Clone the respository
```python
git clone https://github.com/NikitaMalik2303/VideoTranslation_Heygen.git
cd VideoTranslation_Heygen
```

2) Create conda environment
```python
conda create -n video_translation python=3.10.19
conda activate video_translation 
```

3) Install Dependencies
```python
pip install -r requirements.txt
```

4) Translation 
```python
python main/translate.py
```

The translated captions in german are stored in output

5) Extract reference audio for voice cloning
```python
ffmpeg -i data/input/Tanzania-2.mp4 -ss 00:00:01 -t 10 -vn data/output/ref_aud.wav
```

6) Generating synchronised German audio
```python
python main/audio_syn.py 
```



The generated audio is saved in data/output/translated_audio.wav

7) Replacing original video audio with german audio
```python
main/replace_audio.sh data/input/Tanzania-2.mp4 data/output/translated_audio.wav data/output/Tanzania-German.mp4
```

The generated video is saved in data/output/Tanzania-German.mp4

# Generated Video

https://github.com/user-attachments/assets/28f6dcb5-8e64-4059-9689-e454ff7f578f
<!-- <video src="https://raw.githubusercontent.com/NikitaMalik2303/VideoTranslation_Heygen/main/data/output/Tanzania-German.mp4" width="600" controls></video> -->
