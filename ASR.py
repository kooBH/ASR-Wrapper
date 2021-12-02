import ETRI
from datetime import datetime
import os.path

#Read audio file in folder audio_path
#Write ETRI ASR result in output_path

audio_path = 'D:/albert/temp/separation/4/'
output_path = 'D:/albert/temp/separation/4.txt'
#output_path = 'D:/albert/temp/separation/' + str(datetime.now().strftime("%Y%m%d-%H-%M-%S.txt"))

audioList = os.listdir(audio_path)
ret = open(output_path,'w')
for audiofile in audioList:
    print(audio_path+audiofile)
    ASR_result = ETRI.ASR(audio_path+audiofile)
    print(ASR_result)
    # result log   
    ret.write("+ input : " + audio_path + audiofile + "\n")    
    ret.write("+ ASR result : " + ASR_result + "\n" )
    ret.write("\n")
ret.close()
