# -*- coding:utf-8 -*-
# ---------------------------
# 说明：
#     系统函数
# ---------------------------

def DEBUG_ERR(*args, **kwargs):
    if 1:
        print args
    else:
        raise Exception, str(args)