#!/usr/bin/env bash

pacman -Qqn > /home/yusuf/.cache/pkglist.txt
scp /home/yusuf/.cache/pkglist.txt yusuf@192.168.1.143:/home/yusuf/pkg_lists/yusufs_dell_list.txt
