#!/home/tops/bin/python
# -*- coding: utf-8 -*-
# Create Time: 2020/3/7 14:15
# Author: Riners
import sys

CORLOR_BLACK    = "\033[0;30m"
COLOR_RED       =   "\033[0;31m"
COLOR_GREEN     =   "\033[0;32m"
COLOR_YELLOW    =   "\033[0;33m"
COLOR_BLUE      =   "\033[0;34m"
COLOR_PUPPLE    =   "\033[0;35m"
COLOR_CYAN      =   "\033[0;36m"
COLOR_WHITE     =   "\033[0;37m"
COLOR_RESTORE   =   "\033[0m"

def colorPrint(msg, color = None):
    msg = color + msg + COLOR_RESTORE
    print msg
    sys.stdout.flush()
    # return


'''颜色打印测试代码'''
# colorPrint('hello colorful world!', color = CORLOR_BLACK)
# colorPrint('hello colorful world!', color = COLOR_RED)
# colorPrint('hello colorful world!', color = COLOR_GREEN)
# colorPrint('hello colorful world!', color = COLOR_YELLOW)
# colorPrint('hello colorful world!', color = COLOR_BLUE)
colorPrint('hello colorful world!', color = COLOR_PUPPLE)
# colorPrint('hello colorful world!', color = COLOR_CYAN)
# colorPrint('hello colorful world!', color = COLOR_WHITE)
# colorPrint('hello colorful world!', color = COLOR_RESTORE)
