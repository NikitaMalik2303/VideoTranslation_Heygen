from transformers import MarianMTModel, MarianTokenizer
import pysrt
from comet import download_model, load_from_checkpoint

# Using hf model for translation
model_name= "Helsinki-NLP/opus-mt-en-de"
tokenizer= MarianTokenizer.from_pretrained(model_name)
model= MarianMTModel.from_pretrained(model_name)

# Translating text from eng to german 
org_text= pysrt.open("data/input/Tanzania-caption.srt")
translated_path= "data/output/subtitles_de.srt"

translations=[] #for eval
with open(translated_path, "w", encoding="utf-8") as f:
    for line in org_text:
        eng_text= line.text.replace("\n", " ")
        inputs= tokenizer([eng_text], return_tensors="pt", padding=True, truncation=True)
        outputs= model.generate(**inputs, max_length=512)
        german_text= tokenizer.batch_decode(outputs, skip_special_tokens=True)[0]
        
        f.write(f"{line.index}\n")
        f.write(f"{line.start} --> {line.end}\n")
        f.write(f"{german_text}\n")
        f.write(f"\n")

        translations.append({
            "src": eng_text, 
            "mt": german_text, 
            "ref": None
        })
