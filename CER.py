import ETRI
import metric
import argparse
from datetime import datetime
import os.path

if __name__ == '__main__' : 
    parser = argparse.ArgumentParser()
    parser.add_argument('--input', '-i', type=str, required=True,
                        help="input audio path")
    parser.add_argument('--script', '-s', type=str, required=True,
                        help="ground truth script")
    parser.add_argument('--output', '-o', type=str, required=False
                        ,default='./', help="output path[WIP]")
    parser.add_argument('--type', '-t', type=str, required=False, default='ETRI'
                        ,help="ASR type[WIP]")
    args = parser.parse_args()

    # path
    audio_path = args.input
    script_path =  args.script
    output_path = args.output + '/' + str(datetime.now().strftime("%Y%m%d-%H-%M-%S.txt"))

    # ground truth
    script = open(script_path,encoding='UTF8')
    ground_truth = script.readlines()[0]
    # elim dot
    ground_truth = ground_truth.replace('.','')
    script.close()

    # ASR
    if os.path.isfile(audio_path):
	ASR_result = ETRI.ASR(audio_path)
	# input data is not enough to recognize
	ASR_result= ASR_result.replace('Handler didnt call response()','') 
	# adjust with ground truth
	ASR_result = ASR_result.replace('‘','')
 	ASR_result = ASR_result.replace('’','')
    else:
        print('ERROR::No file : ' + audio_path)
        return

    # Error
    CER = metric.CharacterErrorRate()
    dist,length = CER.metric(ground_truth, ASR_result)
    cer = dist/length

    # result log
    ret = open(output_path,'w')
    ret.write("+ input : %s\n"%args.input)
    ret.write("+ script : %s\n"%args.script)
    ret.write("+ CER\n")
    ret.write("%f\n"%cer)
    ret.write("+ Ground Truth\n")
    ret.write(ground_truth + "\n")
    ret.write("+ ASR %s result\n" % args.type)
    ret.write(ASR_result + "\n")
    ret.close()

    print('CER : '+str(cer))

