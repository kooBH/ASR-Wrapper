import numpy as np
import os,glob,argparse
import librosa as rs
import soundfile as sf
from tqdm.auto import tqdm


if __name__ == "__main__" : 
    parser = argparse.ArgumentParser()
    parser.add_argument('--dir_clean',"-c", type=str, required=True)
    parser.add_argument('--dir_noise',"-n", type=str, required=True)
    parser.add_argument('--dir_out',"-o", type=str, required=True)
    parser.add_argument('--SNR', type=int, required=True)
    parser.add_argument('--samplerate', type=int, default=16000)
    args = parser.parse_args()

    dir_clean = args.dir_clean
    dir_noise = args.dir_noise
    dir_out = args.dir_out
    sr = args.samplerate

    SNR = args.SNR

    list_clean = glob.glob(os.path.join(dir_clean,"**","*.wav"),recursive=True)
    list_noise = glob.glob(os.path.join(dir_noise,"**","*.wav"),recursive=True)
    print(f"List of clean : {dir_clean} {len(list_clean)}")
    print(f"List of noise : {dir_noise} {len(list_noise)}")
    print(f"Mixing for {args.dir_out} with SNR {SNR}dB")

    for path in tqdm(list_clean) : 
        base_dir = os.path.dirname(path)
        base_name = os.path.basename(path)
        output_dir = base_dir.replace(dir_clean,dir_out)
        os.makedirs(output_dir,exist_ok=True)
        output_path = os.path.join(output_dir,base_name)


        path_noise = np.random.choice(list_noise)

        clean = rs.load(path,sr=sr)[0]
        noise = rs.load(path_noise,sr=sr)[0]

        # match noise length to clean length
        while len(clean) > len(noise) :
            path_noise = np.random.choice(list_noise)
            noise_t = rs.load(path_noise,sr=sr)[0]
            noise = np.concatenate([noise,noise_t])
        noise = noise[:len(clean)]

        # SNR adjustment
        clean_rms = (clean**2).mean()**0.5
        noise_rms = (noise**2).mean()**0.5

        snr_scalar = clean_rms / (10**(SNR/10))/ (noise_rms + 1e-7)
        noise = noise * snr_scalar

        # mix
        noisy = clean + noise
        noisy = noisy / (np.abs(noisy).max() + 1e-7)

        # save
        sf.write(output_path, noisy, sr)









