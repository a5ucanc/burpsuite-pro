#!/bin/bash

SOURCE=${BASH_SOURCE[0]}
while [ -L "$SOURCE" ]; do # resolve $SOURCE until the file is no longer a symlink
  DIR=$( cd -P "$( dirname "$SOURCE" )" >/dev/null 2>&1 && pwd )
  SOURCE=$(readlink "$SOURCE")
  [[ $SOURCE != /* ]] && SOURCE=$DIR/$SOURCE # if $SOURCE was a relative symlink, we need to resolve it relative to the path where the symlink file was located
done
DIR=$( cd -P "$( dirname "$SOURCE" )" >/dev/null 2>&1 && pwd )

cd $DIR
terms=($TERMINAL x-terminal-emulator urxvt rxvt termit terminator gnome-terminal konsole xterm)  
for t in ${terms[*]}
do
    if [ $(command -v $t) ]
    then
        detected_term=$t
        break
    fi
done
# Currently buggy
$detected_term -e python3 burp_updater.py

cd $(ls | grep burpsuite)

loader=$(ls | grep oader)
burp=$(ls | grep burpsuite)

java -javaagent:$loader -noverify -jar $burp &> /dev/null &
