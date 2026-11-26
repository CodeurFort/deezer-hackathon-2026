import sys, warnings, numpy as np, librosa, scipy.signal as sg
warnings.filterwarnings("ignore")
NOTES = ['C','C#','D','D#','E','F','F#','G','G#','A','A#','B']
def basse(f):
    y, sr = librosa.load(f, sr=22050, mono=True)
    b, a = sg.butter(4, 200 / (sr / 2), btype='low'); low = sg.filtfilt(b, a, y)          # garder les graves
    tempo, beats = librosa.beat.beat_track(y=y, sr=sr, units='frames')
    chroma = librosa.feature.chroma_cqt(y=low, sr=sr, fmin=librosa.note_to_hz('E1'), n_octaves=3, bins_per_octave=36)
    sync = librosa.util.sync(chroma, beats, aggregate=np.median)                          # une valeur par temps
    notes = [int(np.argmax(c)) for c in sync.T]
    seq = []                                                                              # fusion des répétitions
    for n in notes:
        if not seq or seq[-1] != n: seq.append(n)
    desc = [i for i in range(len(seq) - 3) if all((seq[i+k] - seq[i+k+1]) % 12 in (1, 2) for k in range(3))]
    return float(np.atleast_1d(tempo)[0]), seq, desc
if __name__ == "__main__":
    for f in sys.argv[1:]:
        tempo, seq, desc = basse(f)
        print(f"{f.split('/')[-1]:28s} tempo {tempo:5.1f} | basse : {' '.join(NOTES[n] for n in seq[:22])}")
        print(f"{'':28s} lignes descendantes de 4 notes : {len(desc)} | ex. : {[' '.join(NOTES[n] for n in seq[i:i+4]) for i in desc[:3]]}")
