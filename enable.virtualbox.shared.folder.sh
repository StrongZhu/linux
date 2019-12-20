#!/bin/bash

# root cause : `whoami` is not in group 'vboxsf', which owns shared folder

# use below cmd to add `whoami` to the group

# reference : https://www.cnblogs.com/xia-weiwen/p/8215350.html
sudo usermod -aG vboxsf $(whoami)

# need reboot !



