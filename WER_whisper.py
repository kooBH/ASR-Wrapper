"""
+ Requirements
Whisper
whisper_normalizer
editdistance
LibriSpeech Corpus

---

$ pip install -U openai-whisper
$ pip install editdistance
$ pip install whisper_normalizer
https://www.openslr.org/12

You may need to update ffmpeg

$ sudo apt update && sudo apt install ffmpeg

+ Whisper
Size	Parameters	English-only model	Multilingual model	Required VRAM	Relative speed
tiny	39 M	tiny.en	tiny	~1 GB	~32x
base	74 M	base.en	base	~1 GB	~16x
small	244 M	small.en	small	~2 GB	~6x
medium	769 M	medium.en	medium	~5 GB	~2x
large	1550 M	N/A	large	~10 GB	1x

"""

import whisper
from whisper_normalizer.basic import BasicTextNormalizer
import editdistance
import os,glob,argparse
from tqdm.auto import tqdm

parser = argparse.ArgumentParser()
parser.add_argument('--dir_in',"-i", type=str, required=True)
parser.add_argument('--dir_label',"-l", type=str, required=True)
parser.add_argument('--dir_out',"-o", type=str, required=True)
parser.add_argument('--version',"-v", type=str, required=True)
parser.add_argument('--format',"-f", type=str, default="flac")
parser.add_argument('--model',"-m", type=str, default="large-v2")
parser.add_argument('--device',"-d", type=str, default="cpu")
args = parser.parse_args()

type_whisper =  args.model
list_trans = glob.glob(os.path.join(args.dir_label,"**","*.txt"),recursive=True)

print("Evaluate WER for {} {}".format(args.dir_in,len(list_trans)))
print("whisper model : ",type_whisper)
model = whisper.load_model(type_whisper)
model = model.to(args.device)
normalizer = BasicTextNormalizer()
format = args.format
version = args.version

distance = 0
total = 0
WER = 0

for item in tqdm(list_trans) :

    dir_audio = os.path.dirname(item)
    dir_audio = dir_audio.replace(args.dir_label,args.dir_in)
    # parse transcript
    with open(item,"r") as f:
        txt = f.readlines()
        list_id = [t.split(" ")[0] for t in txt]
        list_tsc = [t.split(list_id[idx])[1].replace("\n","") for idx,t in enumerate(txt)]

        # iteration for directory
        for idx in range(len(list_id)):
            result = model.transcribe(os.path.join(dir_audio,list_id[idx]+f".{format}"))
            estim = result["text"].upper()
            GT = list_tsc[idx]
            estim = normalizer(estim)
            GT = normalizer(GT)

            t_d = editdistance.eval(estim, GT)
            t_total = len(GT.split(" "))

            distance += t_d
            total += t_total

WER = (distance/total)*100
print("WER : {} | {}/{}".format(WER, distance, total))

os.makedir(args.dir_out,exist_ok=True)
with open(os.path.join(args.dir_out,f"{version}_{model}_{WER:.2f}.txt"),"w") as f :
    f.write(f"{WER}")

#list_audio = glob.glob(os.path.join(dir_audio,"*.flac"))
#print(dir_audio)

