# coding: utf-8

import os
import sys
import re
import random
import time
import glob


def list2file(pylist, savename):
    with open(savename, 'w', encoding='ansi') as fd:
        # fd.writelines('\n'.join(pylist))
        for l in pylist:
            if not l.strip():
                continue
            fd.write(l + '\n')


def file2list(file):
    pylist = []
    with open(file, encoding='ansi') as fd:
        for line in fd:
            line = line.strip()
            if not line:
                continue
            pylist.append(line)
    return pylist


def get_filelist(path, suf):
    if not os.path.exists(path):
        print(path + "not found")
        return []
    dirlist = os.listdir(path)
    # files = [os.path.join(path, file) for file in files]
    # return filter(lambda file: file.endswith(suf), files)
    files = []
    for f in dirlist:
        file = os.path.join(path, f)
        if file.endswith(suf) and os.path.isfile(file):
            files.append(f)
    return files


def merge_datalist(path_pattern, merge_name):
    filelist = glob.glob(path_pattern)
    mergename = merge_name
    if os.path.split(merge_name)[0] == '':
        mergename = os.path.join(os.path.split(path_pattern)[0], merge_name)
    mergefile = open(mergename, 'w', encoding='ansi')
    for file in filelist:
        for line in open(file, 'r', encoding='ansi'):
            mergefile.write(line)
    mergefile.close()


def shuffle_datalist(file):
    root, ext = os.path.splitext(file)
    shufflefile = root + '_shuffle' + ext
    datalist = file2list(file)
    random.shuffle(datalist)
    list2file(datalist, shufflefile)


def proc_datalist(file, train_ratio=None, insert='', append='', label_func=None):
    datalist = []
    with open(file, encoding='ansi') as fd:
        for line in fd:
            if not line.strip():
                continue
            imname, label = line.split()
            if label_func:
                label = label_func(label)
            line_new = '{}{} {}{}'.format(insert, imname, label, append)
            datalist.append(line_new)
    random.shuffle(datalist)
    root, ext = os.path.splitext(file)
    if train_ratio:
        file_train = root + '_train' + ext
        file_test = root + '_test' + ext
        train_num = len(datalist) * train_ratio
        with open(file_train, 'w', encoding='ansi') as fd1, open(file_test, 'w', encoding='ansi') as fd2:
            for i, l in enumerate(datalist):
                if i < train_num:
                    fd1.write(l + '\n')
                else:
                    fd2.write(l + '\n')
        return
    file_new = root + '_proc' + ext
    list2file(datalist, file_new)


def label_func100(x):
    return str(round(float(x)*100))


def extract_label(file, insert='', append=''):
    root, ext = os.path.splitext(file)
    file_new = root + '-withlabel' + ext
    print(file_new)
    with open(file, encoding='ansi') as fd, open(file_new, 'w', encoding='ansi') as fd2:
        for line in fd:
            line = line.strip()
            if len(line) < 1:
                continue
            label, name = line.split()[0].split('_')
            fd2.write('{}{}{} {}\n'.format(insert, name, append, label))


if __name__ == '__main__':
    proc_datalist('AFLW_LFW-score.txt', 0.8, 'AFLW_LFW-norm/', label_func=label_func100)
