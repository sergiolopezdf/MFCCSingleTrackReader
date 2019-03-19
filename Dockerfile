FROM continuumio/miniconda3
RUN apt-get update
WORKDIR home/
RUN git clone https://github.com/sergiolopezdf/MFCCSingleTrackReader
WORKDIR MFCCSingleTrackReader
RUN conda env create -f MusicAnalyzerEnvironment.yml