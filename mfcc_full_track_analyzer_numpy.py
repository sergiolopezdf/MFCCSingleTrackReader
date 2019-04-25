import essentia
from essentia.standard import *
from pathlib import Path
from pylab import plot, show, figure, imshow
import matplotlib.pyplot as plt
from numpy import save
from numpy import append


class TrackMFCCExtractor:
    def __init__(self, file_path, tag, start_time, duration, file_name):
        self.tag = tag
        self.path = Path(file_path)
        self.start_time = start_time
        self.duration = duration
        self.mfccs = None
        self.melbands = None
        self.melbands_log = None
        self.file_name = file_name

    def run(self):
        # we start by instantiating the audio loader:
        loader = essentia.standard.EasyLoader(filename=str(self.path), startTime=self.start_time,
                                              endTime=(self.start_time + self.duration))

        # and then we actually perform the loading:
        audio = loader()

        w = Windowing(type='hann')
        spectrum = Spectrum()  # FFT() would return the complex FFT, here we just want the magnitude spectrum
        mfcc = MFCC()
        logNorm = UnaryOperator(type='log')

        mfccs = []
        melbands = []
        melbands_log = []

        bpm = 128
        fr = 44100
        hopSize_seg = 1
        hopSize = hopSize_seg * fr

        for frame in FrameGenerator(audio, frameSize=1024 * 4, hopSize=int(hopSize), startFromZero=True):
            mfcc_bands, mfcc_coeffs = mfcc(spectrum(w(frame)))
            mfcc_coeffs = append(mfcc_coeffs, self.tag)
            mfccs.append(mfcc_coeffs)
            melbands.append(mfcc_bands)
            melbands_log.append(logNorm(mfcc_bands))

        self.mfccs = mfccs
        self.melbands = melbands
        self.melbands_log = melbands_log

        save(self.file_name, arr=mfccs)
        # print(mfccs)

    def plot(self):
        # transpose to have it in a better shape
        mfccs = essentia.array(self.mfccs.values.tolist()).T
        melbands = essentia.array(self.melbands.values.tolist()).T
        melbands_log = essentia.array(self.melbands_log.values.tolist()).T

        # and plot
        imshow(melbands[:, :], aspect='auto', origin='lower', interpolation='none')
        plt.title("Mel band spectral energies in frames")
        show()

        imshow(melbands_log[:, :], aspect='auto', origin='lower', interpolation='none')
        plt.title("Log-normalized mel band spectral energies in frames")
        show()

        imshow(mfccs[1:, :], aspect='auto', origin='lower', interpolation='none')
        plt.title("MFCCs in frames")
        show()


#####################################################
####################### TEST ########################
#####################################################
tfe = TrackMFCCExtractor('Martin Garrix, Bonn - High On Life (Original Mix) [SWM].mp3', '0', 45, 15,'2')
tfe.run()
