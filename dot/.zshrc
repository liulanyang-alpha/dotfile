
#### 1. for zsh config

export ZSH="$HOME/.oh-my-zsh"
ZSH_THEME="fishy"
plugins=(git zsh-autosuggestions zsh-syntax-highlighting extract)
source $ZSH/oh-my-zsh.sh


alias ls='ls --color=auto'

#### 2. custom config
export SHELL="/usr/bin/zsh"
export PATH=${HOME}/env/bin:$PATH
export LD_LIBRARY_PATH=${HOME}/env/lib:${LD_LIBRARY_PATH}

export QT_AUTO_SCREEN_SCALE_FACTOR=1  # for flameshot
export TERM=xterm-256color     # fix tmux autosuggestion color

#### 3. cuda
export CUDA_HOME=/usr/local/cuda
export PATH=$PATH:$CUDA_HOME/bin
export LD_LIBRARY_PATH=${CUDA_HOME}/lib64:$LD_LIBRARY_PATH
export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:$CUDA_HOME/extras/CUPTI/lib64
export CUDA_DEVICES_ORDER=PCI_BUS_IS