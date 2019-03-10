# ~/.profile: executed by the command interpreter for login shells.
# This file is not read by bash(1), if ~/.bash_profile or ~/.bash_login
# exists.
# see /usr/share/doc/bash/examples/startup-files for examples.
# the files are located in the bash-doc package.

# the default umask is set in /etc/profile; for setting the umask
# for ssh logins, install and configure the libpam-umask package.
#umask 022

# if running bash
if [ -n "$BASH_VERSION" ]; then
    # include .bashrc if it exists
    if [ -f "$HOME/.bashrc" ]; then
	. "$HOME/.bashrc"
    fi
fi

# set PATH so it includes user's private bin if it exists
if [ -d "$HOME/bin" ] ; then
    PATH="$HOME/bin:$PATH"
fi

# ===================================================
# platform specific
# ===================================================
UNAME=`uname`
# echo $UNAME

# MacOS
if [ $UNAME == "Darwin" ];
then
  export GREP_COLOR="1;37;41"

  export GREP_PARAM="-E"
  alias G='grep --color -E'
  alias g='grep --color -i -E'
  alias Gs='find -type f | xargs grep --color -r -E'
  alias gs='find -type f | xargs grep --color -r -i -E'
  alias Gsf='find -type f -follow | xargs grep --color -r -E'
  alias gsf='find -type f -follow | xargs grep --color -r -i -E'
  alias psg='ps -ef | grep -i --color -E'
  alias no='grep "/\.git/" -v -E'
fi

# Linux
if [ $UNAME == "Linux" ];
then
  export GREP_PARAM="-P"
  alias G='grep --color -P'
  alias g='grep --color -i -P'
  alias Gs='find -type f | xargs grep --color -r -P'
  alias gs='find -type f | xargs grep --color -r -i -P'
  alias Gsf='find -type f -follow | xargs grep --color -r -P'
  alias gsf='find -type f -follow | xargs grep --color -r -i -P'
  alias psg='ps -ef | grep -i --color -P'
  alias no='grep "/\.git/" -v -P'
fi

# ===================================================
# color
# ===================================================
RESET="\[\e[m\]"

RED="\[\e[0;31m\]"
RED_H="\[\e[1;31m\]"

GREEN="\[\e[0;32m\]"
GREEN_H="\[\e[1;32m\]"

WHITE="\[\e[0;37m\]"
WHITE_H="\[\e[1;37m\]"

# ===================================================
# prompt
# ===================================================
# export PS1="[${RED_H}\u${RESET}@${GREEN_H}\H${RESET}:${WHITE}\w${RESET}>"
. ~/git-prompt.sh
export PS1="[${RED_H}\u${RESET}@${GREEN_H}\H${RESET}:${WHITE}\w${RESET}"'$(__git_ps1)>'

# ===================================================
# alias
# ===================================================
alias l='ls -l'
alias ll='ls -al'
alias lt='ls -alrt'

# ack, better than grep
alias Ac='ack'
alias ac='ack -i'

alias c='clear'
alias cl='clear ; ls -l'

# cd() { builtin cd "$@"; ll; }               # Always list directory contents upon 'cd'

alias ..='cd ../'
alias ...='cd ../../'
alias ....='cd ../../../'
alias .3='cd ../../../'                     # Go back 3 directory levels
alias .4='cd ../../../../'                  # Go back 4 directory levels
alias .5='cd ../../../../../'               # Go back 5 directory levels
alias .6='cd ../../../../../../'            # Go back 6 directory levels

alias v='vim'
alias les='less -i -f -R'

alias his='history'

alias kk='kill'
alias kkk='kill -9'

# ===================================================
# function
# ===================================================
#   extract:  Extract most know archives with one command
#   ---------------------------------------------------------
extract () {
  if [ -f $1 ] ; then
    case $1 in
      *.tar.bz2)   tar xjf $1     ;;
      *.tar.gz)    tar xzf $1     ;;
      *.bz2)       bunzip2 $1     ;;
      *.rar)       unrar e $1     ;;
      *.gz)        gunzip $1      ;;
      *.tar)       tar xf $1      ;;
      *.tbz2)      tar xjf $1     ;;
      *.tgz)       tar xzf $1     ;;
      *.zip)       unzip $1       ;;
      *.Z)         uncompress $1  ;;
      *.7z)        7z x $1        ;;
      *)     echo "'$1' cannot be extracted via extract(),  please run : extract 'file'" ;;
    esac
  else
    echo "'$1' is not a valid file, please run : extract 'file'"
  fi
}

# ----------------
# --- find file/dir/link, follow symbolic link or not
function find_base() { find $@
}
function ff() { find_base $@ -type f
}
function fff() { ff $@ -follow
}
function fd() { find_base $@ -type d
}
function fdf() { fd $@ -follow
}
function fl() { find_base $@ -type l
}
function flf() { fl $@ -follow
}

# ----------------
function dird() { if [ $# -ne 2 ]
  then
    echo "ERROR : must provide 2 parameters"
  else
    diff -qr $1 $2 | sort | grep "/CVS: |/CVS/|/\.git/" $GREP_PARAM -v | sed "s/^Files \(.\+\) and \(.\+\) differ$/vimdiff \1 \2/" | sed "s/^Only in \(.\+\): \(.\+\)$/\1\/\2 # single/"
  fi
}

# ----------------
# --- find file/dir/link, follow symbolic link or not
# Functions to help us manage paths.  Second argument is the name of the
# path variable to be modified (default: PATH)
pathremove () {
        local IFS=':'
        local NEWPATH
        local DIR
        local PATHVARIABLE=${2:-PATH}
        for DIR in ${!PATHVARIABLE} ; do
                if [ "$DIR" != "$1" ] ; then
                  NEWPATH=${NEWPATH:+$NEWPATH:}$DIR
                fi
        done
        export $PATHVARIABLE="$NEWPATH"
}

pathprepend () {
        pathremove $1 $2
        local PATHVARIABLE=${2:-PATH}
        export $PATHVARIABLE="$1${!PATHVARIABLE:+:${!PATHVARIABLE}}"
}

pathappend () {
        pathremove $1 $2
        local PATHVARIABLE=${2:-PATH}
        export $PATHVARIABLE="${!PATHVARIABLE:+${!PATHVARIABLE}:}$1"
}

export -f pathremove pathprepend pathappend


# ===================================================
# setting
# ===================================================

# ubnutu
bind '"\e[1;3D": backward-word' ### Alt left
bind '"\e[1;3C": forward-word'  ### Alt right


# ===================================================
# notes
# ===================================================

# --------------------------
## git compare with vimdiff, use 'git d' to diff file with vimdiff, input 'qa' (quit all files) to next file
# git config --global diff.tool vimdiff  
# git config --global difftool.prompt false  
# git config --global alias.d difftool  


# ===================================================
# 
# ===================================================


# exit

#
# change permission
# hence we can write the disk
# /sbin/fsck -fy
# /sbin/mount -uw /


# chmod -R 755 mach_kernel
# chown -R root:wheel mach_kernel

# chmod -R 755 /System/Library/Extensions/
# chown -R root:wheel /System/Library/Extensions/
# rm -rf /System/Library/Caches/*



