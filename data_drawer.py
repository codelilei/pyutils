# encoding: utf-8

'''
Draw chart for both multi data lists and single list.
Supported types: line, hist, pie.
'''

import os
import sys
# import time
from collections import Counter
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.mlab as mlab
from matplotlib.ticker import MultipleLocator


class DataReader:
    def __init__(self, path=None):
        self.path = path

    def get_list(self):
        """
        If path is an directry, return all file lists under it.
        If path is file, return itself.
        """
        if not os.path.exists(self.path):
            # print(self.path + "not found")
            return []
        if os.path.isfile(self.path):
            return [self.path]
        files = os.listdir(self.path)
        files = [os.path.join(self.path, file) for file in files]
        # return filter(lambda file: file.endswith("txt") and os.path.isfile(file), files)
        return list(filter(lambda file: file.endswith("txt") and os.path.isfile(file), files))

    def load_data(self, txt_file):
        scores = []
        with open(txt_file) as f:
            for line in f:
                scores.append(int(line.strip()))
        return scores

    def load_data_np(self, txt_file, delimiter=None, usecols=None):
        # return np.loadtxt(txt_file, dtype=dtype, delimiter=delimiter)
        return np.loadtxt(txt_file, delimiter=delimiter, usecols=usecols, ndmin=1)


class DataDrawer:
    def __init__(self, xlabel, ylabel, title, subplot=False):
        if not subplot:
            self.ax = plt.gca()
        # self.fig = plt.figure()
        self.xlabel = xlabel
        self.ylabel = ylabel
        self.title = title

    def add_data_curve(self, data, label, hist=True):
        """
        Draw line chart.
        Args:
            data: Input text data.
            label: Input label.
            hist: Draw sorted hist if true and simple line chart in raw data order if false.
        """
        # t1 = time.clock()
        # cnt = dict(zip(*np.unique(data, return_counts=True)))
        # # cnt = Counter(data)
        # print(time.clock() - t1)
        # s_cnt = sorted(cnt.items())
        # value = [it[0] for it in s_cnt]
        # freq =  [it[1] for it in s_cnt]
        if hist:
            u = np.unique(data, return_counts=True)
            value, freq = u[0], u[1]
            self.ax.plot(value, freq, label=label)
            # n, bins, patches = self.ax.hist(data, bins=10, label=label)
            # self.ax.plot(bins, patches, 'r--')
        elif data.ndim == 1:
            self.ax.scatter(label, data, label=label)
            # self.ax.plot(data, label=label)
        elif data.ndim == 2:
            self.ax.plot(data[:, 0], data[:, 1], label=label)

        self.ax.set_xlabel(self.xlabel)
        self.ax.set_ylabel(self.ylabel)
        self.ax.set_title(self.title)
        self.ax.legend(loc='best', ncol=1)

    def add_data_pie(self, data, subtitle, plotpos, number=11):
        """
        Draw pie chart.
        Args:
            subtitle: Subtitle for each subplot image.
            plotpos: Specify where to put the subplot.
            number: Tell the number of intervals to be divided.
                e.g. Data ranges from 0 to 100, number is 2,
                such case will divide data into 0-50 and 50-100.
        """
        u = np.unique(data, return_counts=True)
        value, freq = u[0], u[1]
        min_val, max_val = np.min(value), np.max(value)
        # print('min_val'.center(30, '='), min_val)
        # print('max_val'.center(30, '='), max_val)
        interval = float(max_val - min_val) / float(number)
        # print('interval'.center(30, '='), interval)
        xs = [0] * number
        for v, f in zip(*u):
            xs[min(int((v - min_val) / interval), number - 1)] += f
        ls = ['%d-%d' % (round(min_val + i * interval), round(min_val + (i + 1) * interval)) for i in range(number)]
        explode = [0] * number
        explode[xs.index(max(xs))] = 0.05
        explode[xs.index(min(xs))] = 0.05
        # print(xs, ls)

        # ax = self.fig.add_subplot(plotpos)
        ax = plt.subplot(plotpos)
        ax.pie(xs, labels=ls, explode=tuple(explode), autopct='%3.1f%%', shadow=True, startangle=90, pctdistance=0.7)
        ax.set_title(subtitle)
        ax.axis('equal')
        ax.legend(loc='best', ncol=1)
        plt.suptitle(self.title)

    def show_figure(self):
        # self.ax.xaxis.set_major_locator(MultipleLocator(1))
        plt.show()

    def clear_figure(self):
        plt.clf()

    def save_figure(self, pic_name='distribution', dpi=180):
        plt.savefig(pic_name, dpi=dpi)


def get_label(fname):
    fname = fname.replace('\\', '/')
    slash = fname.rfind('/')
    dot = fname.rfind('.')
    if dot < 0:
        dot = None
    return fname[slash + 1:dot]


def draw_chart(path, xlabel=None, ylabel=None, title=None, hist=True, usecols=None, pie=False, plotpos=None):
    """
        Draw line chart.
        Args:
            path: Either directory or file.
            hist: Draw sorted hist if true and simple line chart in raw data order if false.
            usecols: See numpy.loadtxt usecols.
            plotpos: Specify where to put the subplot.
            pie: Draw pie chart if true. Note that this will try to draw multi subplots in square shape.
    """
    drawer = DataDrawer(xlabel, ylabel, title, subplot=pie)
    reader = DataReader(path)
    files = reader.get_list()
    # files = files[::-1]
    # print files
    # file_num = len(list(files))
    file_num = len(files)
    if file_num < 1:
        print('No file found, exit now')
        return
    if pie:
        import math
        n = math.ceil(math.sqrt(file_num))
        for idx, file in enumerate(files):
            cur_pos = plotpos * 10 + idx + 1 if plotpos else n * 110 + idx + 1
            data = reader.load_data_np(file, usecols=usecols)
            drawer.add_data_pie(data, get_label(file), plotpos=cur_pos)
    else:
        for file in files:
            data = reader.load_data_np(file, usecols=usecols)
            drawer.add_data_curve(data, get_label(file), hist=hist)

    drawer.save_figure('figures/' + title)
    drawer.show_figure()
    drawer.clear_figure()


if __name__ == '__main__':
    plt.rcParams['font.sans-serif'] = ['SimHei']
    plt.rcParams['axes.unicode_minus'] = False

    # path_root = u'scores/'
    # path_root = unicode(path_root, 'utf-8') #py2

    # path_root = u'D:/Projects/err_cmp/'
    # draw_chart(path_root, "folder_idx", "err_avg", "err_cmp", False, usecols=(0,3))

    # path_root = u'loss/'
    # draw_chart(path_root, "loss", "frequency", "test_set_loss", False)

    draw_chart('D:/Projects/data_pair', usecols=(1,), title="data distribution")
    # draw_chart('D:/Projects/data_pair', usecols=(1,), title="data portion", pie=True)
    # draw_chart('pie', title="test", pie=True, plotpos=12)
    # draw_chart('pie', title="test", pie=True)
    # draw_chart("D:/Projects/choice.txt", usecols=(1,), title="choice", pie=True)
