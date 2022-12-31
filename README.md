# Burpsuite Pro
Burpsuite Pro jar and updater script

## Installing
1. Make sure you have the latest updates - `sudo apt-get update -y && sudo apt-get upgrade -y`
2. Install the required libraries - `pip3 install -r requirements.txt`
3. Check your java version - `java --version` if the installed JDK version is below 17 update java with `sudo apt install openjdk-17-jdk`
1. Make the startup script executable `cmod +x ./start.sh`

## Activating Burp
1. `./start.sh`
2. `cd burpsuite_pro; java -jar burploader.jar`
3. Follow the video [link](https://www.youtube.com/watch?v=e9u6myyve4g&ab_channel=AseelPSathar)

## Usage
Run `start.sh` file to start burpsuite.

**Updates will run automaticly on each start**

You can create a symlink to the __start.sh__ script so you could run burp from any location by writing
`sudo ln -s [Path to Burp]/start.sh /usr/bin/burp`

Enjoy!
