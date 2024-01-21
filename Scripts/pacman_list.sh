#!/usr/bin/env bash

pacman -Qqen > /home/yusuf/.cache/pkglist.txt
scp /home/yusuf/.cache/pkglist.txt yusuf@192.168.1.143:/home/yusuf/pkg_lists/yusufs_lenovo_list.txt
