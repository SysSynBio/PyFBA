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
    python-pip python3 python3-dev python3-pip && \
    pip3 install lxml python-libsbml-experimental beautifulsoup4 setuptools setuptools_scm && \
    # Build and install pyglpk
    git clone https://github.com/bradfordboyle/pyglpk && \
    cd pyglpk && \
    python3 setup.py build && \
    python3 setup.py install && \
    #make . && \
    #make test && \
    #make install && \
    cd .. && \
    rm -rf pyglpk && \
    # Download ModelSEED database and set environment variable
    git clone https://github.com/ModelSEED/ModelSEEDDatabase && \
    # Build and install PyFBA
    git clone https://github.com/SysSynBio/PyFBA.git && \
    cd PyFBA && \
    python3 setup.py build && \
    python3 setup.py test && \
    python3 setup.py install && \
    mv media /data/media && \
    cd .. && \
    rm -rf PyFBA && \
    # Remove unnecessary build dependencies
    apt-get -y purge --auto-remove g++ gcc git python-pip

# create user for container
#RUN useradd -r -s /sbin/nologin pyfba
#USER pyfba

# Now copy the scripts that assign functions to reactions

