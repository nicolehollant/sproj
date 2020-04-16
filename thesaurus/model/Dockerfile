# FROM python:3.7-alpine3.11
# RUN mkdir -p app
# COPY . /app
# WORKDIR /app
# RUN apk add --update curl gcc g++ libc-dev
# RUN apk --no-cache add lapack libstdc++ && apk --no-cache add --virtual .builddeps g++ gcc gfortran musl-dev lapack-dev && pip install scipy && apk del .builddeps && rm -rf /root/.cache
# RUN ln -s /usr/include/locale.h /usr/include/xlocale.h
# RUN easy_install cython
# RUN pip install --upgrade pip
# # ADD repositories /etc/apk/repositories
# # RUN apk add --update python python-dev gfortran py-pip build-base py-numpy@community
# RUN pip install -r requirements.txt
# EXPOSE 5000
# CMD ["python3", "-m", "model"]


# specifiy base image
FROM ubuntu:16.04

RUN mkdir -p app
COPY . /app
WORKDIR /app

# Update the sources list
RUN apt-get update

# install useful system tools and libraries
RUN apt-get install -y libfreetype6-dev && \
    apt-get install -y libglib2.0-0 \
                       libxext6 \
                       libsm6 \
                       libxrender1 \
                       libblas-dev \
                       liblapack-dev \
                       gfortran \
                       libfontconfig1 --fix-missing

RUN apt-get install -y tar \
                    git \
                    curl \
                    nano \
                    wget \
                    dialog \
                    net-tools \
                    build-essential

# install Python and pip package manager
RUN apt-get install -y python3 \
                       python3-dev \
                       python3-pip

# intall useful and/or required Python libraries to run your script
# RUN pip install matplotlib \
#                 seaborn \
#                 pandas \
#                 numpy \
#                 scipy \
#                 sklearn \
#                 python-dateutil \
#                 gensim
RUN pip3 install -r requirements.txt
# define command to when Docker container starts
EXPOSE 5000
CMD ["python3", "-m", "model"]