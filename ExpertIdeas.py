import xml.etree.ElementTree as ET
import requests
import urllib
import json
from datetime import datetime

def logInRequestToWikipedia(lgtoken, cookies):
    request = { 'action' : 'login' }
    request['format'] = 'xml'
    request['lgname'] = 'ExpertIdeasBot'
    request['lgpassword'] = '**********'
    if lgtoken != '':
        request['lgtoken'] = urllib.urlencode(lgtoken)
    request['Content-Type'] = 'application/x-www-form-urlencoded'
    url = 'https://en.wikipedia.org/w/api.php'
    headers = { 'User-Agent' : 'ExpertIdeasBot, developped by researchers at the University of Michigan, Carnegie Mellon University and the University of Pittsburgh' }
    headers['content-type'] = 'application/x-www-form-urlencoded'
    response = requests.post(url, data=json.dumps(request), headers=headers, cookies = cookies)
    tree = ElementTree.fromstring(response.content)
    root = tree.getroot()
    lgtoken = root[0].attrib['token']
    cookies = response.cookies
    result = root[0].attrib['result']
    if result == "NeedToken":
        return logInRequestToWikipedia(lgtoken, cookies)
    elif result == "Success":
        return lgtoken, cookies

def AddNewSectionToTalkPage(title, summary, text, lgtoken, cookies):
    request = { 'action' : 'edit' }
    request['format'] = 'xml'
    request['title'] = "Talk:" + title
    request['section'] = 'new'
    request['sectiontitle'] = summary
    request['summary'] = "Added a new section for " + summary
    request['text'] = text
    request['watchlist'] = 'watch'
    # request['basetimestamp'] = datetime().now().isoformat() + 'Z'
    while lgtoken == '' or cookies == ''
        lgtoken, cookies = logInRequestToWikipedia(lgtoken, cookies)
    request['token'] = lgtoken
    headers = { 'User-Agent' : 'ExpertIdeasBot bot, developped by researchers at the University of Michigan, Carnegie Mellon University and the University of Pittsburgh' }
    headers['content-type'] = 'application/x-www-form-urlencoded'
    url = 'http://en.wikipedia.org/w/api.php'
    response = requests.post(url, data=json.dumps(request), headers=headers, cookies = cookies)
    tree = ElementTree.fromstring(response.content)
    root = tree.getroot()
    lgtoken = root[0].attrib['token']
    cookies = response.cookies
    result = root[0].attrib['result']
    if result == "NeedToken":
        return AddNewSectionToTalkPage(title, summary, text, lgtoken, cookies)
    elif result == "Success":
        lgtoken, cookies = AddtoWatchlist(title, lgtoken, cookies)
        return lgtoken, cookies

def AddtoWatchlist(title, lgtoken, cookies):
    request = { 'action' : 'edit' }
    request['format'] = 'xml'
    request['title'] = title
    request['watchlist'] = 'watch'
    # request['basetimestamp'] = datetime().now().isoformat() + 'Z'
    while lgtoken == '' or cookies == ''
        lgtoken, cookies = logInRequestToWikipedia(lgtoken, cookies)
    request['token'] = lgtoken
    headers = { 'User-Agent' : 'ExpertIdeasBot bot, developped by researchers at the University of Michigan, Carnegie Mellon University and the University of Pittsburgh' }
    headers['content-type'] = 'application/x-www-form-urlencoded'
    url = 'http://en.wikipedia.org/w/api.php'
    response = requests.post(url, data=json.dumps(request), headers=headers, cookies = cookies)
    tree = ElementTree.fromstring(response.content)
    root = tree.getroot()
    lgtoken = root[0].attrib['token']
    cookies = response.cookies
    result = root[0].attrib['result']
    if result == "NeedToken":
        return AddtoWatchlist(title, lgtoken, cookies)
    elif result == "Success":
        return lgtoken, cookies

def postCommentstoTalkpages(scholarsList):
    for scholarName, scholarPublicationList, scholarComment in scholarsList:
        title = articleTitle
        summary = "'''Professor " + scholarName + "'s comment on this article'''"
        text = "\nProfessor " + scholarName + "has recently published the following research publications which are related to this Wikipedia article:\n"
        for publication in scholarPublicationList:
            text += "Reference 1: " + publication['name'] + " , Number of Ciations: " + publication['numberofCitations'] + "\n"
        text += "\nProfessor " + scholarName + "has reviewed this Wikipedia page, and provided us with the following comments to improve its quality:\n"
        text += scholarComment
        text += "\nWe hope Wikipedians on this talk page can take advantage of these comments and improve the quality of this page accordingly.\n"
        text += "\n[[User:ExpertIdeasBot|ExpertIdeasBot]] ([[User talk:ExpertIdeasBot|talk]]) 16:47, 4 August 2014 (UTC)\n"
        lgtoken = ''
        cookies = ''
        lgtoken, cookies = AddNewSectionToTalkPage(title, summary, text, lgtoken, cookies)
