# coding:utf-8

'''
invert and change clipboard slashes from '/' to '\\' or vice versa
Useful to quickly replace file path in code
'''

# pip3 install pywin32
import win32clipboard as w
import win32con


def get_clipboard():
    w.OpenClipboard()
    t = ''
    try:
        # t = w.GetClipboardData(win32con.CF_TEXT)
        t = w.GetClipboardData(win32con.CF_UNICODETEXT)
    except Exception as e:  # except Exception, e: #py2
        # print(e.args[0])
        print(e)
    w.CloseClipboard()
    # print(t)
    # return t.decode('gbk')
    # return t.decode('ascii')
    # return str(t, 'utf8')
    # return str(t)
    return t


def set_clipboard(strs):
    w.OpenClipboard()
    w.EmptyClipboard()
    # w.SetClipboardData(win32con.CF_TEXT, strs)
    w.SetClipboardData(win32con.CF_UNICODETEXT, strs)
    w.CloseClipboard()


def clear_clipboard():
    w.OpenClipboard()
    w.EmptyClipboard()
    w.CloseClipboard()


def inv_slash_to_clipboard():
    slash1 = '\\'
    slash2 = '/'
    s = get_clipboard().strip()
    # print('clipboard content： ', s)
    if s.find(slash2) >= 0:
        slash1, slash2 = slash2, slash1
    set_clipboard(s.replace(slash1, slash2))


if __name__ == '__main__':
    inv_slash_to_clipboard()
