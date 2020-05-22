# https://hub.docker.com/r/cwaffles/openpose
FROM nvidia/cuda:10.0-cudnn7-devel

#get deps
RUN apt-get update && \
DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
python3-dev python3-pip vim git g++ wget make libprotobuf-dev protobuf-compiler libopencv-dev \
libgoogle-glog-dev libboost-all-dev libcaffe-cuda-dev libhdf5-dev libatlas-base-dev

#for python api
RUN pip3 install numpy opencv-python flask pillow

#replace cmake as old version has CUDA variable bugs
RUN wget https://github.com/Kitware/CMake/releases/download/v3.16.0/cmake-3.16.0-Linux-x86_64.tar.gz && \
tar xzf cmake-3.16.0-Linux-x86_64.tar.gz -C /opt && \
rm cmake-3.16.0-Linux-x86_64.tar.gz
ENV PATH="/opt/cmake-3.16.0-Linux-x86_64/bin:${PATH}"

#get openpose
WORKDIR /openpose
COPY ./3rdparty ./3rdparty
COPY ./cmake ./cmake
COPY ./doc ./doc
COPY ./include ./include
COPY ./models ./models
COPY ./python ./python
COPY ./scripts ./scripts
COPY ./src ./src
COPY CMakeLists.txt ./CMakeLists.txt
COPY ./examples ./examples
COPY .travis.yml ./.travis.yml
COPY appveyor.yml ./appveyor.yml
COPY ./.github ./.github
# COPY ./.git ./.git
RUN git init && git submodule add https://github.com/CMU-Perceptual-Computing-Lab/caffe.git 3rdparty/caffe && \
    git submodule add https://github.com/pybind/pybind11.git 3rdparty/pybind11 && \
    git submodule update
# COPY ./.gitmodules ./.gitmodules

# RUN git clone https://github.com/CMU-Perceptual-Computing-Lab/openpose.git .

#build it
WORKDIR /openpose/build
RUN cmake -DBUILD_PYTHON=ON .. && make -j `nproc`
WORKDIR /openpose

COPY python_scripts/ /openpose/python_scripts/

# RUN pip3 install pillow
EXPOSE 300
WORKDIR /openpose/python_scripts
CMD ["/bin/bash", "/openpose/python_scripts/run.sh"]
# docker run -it --rm --runtime=nvidia -e NVIDIA_VISIBLE_DEVICES=0 pyopenpose