#!/usr/bin/env python
# -*- coding: utf-8 -*-

import urllib2
from bs4 import BeautifulSoup
import re

import YandexXMLSearch
import GoogleAPISearch
import FileUtils
import ErrTransl
import config


def getTextContent(a_str_url, a_html_soup, a_arr_str_text_tags):
    str_text = ""
    for url in a_arr_str_text_tags:
        if url in a_str_url:
            str_tag = a_arr_str_text_tags[url]['tag']
            str_args = a_arr_str_text_tags[url]['args']
            str_text = a_html_soup.find(str_tag, attrs=str_args)
            if str_text is not None:
                str_text = str_text.get_text()
                reg_exp_odd_char = re.compile("&.*?;")
                reg_exp_new_line1 = re.compile("\\n")
                reg_exp_new_line2 = re.compile("\\r")
                str_text = reg_exp_odd_char.sub(" ", str_text)
                str_text = reg_exp_new_line2.sub(' ', str_text)
                str_text = reg_exp_new_line1.sub(' ', str_text)
            else:
                str_text = ""
            break

    return unicode(str_text)


def collect_content_from_url(a_arr_data):
    for page in a_arr_data:
        req = urllib2.Request(page.m_strURL)
        urlResponsContent = None
        try:
            urlResponsContent = urllib2.urlopen(req).read()
        except urllib2.HTTPError as e:
            print "Error Code: " + e.code + "\nMsg: " + ErrTransl.responses[e.code]
            print "Additional Info: " + e.read()
            continue
        except urllib2.URLError as e:
            print e.reason
            continue

        soup = BeautifulSoup(urlResponsContent, 'lxml')
        # strResponsContent = soup.findAll(text=True)

        strFilePath = "data\\" + str(page.m_nID) + ".json"
        dataPage = FileUtils.getDataFromFile(strFilePath)
        dataPage = YandexXMLSearch.WebPage().deserialize(dataPage)

        strTextContentOnly = getTextContent(dataPage.m_strURL, soup, config.c_arr_str_Reliable_URL)

        dataPage.m_strContent = strTextContentOnly
        FileUtils.setData2File(dataPage.serialize(), strFilePath)


if __name__ == '__main__':
    # arrYandexResults = YandexXMLSearch.search_yandex("питон")
    # if len(arrYandexResults) == 0:
    #     print "Error: Result list is empty."
    #     exit(0)
    # print "Search result: " + str(len(arrYandexResults)) + " web pages"
    # for result in arrYandexResults:
    #     FileUtils.setData2File(result.serialize(), "data\\Yandex\\" + str(result.m_nID) + ".json")
    # collect_content_from_url(arrYandexResults)

    arrGoogleResults = GoogleAPISearch.search_google("питон")
    if len(arrGoogleResults) == 0:
        print "Error: Result list is empty."
        exit(0)
    print "Search result: " + str(len(arrGoogleResults)) + " web pages"
    for result in arrGoogleResults:
        FileUtils.setData2File(result.serialize(), "data\\" + str(result.m_nID) + ".json")
    collect_content_from_url(arrGoogleResults)
