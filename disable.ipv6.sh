#!/bin/bash

# * when you 
# ping www.baidu.com
# maybe get a IPv6 address. cannot ping it successfully

# must disable IPv6

# * reference : https://ywnz.com/linuxjc/5099.html

echo ______________________________________
ip a
echo ______________________________________

# run below cmd
echo ______________________________________
sudo sysctl -w net.ipv6.conf.all.disable_ipv6=1
sudo sysctl -w net.ipv6.conf.default.disable_ipv6=1
sudo sysctl -w net.ipv6.conf.lo.disable_ipv6=1

# check
echo ______________________________________
ip a
echo ______________________________________


echo DONE~~~
echo ______________________________________



