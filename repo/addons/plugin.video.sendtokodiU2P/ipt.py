# -*- coding: utf-8 -*-
import requests
from urllib.parse import quote, urlparse, parse_qs, unquote, urlencode
import sys
import time
import sqlite3
import os
import unicodedata
import shutil
import io
import argparse
import random
import datetime
import sqlite3
try:
    from util import *
    import xbmc
    import xbmcvfs
    import xbmcaddon
    import xbmcgui
    import xbmcplugin

    ADDON = xbmcaddon.Addon("plugin.video.sendtokodiU2P")
    HANDLE = int(sys.argv[1])
    BDBOOKMARK = xbmcvfs.translatePath('special://home/userdata/addon_data/plugin.video.sendtokodiU2P/iptv.db')
except: pass

class IPTVMac:

    def __init__(self, urlBase, adrMac, token=""):
        notice(urlBase)
        self.adrMac = quote(adrMac)
        self.urlBase = urlBase
        #self.session = requests.Session()
        self.headers = {
        "X-User-Agent": "Model: MAG254; Link: Ethernet,WiFi",
        "User-Agent": "Mozilla/5.0 (QtEmbedded; U; Linux; C) AppleWebKit/533.3 (KHTML, like Gecko) MAG200 stbapp ver: 4 rev: 1812 Mobile Safari/533.3",
        "Referer": self.urlBase,
        "Accept": "application/json,application/javascript,text/javascript,text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Host": self.urlBase.split("://")[1],
        "Cookie": "mac=" + self.adrMac + "; stb_lang=en; timezone=Europe/Paris; adid=dbe9f56771de8f9abaa3bade08465d6c",
        "Accept-Encoding": "gzip, deflate",
        "Connection": "Keep-Alive",
        }
        self.token = token
        self.vod = "vod"
        self.tv = "itv"
        self.stb = "stb"
        if self.token:
            self.headers["Authorization"] = "Bearer %s" %self.token
        self.proxyDict = {}
        self.tokenUrl = "/portal.php?type=stb&action=handshake"
        self.xpcom = "/c/xpcom.common.js"
        self.tokenUrl = "/portal.php?type=stb&action=handshake&"        
        self.profileUrl = "/portal.php?type=stb&action=get_profile"
        self.infosCompteUrl = "/portal.php?type=account_info&action=get_main_info&JsHttpRequest=1-xml"
        self.genreUrl = "/portal.php?type=itv&action=get_genres&JsHttpRequest=1-xml"
        self.genreUrlVod =  "/server/load.php?action=create_link&type=vod&cmd={}&JsHttpRequest=1-xml"
        self.listGenreUrl = "/portal.php?type={}&action=get_ordered_list&genre={}&force_ch_link_check=&fav=0&sortby=number&hd=0&p={}&from_ch_id=0&JsHttpRequest=1-xml"
        self.catUrl = "/portal.php?type={}&action=get_categories&JsHttpRequest=1-xml"  #vod ou series
        self.createLink = "/portal.php?type=itv&action=create_link&cmd={}&series=0&forced_storage=false&disable_ad=false&download=false&force_ch_link_check=false&JsHttpRequest=1-xml"
        self.panel ="/panel_api.php"
        self.epg = "/portal.php?type={}&action=get_epg_info&period=72&JsHttpRequest=1-xml"
        self.epgChannel = "/portal.php?type=itv&action=get_short_epg&ch_id={}&size=10&JsHttpRequest=1-xml"
        self.catVOD = "/portal.php?type=vod&action=get_categories"
        
    def getInfos(self, compUrl):
        if self.proxyDict:
            print("proxi")
            info = requests.get(self.urlBase + compUrl, proxies=self.proxyDict, headers=self.headers)
        else: 
            info = requests.get(self.urlBase + compUrl, headers=self.headers)
        return info

    @property 
    def extractUsersPass(self):
        url5 = self.urlBase + "/server/load.php?type=itv&action=create_link&cmd=ffmpeg%20http://localhost/ch/1823_&series=&forced_storage=0&disable_ad=0&download=0&force_ch_link_check=0&JsHttpRequest=1-xml" 
        res = requests.get(url5, headers=self.headers, timeout=15, verify=False)
        j = json.loads(res.text)["js"]["cmd"]
        _, _, _, user, pwd, _ = j.split("/")
        return user, pwd
    
    def getUrl(self, compUrl):
        print(compUrl)
        if self.proxyDict:
            print("proxi")
            info = requests.get(compUrl, proxies=self.proxyDict, stream=True, allow_redirects=True)
        else: 
            info = requests.get(compUrl, stream=True, allow_redirects=True)
        return info.url

    @property
    def valideCompte(self):
        try:
            notice(self.urlBase)
            self.getInfos(self.xpcom)
            self.token = self.getInfos(self.tokenUrl).json()['js']['token']
            notice("Token: " + self.token)
            self.headers["Authorization"] = "Bearer %s" %self.token
            
            profile = self.getInfos(self.profileUrl).json()["js"]["id"]
            timez = self.getInfos(self.profileUrl).json()["js"]["default_timezone"]
            notice(timez)
            #timez = "America/Toronto"
            #self.headers["Cookie"] = "mac=" + self.adrMac + "; stb_lang=en; timezone=%s; adid=dbe9f56771de8f9abaa3bade08465d6c" %timez
            
            if profile == None:
                return False

            infoCompte = self.getInfos(self.infosCompteUrl).json()["js"]["phone"]
            self.dateExpiration = infoCompte
            notice("date expiration Compte: " + infoCompte)
            try:
                reste = datetime.datetime.strptime(infoCompte, "%B %d, %Y, %I:%M %p") - datetime.datetime.now()
                notice("reste: " + str(reste.days) + " jours")
                
                if int(reste.days):
                    return True
                else:
                    return False
            except:
                return True
        except Exception as e:
            notice("erreur validité compte " + str(e))
            return False

    def listeChaines(self, typ, genre):
        ok = True
        i = 1
        chaines = []
        while ok:
            print("Extraction Page ", i)
            tmpChaines = self.getInfos(self.listGenreUrl.format(typ, genre, i)).json()["js"]["data"]
            i += 1
            if tmpChaines:
                #notice(tmpChaines)
                #[notice(x['cur_playing']) for x in tmpChaines]
                chaines += [(chaine["cmd"], chaine["name"], chaine["id"], chaine["logo"]) for chaine in tmpChaines]
            else:
                ok = False
            if i > 30:
                ok = False
        return chaines