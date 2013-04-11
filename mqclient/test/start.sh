#!/bin/sh
#通过nohup命令支持即使关闭当前窗口进程也依然会运行
nohup ./test_client.py >print.out &
