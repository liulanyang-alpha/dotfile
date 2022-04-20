#!/bin/bash
basedir=`cd $(dirname $0); pwd -P`


# 1 copy some file
echo "==> copy dotfiles "
mkdir -p ~/.pip
cp ${basedir}/dot/pip.conf ~/.pip/
cp ${basedir}/dot/.vimrc ~/.vimrc
cp ${basedir}/dot/.gitconfig ~/.gitconfig
cp ${basedir}/dot/.tmux.conf ~/.tmux.conf
cp -r ${basedir}/dot/.oh-my-zsh ~/.oh-my-zsh
cp ${basedir}/dot/.zshrc ~/.zshrc

mkdir -p ~/env
cp -r ${basedir}/bin ~/env/bin

echo "==> copy done!!!"
