#!/bin/bash

####
# Copyright (c) 2011, 
#   Florian Sowade <f.sowade@r9e.de>, 
#   Jakob Westhoff <jakob@westhoffswelt.de>
# 
# All rights reserved.
# 
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
# 
#  - Redistributions of source code must retain the above copyright notice, this
#    list of conditions and the following disclaimer.
#  - Redistributions in binary form must reproduce the above copyright notice,
#    this list of conditions and the following disclaimer in the documentation
#    and/or other materials provided with the distribution.
# 
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
# ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
# FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
# DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
# SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
# OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
####

echo "256colors (c) 2011 Florian Sowade, Jakob Westhoff"

usage() {
    cat <<EOF
Usage: $0 <action> [options ...]

Actions:

  grid [colors per row] [skipped start colors]

    Print a grid of all terminal colors in the given format.
    A line break is printed after the given amount of colors has been outputted.
    An arbitrary amount of colors may be skipped at the start of the table.
    Both arguments are optional. By default 6 colors per line are printed, while
    the first 16 colors are skipped

  calculate <r> <g> <b>
    
    Calculate the best match for the given rgb color (0-255)

EOF
}

mapToRange() {
    local scale=$1
    local end=$2
    local value=$3

    echo "scale=6; ${value}*${end}/${scale}"|bc|xargs printf "%.0f"
}

rgbToColorCode() {
    local r=$1
    local g=$2
    local b=$3
    
    # Scale to 0-23 to try grayscale ramp matching
    local greyR=$(mapToRange 255 24 $r)
    local greyG=$(mapToRange 255 24 $g)
    local greyB=$(mapToRange 255 24 $b)

    # Scaling to do some rgb matching
    local colorR=$(mapToRange 255 5 $r)
    local colorG=$(mapToRange 255 5 $g)
    local colorB=$(mapToRange 255 5 $b)
    
    local colorCode=-1

    if [ $greyR -eq $greyG ] && [ $greyG -eq $greyB ]; then
        # Map into greyscale ramp
        if [ $greyR -eq 24 ]; then
            # Special handling for white color
            colorCode=231
        else
            colorCode=$(echo "scale=0; 232 + $greyR"|bc)
        fi
    else
        # Map into color mix
        colorCode=$(echo "scale=0; 16 + $colorB + 6*$colorG + 36*$colorR"|bc)
    fi

    echo $colorCode
}

action-grid() {
    if [ $# -ge 1 ]; then
        WIDTH=$1
    else
        WIDTH=6
    fi

    if [ $# -ge 2 ]; then
        SKIP=$2
    else
        SKIP=16
    fi

    let colors=256-SKIP

    let rows=colors/WIDTH-1

    for i in $(seq 0 $rows); do
        let start=i*WIDTH
        let end=start+WIDTH-1
        for j in $(seq $start $end); do
            let color=SKIP+j
            echo -en "\033[48;05;${color}m  "
            printf "%3d" $color
            echo -en "  \033[0m"
        done
        echo ""
    done;
}

action-calculate() {
    local colorCode=$(rgbToColorCode "$1" "$2" "$3")
    
    echo "The ansi color code mostly matching your color (r: $1, b: $2, g: $3) is $colorCode"
    echo -en "\033[0m\033[38;5;${colorCode}mForeground example "
    echo -n "(\\033[38;5;${colorCode}m)"
    echo -en "\033[0m \033[38;5;232;48;5;${colorCode}m Background example "
    echo -n "(\\033[48;5;${colorCode}m)"
    echo -e "\033[0m"
}
        

if [ $# -lt 1 ] || [ "$1" == "-h" ]; then
    usage
    exit 1
fi

action=$1
shift 1

case "$action" in
    grid)
        action-grid "$@"
    ;;
    calculate)
        if [ $# -lt 3 ]; then
            echo ""
            echo "Calculate needs at least three parameters <r>, <g> and <b>"
            echo ""
            usage
            exit 1
        fi

        action-calculate "$@"
    ;;
    *)
        usage
        exit 1
esac
