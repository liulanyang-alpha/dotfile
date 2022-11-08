FROM ubuntu:20.04
RUN apt-get update \
    && apt-get install -y --no-install-recommends apt-utils build-essential vim sudo git \
    && apt-get install -y zsh zip unzip libsm6 libxext6 libxrender-dev libgl1-mesa-glx rsync zsh git-lfs

#RUN useradd -m docker && echo "docker:docker" | chpasswd && adduser docker sudo
ENV HOME /root
ENV SHELL /usr/bin/zsh
ADD dotfile $HOME/dotfile

RUN chsh -s /bin/zsh \
    && cd $HOME/dotfile \
    && bash copy_dot.sh


WORKDIR /root
ENTRYPOINT ["/bin/zsh"]