#!/usr/bin/env python
# -*- coding: utf-8 -*-

import urllib
import urllib2
from datetime import datetime
import json

# from multiprocessing import Process, ProcessError
# import time as timer
# import sys

import config
import FileUtils

c_strGoogleAPIKey = "AIzaSyCEQNDx0ndYWaM1OQUJa1JHiH0T6s0c_AA"
c_strGoogleCXID = "010331623033688513243:ihg0adtocfg"

c_strRequestTemplate = "https://www.googleapis.com/customsearch/v1?"


class WebPage(object):
    def __init__(self):
        self.m_nID = 0
        self.m_strTitle = ""
        self.m_strHeadline = ""
        self.m_strPassage = ""
        self.m_strURL = ""
        self.m_strContent = ""
        self.m_dtLastModif = datetime.now()
        self.m_nCode = 200
        self.m_nStatus = 200

    def serialize(self):
        temp_dict = {
            'ID': self.m_nID,
            'Title': self.m_strTitle,
            'Headline': self.m_strHeadline,
            'Passage': self.m_strPassage,
            'URL': self.m_strURL,
            'Content': self.m_strContent,
            'LastModif': self.m_dtLastModif.isoformat(),
            'Code': self.m_nCode,
            'Status': self.m_nStatus}
        return temp_dict

    @staticmethod
    def deserialize(a_dict):
        tempObj = WebPage()
        tempObj.m_nID = a_dict['ID']
        tempObj.m_strTitle = a_dict['Title']
        tempObj.m_strHeadline = a_dict['Headline']
        tempObj.m_strPassage = a_dict['Passage']
        tempObj.m_strURL = a_dict['URL']
        tempObj.m_strContent = a_dict['Content']
        dt = datetime.strptime(a_dict['LastModif'], "%Y-%m-%dT%H:%M:%S.%f")
        tempObj.m_dtLastModif = dt
        tempObj.m_nCode = a_dict['Code']
        tempObj.m_nStatus = a_dict['Status']
        return tempObj


def getElemFromNode(astrElemTagName, aNode):
    # noinspection PyBroadException
    try:
        dataTemp_ = aNode.find(astrElemTagName)
        dataTemp = dataTemp_.get_text()
        # dataTemp = dataTemp # .encode('utf-8','ignore')
    except Exception as e:
        #   print type(exc)  # the exception instance
        #   print exc  # __str__ allows args to be printed directly
        return ""
    return dataTemp


def getProperTimeFormat(astrElemTagName, aNode):
    # <год><месяц><день>Т<час><минута><секунда>
    strOldFormat = aNode.find(astrElemTagName)
    strOldFormat = strOldFormat.contents[0]
    dtNewFormat = datetime.now()
    dtNewFormat = dtNewFormat.replace(
        year=int(strOldFormat[0:4]),
        month=int(strOldFormat[4:6]),
        day=int(strOldFormat[6:8]),
        hour=int(strOldFormat[9:11]),
        minute=int(strOldFormat[11:13]))
    return dtNewFormat


def search_google(a_str_query, a_n_start_page=0, a_n_end_page=5):
    arrResults = []
    mapSearchLoginParams = {'cx': c_strGoogleCXID,
                        'key': c_strGoogleAPIKey,
                        'q': a_str_query,
                        'lr': "lang_" + config.__LANG__}
    strSearchUrl = c_strRequestTemplate + urllib.urlencode(mapSearchLoginParams)

    urlRequest = urllib2.Request(strSearchUrl)
    urlResponse = None
    try:
        urlResponse = urllib2.urlopen(urlRequest)
    except Exception as e:
        print "Error : Google API request failed. Msg: "
        print(type(e))
        exit(1)
    urlAnswer = urlResponse.read()

    a_data = json.loads(urlAnswer)
    nPageNum = 0
    nIndex = 1
    for node in a_data['items']:
        item = WebPage()
        item.m_nID = nIndex + nPageNum * 10

        item.m_strTitle = node['title']
        item.m_strHeadline = node['snippet']
        item.m_strURL = node['link']
        item.m_nStatus = 200
        nIndex += 1
        arrResults.append(item)

    return arrResults


def TestGoogleSearch():
    arrGoogleResults = search_google("Питон", 0, 10)

    if len(arrGoogleResults) == 0:
        print "Error: Result list is empty."
        exit(0)
    print "Search result: " + str(len(arrGoogleResults)) + " web pages"
    for result in arrGoogleResults:
        FileUtils.setData2File(result.serialize(), "data\\" + str(result.m_nID) + ".json")
