# Image for PyFBA http://linsalrob.github.io/PyFBA/index.html
FROM ubuntu:18.04
MAINTAINER Song Feng <song.feng@outlook.com>

# All packages will be downloaded and built under /data
WORKDIR /data

# Set environment variables needed for PyFBA
ENV ModelSEEDDatabase="/data/ModelSEEDDatabase"
ENV PYFBA_MEDIA_DIR="/data/media"

# Install packages available in repositories
RUN apt-get update && \
    apt-get -y --no-install-recommends install build-essential git libglpk40 \
    libglpk-dev glpk-utils libgmp10 libgmpxx4ldbl python python-dev \
    python-pip python3 python3-dev python3-pip
# Remove unnecessary build dependencies
#RUN apt-get -y purge --auto-remove g++ gcc git python-pip

RUN pip3 install lxml python-libsbml-experimental beautifulsoup4 setuptools setuptools_scm wheel

# Build and install pyglpk
#RUN git clone https://github.com/bradfordboyle/pyglpk && \
#    cd pyglpk && \
#    python3 setup.py build && \
#    python3 setup.py install && \
#    #make . && \
#    #make test && \
#    #make install && \
#    cd .. && \
#    rm -rf pyglpk
RUN pip3 install glpk

# Download ModelSEED database and set environment variable
RUN cd /data && git clone https://github.com/ModelSEED/ModelSEEDDatabase

# Build and install PyFBA
# RUN cd /data && git clone https://github.com/SysSynBio/PyFBA.git && \
#     cd PyFBA && \
#     python3 setup.py build && \
#     #python3 setup.py test && \
#     python3 setup.py install && \
#     mv media /data/media && \
#     cd .. && \
#     rm -rf PyFBA
RUN pip3 install pyfba

# create user for container
#RUN useradd -r -s /sbin/nologin pyfba
#USER pyfba

# Now copy the scripts that assign functions to reactions
COPY getGaps.py /bin/getGaps.py
RUN chmod +x /bin/getGaps.py

