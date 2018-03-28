#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import codecs
import os.path as f
import errno
import json


def createFile(a_str_path):
    if not os.path.exists(os.path.dirname(a_str_path)):
        try:
	    print "Path ",a_str_path
            os.makedirs(os.path.dirname(a_str_path))
        except OSError as exc:  # Guard against race condition
            if exc.errno != errno.EEXIST:
                raise

    return codecs.open(a_str_path, 'w', encoding='utf8')


def createDir(a_str_path):
    try:
        os.makedirs(a_str_path)
    except OSError as e:
        if e.errno != errno.EEXIST:
            raise
    return


def isFile(a_str_path):
    return f.isfile(a_str_path)


def isDir(a_str_path):
    return f.isdir(a_str_path)


def saveFile(a_file):
    return a_file.close()


def openFile(a_str_path, mode='w'):
    return codecs.open(a_str_path, mode, encoding='utf8')


def isExistFile(a_str_path):
    return f.exists(a_str_path) and f.isfile(a_str_path)


def isExistDir(a_str_path):
    return f.exists(a_str_path) and f.isdir(a_str_path)


def delFile(a_str_path):
    return os.remove(a_str_path)


def delDir(a_str_path):
    for root, directories, filenames in os.walk(a_str_path):
        for directory in directories:
            str_full_path = f.join(root, directory)
            print str_full_path
            delDir(str_full_path)
        for filename in filenames:
            str_full_path = f.join(root, filename)
            print str_full_path
            delDir(str_full_path)
    print a_str_path
    if isDir(a_str_path):
        os.removedirs(a_str_path)
    elif isFile(a_str_path):
        os.remove(a_str_path)


def setData2File(a_data, a_str_path, a_f_pretty=True):
    if a_data is None or a_str_path == "":
        return -13
    fin = createFile(a_str_path)
    if fin is not None:
        json.dump(a_data, fin, ensure_ascii=False, indent=4)
        return fin.close()
    return -12


def getDataFromFile(a_str_path):
    if a_str_path == "":
        return -13
    fout = openFile(a_str_path, 'r')
    a_data = None
    if fout is not None:
        a_data = json.load(fout)
        fout.close()
        return a_data
    return None
