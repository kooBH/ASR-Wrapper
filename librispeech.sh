#!/bin/bash

DIR_LABEL=/home/data/LibriSpeech/test-clean
MODEL=large-v2
DEVICE=cuda:1

: <<'END_COMMENT'
# clean evaluation
DIR_IN=/home/data/LibriSpeech/test-clean
DIR_LABEL=/home/data/LibriSpeech/test-clean
DIR_OUT=/home/data/Libri-test/result
FORMAT=flac
VERSION=clean

python WER_whisper.py -i ${DIR_IN} -l ${DIR_LABEL} -o ${DIR_OUT} -v ${VERSION} -f ${FORMAT} -m ${MODEL} -d ${DEVICE}
END_COMMENT


DIR_IN=/home/data/kbh/Libri-test/noisy
DIR_OUT=/home/data/kbh/Libri-test/result
FORMAT=wav
VERSION=noisy

#for SNR in SNR-10 SNR-5 SNR0 SNR5 SNR10 SNR15;
for SNR in SNR-10;
do
python WER_whisper.py -i ${DIR_IN}/${SNR} -l ${DIR_LABEL} -o ${DIR_OUT} -v ${VERSION}_${SNR} -f ${FORMAT} -m ${MODEL} -d ${DEVICE}
done
