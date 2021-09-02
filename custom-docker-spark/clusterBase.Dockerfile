ARG debian_buster_image_tag=8-jdk-slim-buster
FROM openjdk:${debian_buster_image_tag}

# -- Layer: OS + Python 3.7

ARG shared_workspace=/opt/workspace

# RUN mkdir -p ${shared_workspace} && \
#     apt-get update -y && apt-get -y upgrade && \
#     apt-get install -y python && \
#     ln -s /usr/bin/python3 /usr/bin/python && \
#     rm -rf /var/lib/apt/lists/*
RUN mkdir -p ${shared_workspace}
# RUN apt-get update && apt-get install -y apt-utils &&\
#     apt-get install -y software-properties-common && \
#     add-apt-repository ppa:deadsnakes/ppa && \
#     apt-get update && \
#     apt-get install -y python3.6
# RUN apt-get update -y && apt-get -y upgrade && \
#     apt-get install -y make build-essential libssl-dev zlib1g-dev libbz2-dev libsqlite3-dev && \
#     apt-get install -y build-essential && apt-get install zlib1g-dev
# RUN apt-get install -y libssl-dev openssl && apt-get install -y wget && \
#     wget https://www.python.org/ftp/python/3.5.1/Python-3.5.1.tgz &&  \
#     tar xzvf Python-3.5.1.tgz
# RUN cd Python-3.5.1 && ./configure && \
#     make && make install 

ENV SHARED_WORKSPACE=${shared_workspace}

# -- Runtime

VOLUME ${shared_workspace}
CMD ["bash"]

