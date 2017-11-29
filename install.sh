#!/bin/bash

read -p "ENTER FULL DEVICE PATH:" DEVICE
read -p "ENTER FULL IMAGE PATH:" IMAGE
PART1="${DEVICE}p1"
PART2="${DEVICE}p2"

pause(){
    printf "\n"
    printf "$1\n"
    read -p "press [Enter] to continue, CTRL-C to abort" key
    printf "\n"
}

checkDevice(){
    if [ "$1" == "" -o "$(df -h --output=source | grep "$DEVICE")" == "" ]; then
        printf "\ndevice '$1' does not exist\n"
        printf "> check SD card devices with 'df -h'\n"
        printf "> re-insert SD card if necessary\n"
        printf "> edit DEVICE= in script if necessary\n\n"
        exit 1
    fi
}


rootCheck(){
    if [ $(id -u) -ne 0 ]; then
        printf "\n"
        printf "script must be run as root\n"
        printf "> try 'sudo ./shrink'\n\n"
        exit 1
    fi
}

# if [ "$USER" == "" ]; then
#     printf "\n"
#     printf "user not set\n"
#     printf "> edit USER= in script\n\n"
#     exit 1
# fi

writeImage(){
    if [ true ]; then
        sudo umount $PART1 $PART2 && echo unmount ok || exit 1
        sudo dcfldd if=$IMAGE of=$DEVICE && echo image read ok || exit 1
        sudo sync
        echo "unmounted and image written to sd card"
        echo "remove sd card"
    fi
}

rootCheck
checkDevice $DEVICE
writeImage
