#!/usr/bin/env python
# -*- coding: utf-8 -*-

import urllib
import urllib2
from datetime import datetime
#   from BeautifulSoup import BeautifulStoneSoup
from bs4 import BeautifulSoup

# from multiprocessing import Process, ProcessError
# import time as timer
# import sys

import config
import FileUtils

c_strYandexUserID = "lyilyidgivampa"
c_strYandexAPIKey = "03.371325562:c6780f3cc5898ffedf90a50ee65d84f6"

c_strRequestTemplate = """<?xml version="1.0" encoding="UTF-8"?>
                                  <request>
                                        <query> %s </query>
                                        <groupings>
                                            <groupby attr="d"
                                                mode="deep"
                                                groups-on-page="10"
                                                docs-in-group="1" />
                                        </groupings>
                                        <page> %s </page>
                                        <sortby>rlv</sortby>
                                    </request>"""


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


def search_yandex(a_str_query, a_n_start_page=0, a_n_end_page=5):
    arrResults = []
    mapSearchLoginParams = {'user': c_strYandexUserID,
                            'key': c_strYandexAPIKey,
                            'site': "wikipedia.org,habrahabr.ru",
                            'lang': config.__LANG__}
    strSearchUrl = 'https://yandex.com/search/xml?' + urllib.urlencode(mapSearchLoginParams)

    for nPageNum in range(a_n_start_page, a_n_end_page):
        post_data = c_strRequestTemplate % (a_str_query, str(nPageNum))
        urlRequest = urllib2.Request(strSearchUrl, post_data)
        urlResponse = None
        try:
            urlResponse = urllib2.urlopen(urlRequest)
        except Exception as e:
            print "Error : Reload Yandex.XML service. Msg: "
            print(type(e))
            exit(1)
        urlAnswer = urlResponse.read()

        xmlResult = BeautifulSoup(''.join(urlAnswer), "lxml-xml")
        if xmlResult.find('group') is None:
            print BeautifulSoup(''.join(xmlResult.find('error')), "lxml-xml").prettify()
            exit(0)

        nGroupIndex = 1  # index in search list

        for node in xmlResult('group'):  # xmlResult.getElementsByTagName('group'):
            item = WebPage()
            item.m_nID = nGroupIndex + nPageNum * 10

            item.m_strTitle = getElemFromNode('title', node)
            item.m_strHeadline = getElemFromNode('headline', node)
            item.m_strPassage = getElemFromNode('passage', node)
            item.m_dtLastModif = getProperTimeFormat('modtime', node)
            item.m_strURL = getElemFromNode('url', node)
            item.m_nCode = getElemFromNode('charset', node)
            item.m_nStatus = 200
            nGroupIndex += 1
            arrResults.append(item)

    return arrResults


def TestYandexSearch():
    # ts = timer.time()
    # p1 = Process(target=search_yandex, args =("Питон",0,5))
    # p2 = Process(target=search_yandex, args =("Питон",5,10))
    #
    # p1.start()
    # p2.start()
    #
    # p1.join()
    # p2.join()
    # te = timer.time()
    #
    # print "P : " + str(te - ts) + " y.e"

    arrYandexResults = search_yandex("Питон", 0, 10)

    if len(arrYandexResults) == 0:
        print "Error: Result list is empty."
        exit(0)
    print "Search result: " + str(len(arrYandexResults)) + " web pages"
    for result in arrYandexResults:
        FileUtils.setData2File(result.serialize(), "data\\" + str(result.m_nID) + ".json")
