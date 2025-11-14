import pysrt
import os
from pydub import AudioSegment
from TTS.api import TTS
import pyrubberband as pyrb
import soundfile as sf

max_strech = 1.05   
max_compress = 0.95
fade_durr= 50

video_pth= "data/input/Tanzania-2.mp4"
ref_audio= "data/output/ref_aud.wav"
german_txt= "data/output/subtitles_de.srt"
output_vid= "data/output/translated_audio.wav"
segment_audio= "data/output/audio_segments"
os.makedirs(segment_audio, exist_ok=True)

text= pysrt.open(german_txt)
tts= TTS("tts_models/multilingual/multi-dataset/xtts_v2")

audio_full= AudioSegment.silent(duration=0)
for line in text:
    txt= line.text.replace("\n", " ")
    start_t, end_t, idx= line.start.ordinal, line.end.ordinal, line.index
    curr_dur= end_t- start_t

    f_pth= os.path.join(segment_audio, f"seg_{idx}.wav")

    tts.tts_to_file(
        text=txt, 
        file_path=f_pth, 
        speaker_wav= ref_audio, 
        language="de"
    )

    y, sr= sf.read(f_pth)
    ger_len = int(len(y)/ sr*1000)

    stretch_ratio= ger_len/curr_dur

    if 0.97 < stretch_ratio < 1.03:
        y_stretched = y
    else:
        factor = 1 / stretch_ratio    
        if factor > max_strech:
            factor = max_strech
        if factor < max_compress:
            factor = max_compress
        y_stretched = pyrb.time_stretch(y, sr, factor)
    
    sf.write(f_pth, y_stretched, sr)

    curr_aud = AudioSegment.from_wav(f_pth)
    
    if len(curr_aud)< curr_dur:
        curr_aud+= AudioSegment.silent(duration= curr_dur- len(curr_aud))
    else:
        print(f"German longer by {len(curr_aud) - curr_dur} ms")
        curr_aud= curr_aud[:curr_dur]
    
    curr_aud = curr_aud.fade_in(fade_durr).fade_out(fade_durr)
    
    if start_t> len(audio_full):
        audio_full+= AudioSegment.silent(duration= (start_t-len(audio_full)))
    
    audio_full+= curr_aud


audio_full.export(output_vid, format="wav")

