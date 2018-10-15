# coding: utf-8

'''
fix html files attacked by vbs script virus
'''

import os
import re
import codecs


def get_vbs_pattern():
    reg = r'''<SCRIPT Language=VBScript><!--\nDropFileName = "svchost.exe"\n'''
    vbscode_pat = re.compile(reg, re.M)
    return vbscode_pat


def fix_vbs_file(file_name):
    vbs_pat = get_vbs_pattern()
    with codecs.open(file_name, 'r+', 'utf8') as f:
        content = f.read()
        rst = vbs_pat.search(content)
        if rst:
            pos = rst.start()
            # print(pos)
            f.seek(pos)
            f.truncate()


if __name__ == '__main__':
    fix_vbs_file('test.html')
