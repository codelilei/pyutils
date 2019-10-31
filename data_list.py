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
        last_line = ''
        for line in open(file, 'r', encoding='ansi'):
            if line.strip():
                print(line)
                mergefile.write(line)
                last_line = line
        if not last_line.endswith('\n'):
            mergefile.write('\n')
    mergefile.close()


def shuffle_datalist(file):
    root, ext = os.path.splitext(file)
    shufflefile = root + '_shuffle' + ext
    datalist = file2list(file)
    random.shuffle(datalist)
    list2file(datalist, shufflefile)


def proc_datalist(file, train_ratio=None, insert='', append='', label_func=None, pick_num=None, shuffle=True):
    datalist = []
    with open(file, encoding='ansi') as fd:
        for line in fd:
            if not line.strip():
                continue
            try:
                imname, label = line.split()
                label = ' ' + label
            except Exception as e:
                imname = line.strip()
                label = ''
            if label_func:
                label = label_func(label)
            line_new = '{}{}{}{}'.format(insert, imname, label, append)
            datalist.append(line_new)
    if shuffle:
        random.shuffle(datalist)
    if pick_num:
        datalist = datalist[:pick_num]
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


def filter_line(file, keep_word=None, exclude_word=None, ignore_case=False):
    if keep_word is None and exclude_word is None:
        return
    if ignore_case:
        keep_word = keep_word.lower()
        exclude_word = exclude_word.lower()
    root, ext = os.path.splitext(file)
    file_filter = root + '_filter' + ext
    with open(file, encoding='ansi') as fd, open(file_filter, 'w', encoding='ansi') as fd1:
        for line in fd:
            line = line.strip()
            if not line:
                continue
            line_tmp = line.lower() if ignore_case else line
            if keep_word and keep_word not in line_tmp:
                continue
            if exclude_word and exclude_word in line_tmp:
                continue
            fd1.write(line + '\n')


def split_pos_neg(list_path):
    path_pre = os.path.splitext(list_path)[0]
    # fdp = open('{}/{}_pos_neg.txt'.format(path_pre), 'w')
    fdp = open('{}_pos.txt'.format(path_pre), 'w')
    fdn = open('{}_neg.txt'.format(path_pre), 'w')
    for line in open(list_path):
        tmp = line.strip()
        # dir_name = tmp.split('/')[1]
        # dir_name_new = dir_name.replace(' ', '')
        # line_new = line.replace(dir_name, dir_name_new)
        # fdpn.write(line_new)
        if tmp.split()[-1] == '1':
            fdp.write(line)
        else:
            fdn.write(line)
    # fdpn.close()
    fdp.close()
    fdn.close()


def gen_list(root_folder, exts=None, keep_root=False, lamda_dir_level=None):
    root_folder = os.path.realpath(root_folder)
    parent_folder = os.path.abspath(os.path.join(root_folder, '..'))
    rt_name = os.path.basename(root_folder)
    fd = open('{}/{}_list.txt'.format(parent_folder, rt_name), 'w')
    for rt, d, f in os.walk(root_folder):
        if len(f) < 0:
            continue
        rel_path = os.path.relpath(rt, root_folder)
        dir_level = 0 if len(rt) == len(root_folder) else len(rel_path.split(os.sep))
        # print(rt, d, f, dir_level)
        if lamda_dir_level and not lamda_dir_level(dir_level):
            continue
        for fname in f:
            ext = os.path.splitext(fname)[-1]
            if not exts or (len(ext) > 0 and ext in exts):
                if dir_level == 0:
                    rel_path_new = fname
                else:
                    rel_path_new = rel_path.replace('\\', '/') + '/' + fname
                if keep_root:
                    rel_path_new = rt_name + '/' + rel_path_new
                fd.write(rel_path_new + '\n')
    fd.close()


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
    # split_pos_neg('D:/train_shuffle.txt')
    # gen_list('test_folder', '.jpg', False, lambda d: d > 0)
    # gen_list('E:/cellphone_imgs', ['.jpg', '.png'], keep_root=True)
