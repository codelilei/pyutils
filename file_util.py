# coding:utf-8

'''
A series of functions related to file operation
'''

import os
import sys
import re
import shutil
import subprocess
import time
import datetime


def get_list(path, suf):
    """Return files list under given directory."""
    if not os.path.exists(path):
        print(path + "not found")
        return []
    files = os.listdir(path)
    # files = [os.path.join(path, file) for file in files]
    # return filter(lambda file: file.endswith(suf) and os.path.isfile(file), files)
    files = [os.path.join(path, file)
             for file in files if file.endswith(suf) and os.path.isfile(file)]
    return files


def get_files_size(file_path, size=0):
    """Accumulate file size recursively"""
    if (os.path.isfile(file_path)):
        size = os.path.getsize(file_path)
    else:
        for root, dirs, files in os.walk(file_path):
            for f in files:
                # print(f)
                size += os.path.getsize(os.path.join(root, f))
            for d in dirs:
                get_files_size(os.path.join(root, d), size)
    return size


def del_files(path, pattern):
    """Delete files mathing the given regular pattern."""
    zipfiles = get_list(path, "zip")
    for f in zipfiles:
        if pattern.search(f):
            print('**{}** going to be deleted'.format(f))
            os.remove(f)


def rdel_empty(path, level=0, max_level=1):
    """Delete empty directories and files recursively."""
    if level > max_level:
        return
    lists = os.listdir(path)
    if not lists:
        shutil.rmtree(path)
        return
    for item in lists:
        path_full = os.path.join(path, item)
        if os.path.isdir(path_full):
            del_empty(path_full, level+1, max_level)
        elif os.path.isfile(path_full):
            if os.path.getsize(path_full) == 0:
                os.remove(path_full)


def rcopy_files(src, dst, suf=None):
    if not os.path.exists(dst):
        os.makedirs(dst)
    names = os.listdir(src)
    for name in names:
        srcname = os.path.join(src, name)
        dstname = os.path.join(dst, name)
        if os.path.isfile(srcname):
            if suf is not None:
                if not name.endswith(suf):
                    continue
            shutil.copy2(srcname, dstname)
        elif os.path.isdir(srcname):
            rcopy_files(srcname, dst, suf)


def rcopy_tree(src, dst, suf=None):
    if not os.path.exists(dst):
        os.makedirs(dst)
    names = os.listdir(src)
    for name in names:
        srcname = os.path.join(src, name)
        dstname = os.path.join(dst, name)
        if os.path.isfile(srcname):
            if suf is not None:
                if not name.endswith(suf):
                    continue
            shutil.copy2(srcname, dstname)
        elif os.path.isdir(srcname):
            rcopy_files(srcname, dstname, suf)
        # shutil.copystat(src, dst)


def zip_file(zip_name, zip_dir):
    """Create zip by HaoZip"""
    cmd_str = '"D:\\Program Files\\2345Soft\\HaoZip\\HaoZipC.exe" a -tzip '
    cmd_str += '{} {}{}* -r'.format(zip_name, zip_dir, os.sep)
    print(cmd_str)
    # os.system(cmd_str)
    # exec_ret = os.popen(cmd_str)
    # print(exec_ret.read())
    proc = subprocess.Popen(cmd_str, shell=True, stdout=subprocess.PIPE)
    proc.wait()
    if proc.returncode != 0:
        print("subprocess Error.")


def unzip_file(zip_name, unzip_dir):
    """Unzip file by HaoZip"""
    if not os.path.exists(unzip_dir):
        os.makedirs(unzip_dir)
    cmd_str = '"D:/Program Files/2345Soft/HaoZip/HaoZipC.exe" x -y -o' + unzip_dir + " " + f
    print(cmd_str)
    # os.system(cmd_str)
    # exec_ret = os.popen(cmd_str)
    # print(exec_ret.read())
    proc = subprocess.Popen(cmd_str, shell=True, stdout=subprocess.PIPE)
    proc.wait()
    if proc.returncode != 0:
        print("subprocess Error.")


'''
total_size = 0
# wrong, os.walk is recursive itself
for rt, dirs, files in os.walk(root):
    for f in files:
        fname = os.path.join(rt, f)
        print(fname.decode('gbk'))
        print(os.path.getsize(fname))
        total_size += os.path.getsize(fname)
        print('#' * 10)
    print(rt)
    print(dirs)
    print(files)
    print("#####################")
print(total_size)
'''


if __name__ == '__main__':
    print(get_files_size('E:/Py'))
