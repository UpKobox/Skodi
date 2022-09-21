# Module: default
# Author: CoKodico
# Created on: 15.09.2023
import xbmcplugin
from urllib.parse import quote_plus, unquote_plus, parse_qsl
import xbmc
import xbmcvfs
import xbmcaddon
import xbmcgui
import xbmcplugin
from io import BytesIO
from urllib.request import urlopen
from zipfile import ZipFile
import os
import shutil
import requests
import random
import re

artworkPath = xbmcvfs.translatePath('special://home/addons/plugin.program.Skodi/resources/media/')
fanart = artworkPath + "fanart.jpg"

def notice(content):
    log(content, xbmc.LOGINFO)

def log(msg, level=xbmc.LOGINFO):
    addon = xbmcaddon.Addon()
    addonID = addon.getAddonInfo('id')
    xbmc.log('%s: %s' % (addonID, msg), level)

def showErrorNotification(message):
    xbmcgui.Dialog().notification("Skodi", message,
                                  xbmcgui.NOTIFICATION_ERROR, 5000)
def showInfoNotification(message):
    xbmcgui.Dialog().notification("Skodi", message, xbmcgui.NOTIFICATION_INFO, 15000)

def add_dir(name, mode, thumb):
    u = sys.argv[0] + "?" + "action=" + str(mode)
    liz = xbmcgui.ListItem(name)
    liz.setArt({'icon': thumb})
    liz.setProperty("fanart_image", fanart)
    ok = xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]), url=u, listitem=liz, isFolder=True)
    return ok

##############################################

# MENU PRINCIPAL
def main_menu():
    xbmcplugin.setPluginCategory(__handle__, "Choix Skodi")
    xbmcplugin.setContent(__handle__, 'files')  
    add_dir("[COLOR transparent]1 - [/COLOR][COLOR yellow] Installer et Activer Skin [/COLOR] (Habillage en obtenir plus...)", 'inst_skin', artworkPath + 'install3.jpg')     
    add_dir("[COLOR transparent]2 - [/COLOR][COLOR cyan] Choisir Skins U2Pplay HK2[/COLOR]", 'hk2', artworkPath + 'icon (U2P).png')
    add_dir("[COLOR red]-- Choisir Skins Rayflix HK2 --[/COLOR][COLOR orangered] (Rayflix)[/COLOR]", 'rayhk2', artworkPath + 'icon (Ray).png')
    add_dir("[COLOR yellow]--- Menu pour installer ---[/COLOR]", 'inst_add', artworkPath + 'click-here-button.jpg')
    #add_dir("Choix SKins [COLOR green]vStream[/COLOR] Clic ici", 'vstream', artworkPath + 'icone.png')
    add_dir("[COLOR blueviolet]--- Sauvegarde et restauration ---[/COLOR]", 'save_restor', artworkPath + 'save.png')
    #add_dir("[COLOR lime]Maj Database HK2[/COLOR]", 'menumajhk2', artworkPath + 'icone.png')
    #add_dir("[COLOR darkviolet]Nettoyer KODI[/COLOR]", 'nettoye', artworkPath + 'icone.png')
    xbmcplugin.endOfDirectory(handle=__handle__, succeeded=True)

##############################################

# MENU INSTALLER LES REPOSITORY 
def inst_add():
    xbmcplugin.setPluginCategory(__handle__, "Installer les Repo et Skins")
    xbmcplugin.setContent(__handle__, 'files')
    add_dir("[COLOR darkorange]1 - [/COLOR][COLOR yellow]Installer les repo [/COLOR](Redemarrage Kodi obligatoire)", 'inst_tout', artworkPath + 'download-icon.jpg')    
    add_dir("[COLOR darkorange]2 - [/COLOR][COLOR yellow]Activer les repo[/COLOR]", 'au_maj2', artworkPath + 'install.jpg')    
    add_dir("[COLOR darkorange]3 - [/COLOR][COLOR yellow]Installer Skins [/COLOR](Habillage en obtenir plus...)", 'inst_skin', artworkPath + 'install3.jpg') 
    #add_dir("Mettre a jour les icones", 'au_maj', artworkPath + 'icone.png')
    xbmcplugin.endOfDirectory(handle=__handle__, succeeded=True)

# MENU INSTALLER ADDONS ADDITIONNELS
def inst_add2():
    xbmcplugin.setPluginCategory(__handle__, "Installer addons additionnels")
    xbmcplugin.setContent(__handle__, 'files')
    add_dir("[COLOR red]1[/COLOR] Copier [COLOR deepskyblue]addons additionnels[/COLOR] en un clic", 'inst_tout2', artworkPath + 'fanart (Ray).jpg')
    add_dir("[COLOR red]2[/COLOR] Relancer Kodi clic ici", 'inst_quit2', artworkPath + 'fanart (Ray).jpg')
    add_dir("[COLOR red]3[/COLOR] Activer [COLOR deepskyblue]addons additionnels[/COLOR] en un clic", 'inst_act2', artworkPath + 'fanart (Ray).jpg')
    xbmcplugin.endOfDirectory(handle=__handle__, succeeded=True)


# INSTALLER LES REPOSITORY 
def inst_tout():
    #install repository additionnels
    # suppression dossier temporaire
    dirPath = xbmc.translatePath('special://home/temp/temp/')
    try:
        shutil.rmtree(dirPath)
    except:
        print('Error while deleting directory')
    xbmc.sleep(2000)
    xbmc.executebuiltin("Notification(REPO,Téléchargement en cours...)")
    # telechargement et extraction du zip
    zipurl = 'https://github.com/UpKobox/Skodi/raw/main/repo.zip'
    with urlopen(zipurl) as zipresp:
        with ZipFile(BytesIO(zipresp.read())) as zfile:
            zfile.extractall(xbmc.translatePath('special://home/temp/temp/'))
    # copie des fichiers extraie
    source_dir = xbmc.translatePath('special://home/temp/temp/addons')
    destination_dir = xbmc.translatePath('special://home/addons')
    shutil.copytree(source_dir, destination_dir, dirs_exist_ok=True)
    xbmc.sleep(3000)
    xbmc.executebuiltin("Notification(MISE A JOUR OK,Addons copiés !)")
    #active addon
    xbmc.executeJSONRPC('{"jsonrpc": "2.0", "id":1, "method": "Addons.SetAddonEnabled", "params": { "addonid": "repository.autowidget", "enabled": true }}')
    xbmc.executeJSONRPC('{"jsonrpc": "2.0", "id":1, "method": "Addons.SetAddonEnabled", "params": { "addonid": "repository.jurialmunkey", "enabled": true }}')
    xbmc.executeJSONRPC('{"jsonrpc": "2.0", "id":1, "method": "Addons.SetAddonEnabled", "params": { "addonid": "repository.prototype", "enabled": true }}')
    xbmc.executeJSONRPC('{"jsonrpc": "2.0", "id":1, "method": "Addons.SetAddonEnabled", "params": { "addonid": "repository.lattsrepo", "enabled": true }}')
    xbmc.executeJSONRPC('{"jsonrpc": "2.0", "id":1, "method": "Addons.SetAddonEnabled", "params": { "addonid": "repository.titan.bingie.mod", "enabled": true }}')
    xbmc.executeJSONRPC('{"jsonrpc": "2.0", "id":1, "method": "Addons.SetAddonEnabled", "params": { "addonid": "repository.marcelveldt", "enabled": true }}')
    xbmc.executeJSONRPC('{"jsonrpc": "2.0", "id":1, "method": "Addons.SetAddonEnabled", "params": { "addonid": "repository.UpKobox", "enabled": true }}')
    xbmc.executeJSONRPC('{"jsonrpc": "2.0", "id":1, "method": "Addons.SetAddonEnabled", "params": { "addonid": "repository.RayRepo", "enabled": true }}')
    xbmc.executeJSONRPC('{"jsonrpc": "2.0", "id":1, "method": "Addons.SetAddonEnabled", "params": { "addonid": "repository.auramod.aio", "enabled": true }}')
    xbmc.sleep(2000)
    xbmc.executebuiltin("Notification(MISE A JOUR OK,Addons activer !)")
    xbmc.sleep(2000)
    xbmc.executebuiltin( 'ReloadSkin()' )
    xbmc.executebuiltin( "Notification(Rafraichissement Skin,,2000)" )
    xbmc.executebuiltin("Notification(ATTENTION KODI VA SE FERMER , Relancez le...)")
    xbmc.sleep(2000)
    xbmc.executebuiltin('Quit')

# ACTIVER LES REPOSITORY
def inst_quit():
    #active addon
    xbmc.executeJSONRPC('{"jsonrpc": "2.0", "id":1, "method": "Addons.SetAddonEnabled", "params": { "addonid": "repository.autowidget", "enabled": true }}')
    xbmc.executeJSONRPC('{"jsonrpc": "2.0", "id":1, "method": "Addons.SetAddonEnabled", "params": { "addonid": "repository.jurialmunkey", "enabled": true }}')
    xbmc.executeJSONRPC('{"jsonrpc": "2.0", "id":1, "method": "Addons.SetAddonEnabled", "params": { "addonid": "repository.prototype", "enabled": true }}')
    xbmc.executeJSONRPC('{"jsonrpc": "2.0", "id":1, "method": "Addons.SetAddonEnabled", "params": { "addonid": "repository.lattsrepo", "enabled": true }}')
    xbmc.executeJSONRPC('{"jsonrpc": "2.0", "id":1, "method": "Addons.SetAddonEnabled", "params": { "addonid": "repository.titan.bingie.mod", "enabled": true }}')
    xbmc.executeJSONRPC('{"jsonrpc": "2.0", "id":1, "method": "Addons.SetAddonEnabled", "params": { "addonid": "repository.marcelveldt", "enabled": true }}')
    xbmc.executeJSONRPC('{"jsonrpc": "2.0", "id":1, "method": "Addons.SetAddonEnabled", "params": { "addonid": "repository.UpKobox", "enabled": true }}')
    xbmc.executeJSONRPC('{"jsonrpc": "2.0", "id":1, "method": "Addons.SetAddonEnabled", "params": { "addonid": "repository.RayRepo", "enabled": true }}')
    xbmc.executeJSONRPC('{"jsonrpc": "2.0", "id":1, "method": "Addons.SetAddonEnabled", "params": { "addonid": "repository.auramod.aio", "enabled": true }}')
    xbmc.sleep(2000)
    xbmc.executebuiltin("Notification(MISE A JOUR OK,Addons activer !)")

# ACTIVER ADDONS ADDITIONNELS
def inst_act():
    #active addon
    xbmc.executeJSONRPC('{"jsonrpc": "2.0", "id":1, "method": "Addons.SetAddonEnabled", "params": { "addonid": "repository.autowidget", "enabled": true }}')
    xbmc.executeJSONRPC('{"jsonrpc": "2.0", "id":1, "method": "Addons.SetAddonEnabled", "params": { "addonid": "repository.jurialmunkey", "enabled": true }}')
    xbmc.executeJSONRPC('{"jsonrpc": "2.0", "id":1, "method": "Addons.SetAddonEnabled", "params": { "addonid": "repository.prototype", "enabled": true }}')
    xbmc.executeJSONRPC('{"jsonrpc": "2.0", "id":1, "method": "Addons.SetAddonEnabled", "params": { "addonid": "repository.lattsrepo", "enabled": true }}')
    xbmc.executeJSONRPC('{"jsonrpc": "2.0", "id":1, "method": "Addons.SetAddonEnabled", "params": { "addonid": "repository.titan.bingie.mod", "enabled": true }}')
    xbmc.executeJSONRPC('{"jsonrpc": "2.0", "id":1, "method": "Addons.SetAddonEnabled", "params": { "addonid": "repository.marcelveldt", "enabled": true }}')
    xbmc.executeJSONRPC('{"jsonrpc": "2.0", "id":1, "method": "Addons.SetAddonEnabled", "params": { "addonid": "repository.UpKobox", "enabled": true }}')
    xbmc.executeJSONRPC('{"jsonrpc": "2.0", "id":1, "method": "Addons.SetAddonEnabled", "params": { "addonid": "repository.RayRepo", "enabled": true }}')
    xbmc.executeJSONRPC('{"jsonrpc": "2.0", "id":1, "method": "Addons.SetAddonEnabled", "params": { "addonid": "repository.auramod.aio", "enabled": true }}')
    xbmc.sleep(2000)
    xbmc.executebuiltin("Notification(MISE A JOUR OK,Addons activer !)")

##############################################

# COPIER ADDONS ADDITIONNELS
def inst_tout2():
    #install addons additionnels
    # suppression dossier temporaire
    dirPath = xbmc.translatePath('special://home/temp/temp/')
    try:
        shutil.rmtree(dirPath)
    except:
        print('Error while deleting directory')
    xbmc.sleep(2000)
    xbmc.executebuiltin("Notification(ADDONS,Téléchargement en cours...)")
    # telechargement et extraction du zip
    zipurl = 'http://kodi.prf2.ovh/dbs/addons.zip'
    with urlopen(zipurl) as zipresp:
        with ZipFile(BytesIO(zipresp.read())) as zfile:
            zfile.extractall(xbmc.translatePath('special://home/temp/temp/'))
    # copie des fichiers extraie
    source_dir = xbmc.translatePath('special://home/temp/temp/addons')
    destination_dir = xbmc.translatePath('special://home/addons')
    shutil.copytree(source_dir, destination_dir, dirs_exist_ok=True)
    xbmc.sleep(3000)
    #active addon
    xbmc.executeJSONRPC('{"jsonrpc": "2.0", "id":1, "method": "Addons.SetAddonEnabled", "params": { "addonid": "resource.uisounds.androidtv", "enabled": true }}')
    xbmc.executeJSONRPC('{"jsonrpc": "2.0", "id":1, "method": "Addons.SetAddonEnabled", "params": { "addonid": "plugin.program.autocompletion", "enabled": true }}')
    xbmc.executeJSONRPC('{"jsonrpc": "2.0", "id":1, "method": "Addons.SetAddonEnabled", "params": { "addonid": "repository.prototype", "enabled": true }}')
    xbmc.executeJSONRPC('{"jsonrpc": "2.0", "id":1, "method": "Addons.SetAddonEnabled", "params": { "addonid": "repository.vstream", "enabled": true }}')
    xbmc.executeJSONRPC('{"jsonrpc": "2.0", "id":1, "method": "Addons.SetAddonEnabled", "params": { "addonid": "script.module.dnspython", "enabled": true }}')
    xbmc.executeJSONRPC('{"jsonrpc": "2.0", "id":1, "method": "Addons.SetAddonEnabled", "params": { "addonid": "service.upnext", "enabled": true }}')
    xbmc.executeJSONRPC('{"jsonrpc": "2.0", "id":1, "method": "Addons.SetAddonEnabled", "params": { "addonid": "repository.UpKobox", "enabled": true }}')
    xbmc.sleep(2000)
    xbmc.executebuiltin("Notification(MISE A JOUR OK,Addons copiés !)")

# QUITTER KODI
def inst_quit2():
    # fermeture de kodi
    xbmc.executebuiltin("Notification(ATTENTION KODI VA SE FERMER , Relancez le...)")
    xbmc.sleep(2000)
    xbmc.executebuiltin('ReloadSkin')
    xbmc.sleep(2000)
    xbmc.executebuiltin('Quit')

# ACTIVER ADDONS ADDITIONNELS
def inst_act2():
    #active addon
    xbmc.executeJSONRPC('{"jsonrpc": "2.0", "id":1, "method": "Addons.SetAddonEnabled", "params": { "addonid": "resource.uisounds.androidtv", "enabled": true }}')
    xbmc.executeJSONRPC('{"jsonrpc": "2.0", "id":1, "method": "Addons.SetAddonEnabled", "params": { "addonid": "plugin.program.autocompletion", "enabled": true }}')
    xbmc.executeJSONRPC('{"jsonrpc": "2.0", "id":1, "method": "Addons.SetAddonEnabled", "params": { "addonid": "repository.prototype", "enabled": true }}')
    xbmc.executeJSONRPC('{"jsonrpc": "2.0", "id":1, "method": "Addons.SetAddonEnabled", "params": { "addonid": "repository.vstream", "enabled": true }}')
    xbmc.executeJSONRPC('{"jsonrpc": "2.0", "id":1, "method": "Addons.SetAddonEnabled", "params": { "addonid": "script.module.dnspython", "enabled": true }}')
    xbmc.executeJSONRPC('{"jsonrpc": "2.0", "id":1, "method": "Addons.SetAddonEnabled", "params": { "addonid": "service.upnext", "enabled": true }}')
    xbmc.executeJSONRPC('{"jsonrpc": "2.0", "id":1, "method": "Addons.SetAddonEnabled", "params": { "addonid": "repository.UpKobox", "enabled": true }}')
    xbmc.sleep(2000)
    xbmc.executebuiltin("Notification(MISE A JOUR OK,Addons activer !)")

##############################################

# METTRE A JOUR LES ICONES
def au_maj():
    # mise a jour icone aura
    # telechargement et extraction du zip
    zipurl = 'https://github.com/prf2/pack/raw/kodi/au_maj.zip'
    with urlopen(zipurl) as zipresp:
        with ZipFile(BytesIO(zipresp.read())) as zfile:
            zfile.extractall(xbmc.translatePath('special://home/temp/temp/'))
    # copie des fichiers extraie
    source_dir = xbmc.translatePath('special://home/temp/temp/addon_data')
    destination_dir = xbmc.translatePath('special://home/userdata/addon_data')
    source_dir2 = xbmc.translatePath('special://home/temp/temp/addons')
    destination_dir2 = xbmc.translatePath('special://home/addons')
    source_dir3 = xbmc.translatePath('special://home/temp/temp/keymaps')
    destination_dir3 = xbmc.translatePath('special://home/userdata/keymaps')
    shutil.copytree(source_dir, destination_dir, dirs_exist_ok=True)
    shutil.copytree(source_dir2, destination_dir2, dirs_exist_ok=True)
    shutil.copytree(source_dir3, destination_dir3, dirs_exist_ok=True)
    xbmc.executebuiltin("Notification(EXTRACTION OK,Mise à jour effectuée !)")
    xbmc.sleep(2000)
    
##############################################
def au_majCoKo():
    # mise a jour icone CoKodico
    # telechargement et extraction du zip
    zipurl = 'https://github.com/UpKobox/Skodi/raw/main/SKIN/media(CoKodico).zip'
    with urlopen(zipurl) as zipresp:
        with ZipFile(BytesIO(zipresp.read())) as zfile:
            zfile.extractall(xbmc.translatePath('special://home/temp/temp/'))
    # copie des fichiers extraie
    source_dir = xbmc.translatePath('special://home/temp/temp')
    destination_dir = xbmc.translatePath('special://home/media')
    shutil.copytree(source_dir, destination_dir, dirs_exist_ok=True)
    xbmc.executebuiltin("Notification(EXTRACTION OK,Maj 1 effectuée !)")
    xbmc.sleep(2000)
    zipurl = 'https://github.com/UpKobox/Skodi/raw/main/SKIN/png(CoKodico).zip'
    with urlopen(zipurl) as zipresp:
        with ZipFile(BytesIO(zipresp.read())) as zfile:
            zfile.extractall(xbmc.translatePath('special://home/temp/temp/'))
    # copie des fichiers extraie
    source_dir = xbmc.translatePath('special://home/temp/temp')
    destination_dir = xbmc.translatePath('special://home/media')
    shutil.copytree(source_dir, destination_dir, dirs_exist_ok=True)
    xbmc.executebuiltin("Notification(EXTRACTION OK,Maj 2 effectuée !)")
    xbmc.sleep(2000)
##############################################

# ACTIVER ET METTRE A JOUR LES REPOSITORY
def au_maj2():
    #install repository additionnels
    # suppression dossier temporaire
    dirPath = xbmc.translatePath('special://home/temp/temp/')
    try:
        shutil.rmtree(dirPath)
    except:
        print('Error while deleting directory')
    xbmc.sleep(2000)
    xbmc.executebuiltin("Notification(REPO,Téléchargement en cours...)")
    # telechargement et extraction du zip
    zipurl = 'https://github.com/UpKobox/Skodi/raw/main/repo.zip'
    with urlopen(zipurl) as zipresp:
        with ZipFile(BytesIO(zipresp.read())) as zfile:
            zfile.extractall(xbmc.translatePath('special://home/temp/temp/'))
    # copie des fichiers extraie
    source_dir = xbmc.translatePath('special://home/temp/temp/addons')
    destination_dir = xbmc.translatePath('special://home/addons')
    shutil.copytree(source_dir, destination_dir, dirs_exist_ok=True)
    xbmc.sleep(3000)
    xbmc.executebuiltin("Notification(MISE A JOUR OK,Addons copiés !)")
    #active addon
    xbmc.executeJSONRPC('{"jsonrpc": "2.0", "id":1, "method": "Addons.SetAddonEnabled", "params": { "addonid": "repository.autowidget", "enabled": true }}')
    xbmc.executeJSONRPC('{"jsonrpc": "2.0", "id":1, "method": "Addons.SetAddonEnabled", "params": { "addonid": "repository.jurialmunkey", "enabled": true }}')
    xbmc.executeJSONRPC('{"jsonrpc": "2.0", "id":1, "method": "Addons.SetAddonEnabled", "params": { "addonid": "repository.prototype", "enabled": true }}')
    xbmc.executeJSONRPC('{"jsonrpc": "2.0", "id":1, "method": "Addons.SetAddonEnabled", "params": { "addonid": "repository.lattsrepo", "enabled": true }}')
    xbmc.executeJSONRPC('{"jsonrpc": "2.0", "id":1, "method": "Addons.SetAddonEnabled", "params": { "addonid": "repository.titan.bingie.mod", "enabled": true }}')
    xbmc.executeJSONRPC('{"jsonrpc": "2.0", "id":1, "method": "Addons.SetAddonEnabled", "params": { "addonid": "repository.marcelveldt", "enabled": true }}')
    xbmc.executeJSONRPC('{"jsonrpc": "2.0", "id":1, "method": "Addons.SetAddonEnabled", "params": { "addonid": "repository.UpKobox", "enabled": true }}')
    xbmc.executeJSONRPC('{"jsonrpc": "2.0", "id":1, "method": "Addons.SetAddonEnabled", "params": { "addonid": "repository.RayRepo", "enabled": true }}')
    xbmc.executeJSONRPC('{"jsonrpc": "2.0", "id":1, "method": "Addons.SetAddonEnabled", "params": { "addonid": "repository.auramod.aio", "enabled": true }}')
    xbmc.sleep(2000)
    xbmc.executebuiltin("Notification(MISE A JOUR OK,Addons activer !)")

##############################################
# Installer Skin
def inst_skin():
    xbmc.executebuiltin('RunScript(special://home/addons/plugin.program.Skodi/resources/ChangeSkin2.py,True)')
##############################################

##############################################

# COMPTES PREMIUM ALEATOIRE
def menuKey():
    tabkey = extractAnotpad()
    nb = 0
    ok = False
    while tabkey:
        keyUpto = random.choice(tabkey)
        status, validite = testUptobox(keyUpto)
        if status == "Success":
            showInfoNotification("Notification(Key Upto ok! expire: %s)" %validite)
            ok = True
            break
        else:
            tabkey.remove(keyUpto)
            showErrorNotification("Prevenir Ray key: %s HS" %keyUpto)
            nb += 1
        if nb > 50:
            break
            return
    if ok:
        # config u2play
        try:
            addon = xbmcaddon.Addon("plugin.video.sendtokodiU2P")
            addon.setSetting(id="keyupto", value=keyUpto)
            nb_items = "50"
            addon.setSetting(id="nb_items", value=nb_items)
            thumbnails = "5000"
            addon.setSetting(id="thumbnails", value=thumbnails)
        except Exception as e:
            notice("Erreur HK: " + str(e))
        
        # config vstream
        try:
            addon = xbmcaddon.Addon("plugin.video.vstream")
            cache_v = "8"
            addon.setSetting(id="pastebin_cacheDuration", value=cache_v)
            hoster_uptobox_premium = "true"
            addon.setSetting(id="hoster_uptobox_premium", value=hoster_uptobox_premium)
            hoster_uptobox_mode_default = "2"
            addon.setSetting(id="hoster_uptobox_mode_default", value=hoster_uptobox_mode_default)
            meta_view = "true"
            addon.setSetting(id="meta-view", value=meta_view)
            addon.setSetting(id="hoster_uptobox_token", value=keyUpto)
        except Exception as e:
            notice("Erreur Vstream: " + str(e))
        
        #config catchup
        try:
            addon = xbmcaddon.Addon("plugin.video.catchuptvandmore")
            mail = "rayflix@laposte.net"
            mot2passe = "Mot2passe"
            addon.setSetting(id="nrj.login", value=mail)
            addon.setSetting(id="6play.login", value=mail)
            addon.setSetting(id="rmcbfmplay.login", value=mail)
            addon.setSetting(id="nrj.password", value=mot2passe)
            addon.setSetting(id="6play.password", value=mot2passe)
            addon.setSetting(id="rmcbfmplay.password", value=mot2passe)
        except Exception as e:
            notice("Erreur CatchUp: " + str(e))

        showInfoNotification("Config Comptes ok")

def extractAnotpad():
    numAnotepad = __addon__.getSetting("numAnotepad")
    motifAnotepad = r'.*<\s*div\s*class\s*=\s*"\s*plaintext\s*"\s*>(?P<txAnote>.+?)</div>.*'
    url = "https://anotepad.com/note/read/" + numAnotepad.strip()
    rec = requests.get(url, verify=False)
    r = re.match(motifAnotepad, rec.text, re.MULTILINE|re.DOTALL)
    tabKey = [x.strip() for x in r.group("txAnote").splitlines() if x]
    return tabKey 

def testUptobox(key):
    url = 'https://uptobox.com/api/user/me?token=' + key
    headers = {'Accept': 'application/json'}
    try:
        data = requests.get(url, headers=headers).json()
        status = data["message"]
        validite = data["data"]["premium_expire"]
    except:
        status = "out"
        validite = ""
    return status, validite 

##############################################

# MENU CHOIX SKIN U2PLAY HK
def hk():
    #choix skin
    xbmcplugin.setPluginCategory(__handle__, "Choix skin HK")
    xbmcplugin.setContent(__handle__, 'files')
    add_dir("Activer Mise a Jour Database Automatique [COLOR red]Clic ici[/COLOR]", 'db_auto', artworkPath + 'icone.png')
    add_dir("[COLOR red]u2Play[/COLOR] SKIN LIGHT [COLOR deepskyblue](le + leger)[/COLOR]", 'choixskinlite', artworkPath + 'icone.png')
    add_dir("[COLOR red]u2Play[/COLOR] SKIN FULL [COLOR deepskyblue](le + gourmand)[/COLOR]", 'choixskinfull', artworkPath + 'icone.png')
    add_dir("[COLOR red]u2Play[/COLOR] SKIN KIDS [COLOR deepskyblue](special enfants)[/COLOR]", 'choixskinkids', artworkPath + 'icone.png')
    add_dir("Desactiver Mise a Jour Database Automatique [COLOR red]Clic ici[/COLOR]", 'db_auto_no', artworkPath + 'icone.png')
    xbmcplugin.endOfDirectory(handle=__handle__, succeeded=True)

# ACTIVER MISE A JOUR DATABASE AUTOMATIQUE
def db_auto():
    #active autoexec
    xbmc.executeJSONRPC('{"jsonrpc": "2.0", "id":1, "method": "Addons.SetAddonEnabled", "params": { "addonid": "service.autoexec", "enabled": true }}')
    xbmc.sleep(2000)
    #notification
    xbmc.executebuiltin("Notification(AUTOEXEC, activé...)")

# DESACTIVER MISE A JOUR DATABASE AUTOMATIQUE
def db_auto_no():
    #desactive autoexec
    xbmc.executeJSONRPC('{"jsonrpc": "2.0", "id":1, "method": "Addons.SetAddonEnabled", "params": { "addonid": "service.autoexec", "enabled": false }}')
    xbmc.sleep(2000)
    #notification
    xbmc.executebuiltin("Notification(AUTOEXEC, désactivé...)")

##############################################

# CHOIX SKINRAY HK2
def rayhk2():
    #choix skin
    xbmcplugin.setPluginCategory(__handle__, "Choix Skins [COLOR red]Rayflix HK2[/COLOR]")
    xbmcplugin.setContent(__handle__, 'files')
    add_dir("[COLOR deepskyblue]Rayflix[/COLOR] Menu installation [COLOR red](Redemarrage necessaire)[/COLOR]", 'inst_add2', artworkPath + 'icon (Ray).png')
    add_dir("[COLOR red]Rayflix[/COLOR] Skin LIGHT [COLOR deepskyblue](le + leger)[/COLOR]", 'hk2lite', artworkPath + 'icon (Ray).png')
    add_dir("[COLOR red]Rayflix[/COLOR] Skin FULL [COLOR deepskyblue](le + gourmand)[/COLOR]", 'hk2full', artworkPath + 'icon (Ray).png')
    add_dir("[COLOR red]Rayflix[/COLOR] Skin KIDS [COLOR deepskyblue](special enfants)[/COLOR]", 'hk2kids', artworkPath + 'icon (Ray).png')
    add_dir("[COLOR red]Rayflix[/COLOR] Skin RETRO [COLOR deepskyblue](pour les nostalgiques)[/COLOR]", 'hk2retro', artworkPath + 'icon (Ray).png')
    add_dir("[COLOR lime]Lancer: Skin Rayflix choisi [/COLOR]", 'ChangeSkinsProjectAura', artworkPath + 'icon (Ray).png')
    add_dir("[COLOR red]Rayflix[/COLOR] icones [COLOR deepskyblue](pour Skins de Rayflix)[/COLOR]", 'au_maj', artworkPath + 'icon (Ray).png')
    add_dir("[COLOR lime]Maj HK2 et Skin sauvegarde[/COLOR]", 'menumajhk2', artworkPath + 'NETTOYER1.jpg')
    xbmcplugin.endOfDirectory(handle=__handle__, succeeded=True)

##############################################

# CHOIX SKIN U2PLAY HK2
def hk2():
    #choix skin
    xbmcplugin.setPluginCategory(__handle__, "Choix skin [COLOR cyan]U2Pplay[/COLOR]")
    xbmcplugin.setContent(__handle__, 'files')
    #add_dir("[COLOR red]U2Pplay[/COLOR] SKIN LEGER [COLOR deepskyblue](le + leger)[/COLOR]", 'hk2leger', artworkPath + 'icone.png')
    #add_dir("[COLOR red]U2Pplay[/COLOR] SKIN COMPLET [COLOR deepskyblue](le + gourmand)[/COLOR]", 'hk2complet', artworkPath + 'icone.png')
    #add_dir("[COLOR red]U2Pplay[/COLOR] SKIN ENFANTS [COLOR deepskyblue](special enfants)[/COLOR]", 'hk2enfants', artworkPath + 'icon (enfants2).png')
    add_dir("[COLOR cyan]U2Pplay[/COLOR] SKIN de [COLOR yellow](CoKodico)[/COLOR]", 'CoKo', artworkPath + 'icon (CoKodico).jpg')
    add_dir("[COLOR cyan]U2Pplay[/COLOR] SKIN de [COLOR yellow](Luc562)[/COLOR]", 'Luc562', artworkPath + 'Luc562.png')
    add_dir("[COLOR cyan]U2Pplay[/COLOR] SKIN de [COLOR yellow](pistachePoilue)[/COLOR]", 'pistachePoilue', artworkPath + 'icone.png')
    add_dir("[COLOR cyan]U2Pplay[/COLOR] SKIN de [COLOR yellow](bePurple)[/COLOR]", 'bePurple', artworkPath + 'icone.png')
    add_dir("[COLOR cyan]U2Pplay[/COLOR] SKIN de [COLOR yellow](Ghantholiny)[/COLOR]", 'Ghantholiny', artworkPath + 'icone.png')
    add_dir("[COLOR cyan]U2Pplay[/COLOR] SKIN de [COLOR yellow](FanKai)[/COLOR]", 'FanKai', artworkPath + 'FanKai.png')
    add_dir("[COLOR lime]Maj HK2 et Skin sauvegarde[/COLOR]", 'menumajhk2', artworkPath + 'NETTOYER1.jpg')
    xbmcplugin.endOfDirectory(handle=__handle__, succeeded=True)

##############################################

# MENU CHOIX SKIN U2PLAY COKODICO
def CoKo():
    #choix skin
    xbmcplugin.setPluginCategory(__handle__, "Choix Skins [COLOR chartreuse]CoKodico[/COLOR]")
    xbmcplugin.setContent(__handle__, 'files')
    add_dir("[COLOR cyan]Choisir:[/COLOR] Skin Arctic Horizon 2 [COLOR yellow](Alpha)[/COLOR]", 'hk2AH2', artworkPath + 'icon (AH2).png')
    add_dir("[COLOR lime]Lancer:[/COLOR] Skin Arctic Horizon 2 [COLOR yellow](Alpha)[/COLOR]", 'ChangeSkinAH2CoKo', artworkPath + 'icon (AH2).png')
    add_dir("[COLOR cyan]Choisir:[/COLOR] Choisir Skin Titan BINGIE MOD [COLOR yellow](le + gourmand)[/COLOR]", 'titanbingieCoKo', artworkPath + 'fanart (titanbingieCoKo).jpg')
    add_dir("[COLOR lime]Lancer:[/COLOR] Lancer Skin Titan BINGIE MOD [COLOR yellow](le + gourmand)[/COLOR]", 'ChangeSkinbingieCoKo', artworkPath + 'fanart (titanbingieCoKo).jpg')
    add_dir("[COLOR cyan]Choisir:[/COLOR] Choisir Skin Copacetic [COLOR yellow](WIP Alpha)[/COLOR]", 'SkinCoKopacetic', artworkPath + 'fanart (Copacetic).jpg')
    add_dir("[COLOR lime]Lancer:[/COLOR] Lancer Skin Copacetic [COLOR yellow](WIP Alpha)[/COLOR]", 'ChangeSkincopacetiCoKo', artworkPath + 'fanart (Copacetic).jpg')
    add_dir("[COLOR cyan]Choisir:[/COLOR] Choisir Skin Aeon [COLOR yellow](MQ 8)[/COLOR]", 'MQ8', artworkPath + 'fanart (MQ8).jpg')
    add_dir("[COLOR lime]Lancer:[/COLOR] Lancer Skin Aeon [COLOR yellow](MQ 8)[/COLOR]", 'ChangeSkinAeonMQ8CoKo', artworkPath + 'fanart (MQ8).jpg')
    add_dir("Mettre a jour les icones", 'au_majCoKo', artworkPath + 'icone.png')
    add_dir("[COLOR red]Maj HK2 et Skin sauvegarde[/COLOR]", 'menumajhk2', artworkPath + 'NETTOYER1.jpg')
    #add_dir("[COLOR red]Desactiver Mise a Jour Database Automatique[/COLOR]", 'db_auto_no', artworkPath + 'icon (U2P).png')
    xbmcplugin.endOfDirectory(handle=__handle__, succeeded=True)

##############################################

# MENU CHOIX SKIN U2PLAY bePurple
def bePurple():
    #choix skin
    xbmcplugin.setPluginCategory(__handle__, "Choix Skins [COLOR chartreuse]bePurple[/COLOR]")
    xbmcplugin.setContent(__handle__, 'files')
    add_dir("[COLOR cyan]Choisir:[/COLOR] Skin Arctic Horizon 2 [COLOR yellow](WIP Alpha)[/COLOR]", 'bePurpleAH2', artworkPath + 'icon (AH2).png')
    add_dir("[COLOR lime]Lancer:[/COLOR] Skin Arctic Horizon 2 [COLOR yellow](Alpha)[/COLOR]", 'ChangeSkinAH2CoKo', artworkPath + 'icon (AH2).png')
    add_dir("[COLOR cyan]Choisir:[/COLOR] Skin Auramod [COLOR yellow](Enfants)[/COLOR]", 'bePurpleAuraKid', artworkPath + 'icon (enfants).png')
    add_dir("[COLOR lime]Lancer:[/COLOR] Skin Auramod [COLOR yellow](Enfants)[/COLOR]", 'ChangeSkinskinauramod', artworkPath + 'icon (enfants).png')
    add_dir("[COLOR cyan]Choisir:[/COLOR] Skin Auramod [COLOR yellow][/COLOR]", 'bePurpleAura', artworkPath + 'Skin Auramod.jpg')
    add_dir("[COLOR lime]Lancer:[/COLOR] Skin Auramod [COLOR yellow](Enfants)[/COLOR]", 'ChangeSkinskinauramod', artworkPath + 'icon (enfants).png')
    #add_dir("[COLOR cyan]U2Pplay[/COLOR] Skin Aeon [COLOR yellow](MQ 8)[/COLOR]", 'MQ8', artworkPath + 'fanart (MQ8).jpg')
    #add_dir("Mettre a jour les icones", 'au_majCoKo', artworkPath + 'icone.png')
    add_dir("[COLOR red]Maj HK2 et Skin sauvegarde[/COLOR]", 'menumajhk2', artworkPath + 'NETTOYER1.jpg')
    #add_dir("[COLOR red]Desactiver Mise a Jour Database Automatique[/COLOR]", 'db_auto_no', artworkPath + 'icon (U2P).png')
    xbmcplugin.endOfDirectory(handle=__handle__, succeeded=True)

############################################################################################

# MENU CHOIX SKIN U2PLAY Luc562
def Luc562():
    #choix skin
    xbmcplugin.setPluginCategory(__handle__, "Choix skin [COLOR chartreuse]Luc562[/COLOR]")
    xbmcplugin.setContent(__handle__, 'files')
    add_dir("[COLOR cyan]Choisir:[/COLOR] Skin Arctic Horizon 2 [COLOR yellow](WIP Alpha)[/COLOR]", 'Luc562AH2', artworkPath + 'icon (AH2).png')
    add_dir("[COLOR lime]Lancer:[/COLOR] Skin Arctic Horizon 2 [COLOR yellow](Alpha)[/COLOR]", 'ChangeSkinAH2CoKo', artworkPath + 'icon (AH2).png')
    add_dir("[COLOR cyan]Choisir:[/COLOR] Skin Aeon Nox [COLOR yellow](Sylvo)[/COLOR]", 'Luc562Aeon', artworkPath + 'aeon(nox).jpg')
    add_dir("[COLOR lime]Lancer:[/COLOR] Skin Aeon Nox [COLOR yellow](Sylvo)[/COLOR]", 'ChangeSkinaeonnoxsilvo', artworkPath + 'aeon(nox).jpg')
    add_dir("[COLOR cyan]Choisir:[/COLOR] Skin Mimic [COLOR yellow](lr)[/COLOR]", 'Luc562Mimic', artworkPath + 'mimic.jpg')
    add_dir("[COLOR lime]Lancer:[/COLOR] Skin Mimic [COLOR yellow](lr)[/COLOR]", 'ChangeSkinmimiclr', artworkPath + 'mimic.jpg')
    add_dir("[COLOR red]Maj HK2 et Skin sauvegarde[/COLOR]", 'menumajhk2', artworkPath + 'NETTOYER1.jpg')
    xbmcplugin.endOfDirectory(handle=__handle__, succeeded=True)

##############################################

# MENU CHOIX SKIN U2PLAY pistachePoilue
def pistachePoilue():
    #choix skin
    xbmcplugin.setPluginCategory(__handle__, "Choix skin [COLOR chartreuse]pistachePoilue[/COLOR]")
    xbmcplugin.setContent(__handle__, 'files')
    add_dir("[COLOR cyan]Choisir:[/COLOR] Skin Arctic Horizon 2 [COLOR yellow](WIP Alpha)[/COLOR]", 'pistachePoilueAH2', artworkPath + 'icon (AH2).png')
    add_dir("[COLOR lime]Lancer:[/COLOR] Skin Arctic Horizon 2 [COLOR yellow](Alpha)[/COLOR]", 'ChangeSkinAH2CoKo', artworkPath + 'icon (AH2).png')
    add_dir("[COLOR red]Maj HK2 et Skin sauvegarde[/COLOR]", 'menumajhk2', artworkPath + 'NETTOYER1.jpg')
    xbmcplugin.endOfDirectory(handle=__handle__, succeeded=True)

##############################################

# MENU CHOIX SKIN U2PLAY Ghantholiny
def Ghantholiny():
    #choix skin
    xbmcplugin.setPluginCategory(__handle__, "Choix skin [COLOR chartreuse]Ghantholiny[/COLOR]")
    xbmcplugin.setContent(__handle__, 'files')
    add_dir("[COLOR cyan]Choisir:[/COLOR] Skin Arctic Horizon [COLOR yellow][/COLOR](1)", 'GhantholinyAH', artworkPath + 'skin.arctic.horizon.png')
    add_dir("[COLOR lime]Lancer:[/COLOR] Skin Arctic Horizon [COLOR yellow](1)[/COLOR]", 'ChangeSkinarctichorizon', artworkPath + 'mimic.jpg')
    add_dir("[COLOR cyan]Choisir:[/COLOR] Skin Mimic [COLOR yellow](lr)[/COLOR]", 'GhantholinyMimic', artworkPath + 'mimic.jpg')
    add_dir("[COLOR lime]Lancer:[/COLOR] Skin Mimic [COLOR yellow](lr)[/COLOR]", 'ChangeSkinmimiclr', artworkPath + 'mimic.jpg')
    add_dir("[COLOR red]Maj HK2 et Skin sauvegarde[/COLOR]", 'menumajhk2', artworkPath + 'NETTOYER1.jpg')
    xbmcplugin.endOfDirectory(handle=__handle__, succeeded=True)

##############################################

# MENU CHOIX SKIN U2PLAY FanKai
def FanKai():
    #choix skin
    xbmcplugin.setPluginCategory(__handle__, "Choix skin [COLOR chartreuse]FanKai[/COLOR]")
    xbmcplugin.setContent(__handle__, 'files')
    add_dir("[COLOR cyan]u2Play[/COLOR] Skin FanKai[COLOR yellow][/COLOR]", 'FanKai', artworkPath + 'FanKai2.jpg')
    add_dir("[COLOR red]Maj HK2 et Skin sauvegarde[/COLOR]", 'menumajhk2', artworkPath + 'NETTOYER1.jpg')
    xbmcplugin.endOfDirectory(handle=__handle__, succeeded=True)

##############################################

# CHOIX SKIN VSTREAM
def vstream():
    #skin vstream
    xbmcplugin.setPluginCategory(__handle__, "Choix skin vStream")
    xbmcplugin.setContent(__handle__, 'files')
    add_dir("[COLOR red]Supprimer[/COLOR] les Anciens Codes Past de [COLOR green]vStream[/COLOR] Clic ici (supprime le setting)", 'suppast', artworkPath + 'icone.png')
    add_dir("[COLOR deepskyblue]Ajouter[/COLOR] Tous les Codes Past pour [COLOR green]vStream[/COLOR] Clic ici", 'choixpastall', artworkPath + 'icone.png')
    add_dir("Ou [COLOR deepskyblue]Ajouter[/COLOR] un Mix de Codes Past pour [COLOR green]vStream[/COLOR] Clic ici", 'choixpastmix', artworkPath + 'icone.png')
    add_dir("[COLOR deepskyblue]AJOUTER COMPTES PREMIUM ALEATOIRE CLIC ICI[/COLOR]", 'menuKey', artworkPath + 'icone.png')
    add_dir("[COLOR green]vStream[/COLOR] SKIN SUPER LIGHT [COLOR deepskyblue](le encore + leger)[/COLOR]", 'choixskinsuplitev', artworkPath + 'icone.png')
    add_dir("[COLOR green]vStream[/COLOR] SKIN LIGHT [COLOR deepskyblue](le + leger)[/COLOR]", 'choixskinlitev', artworkPath + 'icone.png')
    add_dir("[COLOR green]vStream[/COLOR] SKIN FULL [COLOR deepskyblue](le + gourmand)[/COLOR]", 'choixskinfullv', artworkPath + 'icone.png')
    add_dir("[COLOR green]vStream[/COLOR] SKIN KIDS [COLOR deepskyblue](special enfants)[/COLOR]", 'choixskinkidsv', artworkPath + 'icone.png')
    xbmcplugin.endOfDirectory(handle=__handle__, succeeded=True)

##############################################

# SUPPRIMER LES ANCIENS CODES PAST
def suppast():
    xbmc.executebuiltin("Notification(OPTION DE VSTREAM,Effacement en cours...)")
    # suppression du setting de vstream
    # nous devrions vérifier si le fichier existe ou non avant de le supprimer.
    if os.path.isfile(xbmc.translatePath('special://home/userdata/addon_data/plugin.video.vstream/settings.xml')):
        os.remove(xbmc.translatePath('special://home/userdata/addon_data/plugin.video.vstream/settings.xml'))
    else:
        print("Impossible de supprimer le fichier car il n'existe pas")
    xbmc.sleep(2000)
    xbmc.executebuiltin("Notification(Setting Vstream,Supprimé...)")

##############################################

# AJOUTER TOUS LES CODES PAST
def importpastall():
    #past all
    addon = xbmcaddon.Addon("plugin.video.vstream")
    meta_view = "true"
    addon.setSetting(id="meta-view", value=meta_view)
    pastebin_id_1 = "GQgyuquo8"
    addon.setSetting(id="pastebin_id_1", value=pastebin_id_1)
    pastebin_id_1_1 = "qNtuqy4w3"
    addon.setSetting(id="pastebin_id_1_1", value=pastebin_id_1_1)
    pastebin_id_1_2 = "6JK958n64"
    addon.setSetting(id="pastebin_id_1_2", value=pastebin_id_1_2)
    pastebin_id_2 = "CuSaw6GX9"
    addon.setSetting(id="pastebin_id_2", value=pastebin_id_2)
    pastebin_id_2_1 = "wud76FvV2"
    addon.setSetting(id="pastebin_id_2_1", value=pastebin_id_2_1)
    pastebin_id_2_2 = "rAYRYTfJ3"
    addon.setSetting(id="pastebin_id_2_2", value=pastebin_id_2_2)
    pastebin_id_3 = "yaA3sIezf"
    addon.setSetting(id="pastebin_id_3", value=pastebin_id_3)
    pastebin_id_3_1 = "V98AXTbyc"
    addon.setSetting(id="pastebin_id_3_1", value=pastebin_id_3_1)
    pastebin_id_4 = "cZEyUDCnb"
    addon.setSetting(id="pastebin_id_4", value=pastebin_id_4)
    pastebin_id_4_1 = "19kQJVf4f"
    addon.setSetting(id="pastebin_id_4_1", value=pastebin_id_4_1)
    pastebin_id_5 = "y3duNqoM1"
    addon.setSetting(id="pastebin_id_5", value=pastebin_id_5)
    pastebin_id_6 = "0cwaTCkid"
    addon.setSetting(id="pastebin_id_6", value=pastebin_id_6)
    pastebin_id_7 = "vyMOtqrNf"
    addon.setSetting(id="pastebin_id_7", value=pastebin_id_7)
    pastebin_id_7_1 = "7FjFI8FJ4"
    addon.setSetting(id="pastebin_id_7_1", value=pastebin_id_7_1)
    pastebin_id_8 = "fxPLhFDe5"
    addon.setSetting(id="pastebin_id_8", value=pastebin_id_8)
    pastebin_id_9 = "2Vc6sZW21"
    addon.setSetting(id="pastebin_id_9", value=pastebin_id_9)
    pastebin_label_1 = "1 Films"
    addon.setSetting(id="pastebin_label_1", value=pastebin_label_1)
    pastebin_label_2 = "2 Series"
    addon.setSetting(id="pastebin_label_2", value=pastebin_label_2)
    pastebin_label_3 = "3 Dessin Animes"
    addon.setSetting(id="pastebin_label_3", value=pastebin_label_3)
    pastebin_label_4 = "4 Docs"
    addon.setSetting(id="pastebin_label_4", value=pastebin_label_4)
    pastebin_label_5 = "5 Concert"
    addon.setSetting(id="pastebin_label_5", value=pastebin_label_5)
    pastebin_label_6 = "6 Spectacle"
    addon.setSetting(id="pastebin_label_6", value=pastebin_label_6)
    pastebin_label_7 = "7 Animés"
    addon.setSetting(id="pastebin_label_7", value=pastebin_label_7)
    pastebin_label_8 = "8 Sport"
    addon.setSetting(id="pastebin_label_8", value=pastebin_label_8)
    pastebin_label_9 = "9 Adultes"
    addon.setSetting(id="pastebin_label_9", value=pastebin_label_9)
    pastebin_id_10 = "bE9gqAb10"
    addon.setSetting(id="pastebin_id_10", value=pastebin_id_10)
    pastebin_id_11 = "pnm949oQ3"
    addon.setSetting(id="pastebin_id_11", value=pastebin_id_11)
    pastebin_id_12 = "hEAy2BsY0"
    addon.setSetting(id="pastebin_id_12", value=pastebin_id_12)
    pastebin_id_13 = "5XBJXBI80"
    addon.setSetting(id="pastebin_id_13", value=pastebin_id_13)
    pastebin_label_10 = "widget films"
    addon.setSetting(id="pastebin_label_10", value=pastebin_label_10)
    pastebin_label_11 = "widget series"
    addon.setSetting(id="pastebin_label_11", value=pastebin_label_11)
    pastebin_label_12 = "widget docs"
    addon.setSetting(id="pastebin_label_12", value=pastebin_label_12)
    pastebin_label_13 = "widgets dessin animé"
    addon.setSetting(id="pastebin_label_13", value=pastebin_label_13)
    pastebin_nbItemParPage = "30"
    addon.setSetting(id="pastebin_nbItemParPage", value=pastebin_nbItemParPage)
    showInfoNotification("Ajout Past All ok")

##############################################

# AJOUTER UN MIX DE CODES PAST
def importpastmix():
    #past Mix
    addon = xbmcaddon.Addon("plugin.video.vstream")
    meta_view = "true"
    addon.setSetting(id="meta-view", value=meta_view)
    pastebin_id_1 = "txDUtOdte"
    addon.setSetting(id="pastebin_id_1", value=pastebin_id_1)
    pastebin_id_1_1 = "qsJ1OBfk4"
    addon.setSetting(id="pastebin_id_1_1", value=pastebin_id_1_1)
    pastebin_id_1_2 = "8oEErrWMe"
    addon.setSetting(id="pastebin_id_1_2", value=pastebin_id_1_2)
    pastebin_id_2 = "pVuIECFkc"
    addon.setSetting(id="pastebin_id_2", value=pastebin_id_2)
    pastebin_id_2_1 = "V0I1z8qAd"
    addon.setSetting(id="pastebin_id_2_1", value=pastebin_id_2_1)
    pastebin_id_2_2 = "sDZaHTsPd"
    addon.setSetting(id="pastebin_id_2_2", value=pastebin_id_2_2)
    pastebin_id_3 = "2KicsN7Le"
    addon.setSetting(id="pastebin_id_3", value=pastebin_id_3)
    pastebin_id_3_1 = "8IAzteea1"
    addon.setSetting(id="pastebin_id_3_1", value=pastebin_id_3_1)
    pastebin_id_4 = "I3UK5AW70"
    addon.setSetting(id="pastebin_id_4", value=pastebin_id_4)
    pastebin_id_4_1 = "qKh2NIJoc"
    addon.setSetting(id="pastebin_id_4_1", value=pastebin_id_4_1)
    pastebin_id_5 = "w7wG1JDca"
    addon.setSetting(id="pastebin_id_5", value=pastebin_id_5)
    pastebin_id_6 = "KXFQXaIQ0"
    addon.setSetting(id="pastebin_id_6", value=pastebin_id_6)
    pastebin_id_7 = "WpwoNm177"
    addon.setSetting(id="pastebin_id_7", value=pastebin_id_7)
    pastebin_id_7_1 = "W9Ozl7nXb"
    addon.setSetting(id="pastebin_id_7_1", value=pastebin_id_7_1)
    pastebin_id_8 = "fxPLhFDe5"
    addon.setSetting(id="pastebin_id_8", value=pastebin_id_8)
    pastebin_id_9 = "2Vc6sZW21"
    addon.setSetting(id="pastebin_id_9", value=pastebin_id_9)
    pastebin_label_1 = "1 Films"
    addon.setSetting(id="pastebin_label_1", value=pastebin_label_1)
    pastebin_label_2 = "2 Series"
    addon.setSetting(id="pastebin_label_2", value=pastebin_label_2)
    pastebin_label_3 = "3 Dessin Animes"
    addon.setSetting(id="pastebin_label_3", value=pastebin_label_3)
    pastebin_label_4 = "4 Docs"
    addon.setSetting(id="pastebin_label_4", value=pastebin_label_4)
    pastebin_label_5 = "5 Concert"
    addon.setSetting(id="pastebin_label_5", value=pastebin_label_5)
    pastebin_label_6 = "6 Spectacle"
    addon.setSetting(id="pastebin_label_6", value=pastebin_label_6)
    pastebin_label_7 = "7 Animés"
    addon.setSetting(id="pastebin_label_7", value=pastebin_label_7)
    pastebin_label_8 = "8 Sport"
    addon.setSetting(id="pastebin_label_8", value=pastebin_label_8)
    pastebin_label_9 = "9 Adultes"
    addon.setSetting(id="pastebin_label_9", value=pastebin_label_9)
    pastebin_id_10 = "bE9gqAb10"
    addon.setSetting(id="pastebin_id_10", value=pastebin_id_10)
    pastebin_id_11 = "pnm949oQ3"
    addon.setSetting(id="pastebin_id_11", value=pastebin_id_11)
    pastebin_id_12 = "hEAy2BsY0"
    addon.setSetting(id="pastebin_id_12", value=pastebin_id_12)
    pastebin_id_13 = "5XBJXBI80"
    addon.setSetting(id="pastebin_id_13", value=pastebin_id_13)
    pastebin_label_10 = "widget films"
    addon.setSetting(id="pastebin_label_10", value=pastebin_label_10)
    pastebin_label_11 = "widget series"
    addon.setSetting(id="pastebin_label_11", value=pastebin_label_11)
    pastebin_label_12 = "widget docs"
    addon.setSetting(id="pastebin_label_12", value=pastebin_label_12)
    pastebin_label_13 = "widgets dessin animé"
    addon.setSetting(id="pastebin_label_13", value=pastebin_label_13)
    pastebin_nbItemParPage = "30"
    addon.setSetting(id="pastebin_nbItemParPage", value=pastebin_nbItemParPage)
    showInfoNotification("Ajout Past Mix ok")

##############################################

# IMPORT CHOIX SKIN
def importSkin(zipurl):
    # suppression dossier temporaire
    xbmc.executebuiltin("Notification(DOSSIER TEMP,Effacement en cours...)")
    dirPath = xbmc.translatePath('special://home/temp/temp/')
    try:
       shutil.rmtree(dirPath)
    except:
       print('Error while deleting directory')
    xbmc.sleep(1000)
    # telechargement et extraction du zip
    with urlopen(zipurl) as zipresp:
        with ZipFile(BytesIO(zipresp.read())) as zfile:
            zfile.extractall(xbmc.translatePath('special://home/temp/temp/'))
    # copie des fichiers extraie
    source_dir = xbmc.translatePath('special://home/temp/temp/addon_data')
    destination_dir = xbmc.translatePath('special://home/userdata/addon_data')
    source_dir2 = xbmc.translatePath('special://home/temp/temp/addons')
    destination_dir2 = xbmc.translatePath('special://home/addons')
    shutil.copytree(source_dir, destination_dir, dirs_exist_ok=True)
    shutil.copytree(source_dir2, destination_dir2, dirs_exist_ok=True)
    xbmc.executebuiltin("Notification(COPIE SKIN OK,Faites retour et profitez !)")
    xbmc.sleep(2000)

##############################################

# MENU SAUVEGARDE RESTAURATION
def save_restor():
    #menu sauvegarde restauration
    xbmcplugin.setPluginCategory(__handle__, "[COLOR magenta]Sauvegarde et restauration[/COLOR]")
    xbmcplugin.setContent(__handle__, 'files')
    add_dir("[COLOR lime]1 CREER UNE SAUVEGARDE : [/COLOR]", 'skin_save1', artworkPath + 'save.png')
    add_dir("Skin Arctic Horizon 2", 'skin_save1', artworkPath + 'icon (AH2).png')
    add_dir("Skin Rayflix", 'skin_save2', artworkPath + 'icon (Ray).png')
    add_dir("Emplacement 3", 'skin_save3', artworkPath + 'save.png')
    add_dir("[COLOR red]2 RESTAURER UNE SAUVEGARDE : [/COLOR]", 'skin_restor1', artworkPath + 'restaurer.jpg')
    add_dir("Skin Arctic Horizon 2", 'skin_restor1', artworkPath + 'icon (AH2).png')
    add_dir("Skin Rayflix", 'skin_restor2', artworkPath + 'icon (Ray).png')
    add_dir("Emplacement 3", 'skin_restor3', artworkPath + 'restaurer.jpg')
    xbmcplugin.endOfDirectory(handle=__handle__, succeeded=True)  

##############################################

# SAUVEGARDE
def skin_save1():
    xbmc.executebuiltin("Notification(PREPARATION DES FICHIERS,Copie en cours...)")
    # COPIE DES DOSSIERS ET FICHIERS DU SKIN
    source_dir = xbmc.translatePath('special://home/userdata/addon_data/skin.arctic.horizon.2')
    destination_dir = xbmc.translatePath('special://home/userdata/addon_data/Scripts/Skin_save/1/addon_data')
    source_dir1 = xbmc.translatePath('special://home/userdata/addon_data/script.skinshortcuts')
    destination_dir1 = xbmc.translatePath('special://home/userdata/addon_data/Scripts/Skin_save/1/addon_data/script.skinshortcuts')
    source_dir2 = xbmc.translatePath('special://home/addons/skin.project.aura/1080i/script-skinshortcuts-includes.xml')
    destination_dir2 = xbmc.translatePath('special://home/userdata/addon_data/Scripts/Skin_save/1/addons/skin.project.aura/1080i/script-skinshortcuts-includes.xml')
    shutil.copytree(source_dir, destination_dir, dirs_exist_ok=True)
    shutil.copytree(source_dir1, destination_dir1, dirs_exist_ok=True)
    shutil.copy(source_dir2, destination_dir2)
    # CREATION ARCHIVE ZIP
    shutil.make_archive((xbmc.translatePath('special://home/userdata/addon_data/Scripts/Skin_save/Skin_save1')),'zip',(xbmc.translatePath('special://home/userdata/addon_data/Scripts/Skin_save/1')))
    xbmc.executebuiltin("Notification(SKIN SAUVEGARDE, Archive ZIP créée !)")
    sys.exit()

def skin_save2():
    xbmc.executebuiltin("Notification(PREPARATION DES FICHIERS,Copie en cours...)")
    # COPIE DES DOSSIERS ET FICHIERS DU SKIN
    source_dir = xbmc.translatePath('special://home/userdata/addon_data/skin.project.aura')
    destination_dir = xbmc.translatePath('special://home/userdata/addon_data/Scripts/Skin_save/2/addon_data/skin.project.aura')
    source_dir1 = xbmc.translatePath('special://home/userdata/addon_data/script.skinshortcuts')
    destination_dir1 = xbmc.translatePath('special://home/userdata/addon_data/Scripts/Skin_save/2/addon_data/script.skinshortcuts')
    source_dir2 = xbmc.translatePath('special://home/addons/skin.project.aura/1080i/script-skinshortcuts-includes.xml')
    destination_dir2 = xbmc.translatePath('special://home/userdata/addon_data/Scripts/Skin_save/2/addons/skin.project.aura/1080i/script-skinshortcuts-includes.xml')
    shutil.copytree(source_dir, destination_dir, dirs_exist_ok=True)
    shutil.copytree(source_dir1, destination_dir1, dirs_exist_ok=True)
    shutil.copy(source_dir2, destination_dir2)
    # CREATION ARCHIVE ZIP
    shutil.make_archive((xbmc.translatePath('special://home/userdata/addon_data/Scripts/Skin_save/Skin_save1')),'zip',(xbmc.translatePath('special://home/userdata/addon_data/Scripts/Skin_save/2')))
    xbmc.executebuiltin("Notification(SKIN SAUVEGARDE, Archive ZIP créée !)")
    sys.exit()

def skin_save3():
    xbmc.executebuiltin("Notification(PREPARATION DES FICHIERS,Copie en cours...)")
    # COPIE DES DOSSIERS ET FICHIERS DU SKIN
    source_dir = xbmc.translatePath('special://home/userdata/addon_data/skin.project.aura')
    destination_dir = xbmc.translatePath('special://home/userdata/addon_data/Scripts/Skin_save/3/addon_data/skin.project.aura')
    source_dir1 = xbmc.translatePath('special://home/userdata/addon_data/script.skinshortcuts')
    destination_dir1 = xbmc.translatePath('special://home/userdata/addon_data/Scripts/Skin_save/3/addon_data/script.skinshortcuts')
    source_dir2 = xbmc.translatePath('special://home/addons/skin.project.aura/1080i/script-skinshortcuts-includes.xml')
    destination_dir2 = xbmc.translatePath('special://home/userdata/addon_data/Scripts/Skin_save/3/addons/skin.project.aura/1080i/script-skinshortcuts-includes.xml')
    shutil.copytree(source_dir, destination_dir, dirs_exist_ok=True)
    shutil.copytree(source_dir1, destination_dir1, dirs_exist_ok=True)
    shutil.copy(source_dir2, destination_dir2)
    # CREATION ARCHIVE ZIP
    shutil.make_archive((xbmc.translatePath('special://home/userdata/addon_data/Scripts/Skin_save/Skin_save1')),'zip',(xbmc.translatePath('special://home/userdata/addon_data/Scripts/Skin_save/3')))
    xbmc.executebuiltin("Notification(SKIN SAUVEGARDE, Archive ZIP créée !)")
    sys.exit()

##############################################

# RESTAURATION
def skin_restor1():
    # copie des fichiers sauvegarde
    source_dir = xbmc.translatePath('special://home/userdata/addon_data/Scripts/Skin_save/1/addon_data')
    destination_dir = xbmc.translatePath('special://home/userdata/addon_data')
    source_dir2 = xbmc.translatePath('special://home/userdata/addon_data/Scripts/Skin_save/1/addons/skin.project.aura')
    destination_dir2 = xbmc.translatePath('special://home/addons/skin.project.aura')
    shutil.copytree(source_dir, destination_dir, dirs_exist_ok=True)
    shutil.copytree(source_dir2, destination_dir2, dirs_exist_ok=True)
    xbmc.executebuiltin("Notification(COPIE OK,Mise à jour effectuée !)")
    xbmc.sleep(5000)
    # actualisation du skin
    xbmc.executebuiltin("Notification(ACTUALISATION DU SKIN, Skin Save 1...)")
    xbmc.sleep(2000)
    xbmc.executebuiltin('ReloadSkin')
    sys.exit()

def skin_restor2():
    # copie des fichiers sauvegarde
    source_dir = xbmc.translatePath('special://home/userdata/addon_data/Scripts/Skin_save/2/addon_data')
    destination_dir = xbmc.translatePath('special://home/userdata/addon_data')
    source_dir2 = xbmc.translatePath('special://home/userdata/addon_data/Scripts/Skin_save/2/addons/skin.project.aura')
    destination_dir2 = xbmc.translatePath('special://home/addons/skin.project.aura')
    shutil.copytree(source_dir, destination_dir, dirs_exist_ok=True)
    shutil.copytree(source_dir2, destination_dir2, dirs_exist_ok=True)
    xbmc.executebuiltin("Notification(COPIE OK,Mise à jour effectuée !)")
    xbmc.sleep(5000)
    # actualisation du skin
    xbmc.executebuiltin("Notification(ACTUALISATION DU SKIN, Skin Save 2...)")
    xbmc.sleep(2000)
    xbmc.executebuiltin('ReloadSkin')
    sys.exit()

def skin_restor3():
    # copie des fichiers sauvegarde
    source_dir = xbmc.translatePath('special://home/userdata/addon_data/Scripts/Skin_save/3/addon_data')
    destination_dir = xbmc.translatePath('special://home/userdata/addon_data')
    source_dir2 = xbmc.translatePath('special://home/userdata/addon_data/Scripts/Skin_save/3/addons/skin.project.aura')
    destination_dir2 = xbmc.translatePath('special://home/addons/skin.project.aura')
    shutil.copytree(source_dir, destination_dir, dirs_exist_ok=True)
    shutil.copytree(source_dir2, destination_dir2, dirs_exist_ok=True)
    xbmc.executebuiltin("Notification(COPIE OK,Mise à jour effectuée !)")
    xbmc.sleep(5000)
    # actualisation du skin
    xbmc.executebuiltin("Notification(ACTUALISATION DU SKIN, Skin Save 3...)")
    xbmc.sleep(2000)
    xbmc.executebuiltin('ReloadSkin')
    sys.exit()

##############################################

# MENU MAJ DATABASE
def menumajhk2():
    # menu maj
    xbmcplugin.setPluginCategory(__handle__, "[COLOR yellow]Mise a Jour Database HK2[/COLOR]")
    xbmcplugin.setContent(__handle__, 'files')
    add_dir("[COLOR yellow]1 - M.A.J HK2 et Skin rafraichissement[/COLOR]", 'forcermaj', artworkPath + 'fanart (U2P).jpg')
    add_dir("[COLOR yellow]2 - M.A.J HK2 seulement (rapide)[/COLOR]", 'actuskin', artworkPath + 'fanart (U2P).jpg')
    #add_dir("[COLOR red]En cas de soucis [/COLOR][COLOR deepskyblue]CHANGER COMPTES PREMIUM ALEATOIRE[/COLOR]", 'menuKey', artworkPath + 'icone.png')
    add_dir("--- [COLOR magenta]Sauvegarde des Skins[/COLOR] ---", 'save_restor', artworkPath + 'save.png')
    add_dir("--- [COLOR deepskyblue]Menu Nettoyage[/COLOR][COLOR red](Attention !!!)[/COLOR]---", 'nettoye', artworkPath + 'cleaning-thumbnail.png')
    #add_dir("SKIN FULL [COLOR deepskyblue](le + gourmand)[/COLOR]", 'hk2full', artworkPath + 'icone.png')
    #add_dir("SKIN KIDS [COLOR deepskyblue](special enfants)[/COLOR]", 'hk2kids', artworkPath + 'icone.png')
    #add_dir("SKIN RETRO [COLOR deepskyblue](pour les nostalgiques)[/COLOR]", 'hk2retro', artworkPath + 'icone.png')
    xbmcplugin.endOfDirectory(handle=__handle__, succeeded=True)  

def forcermaj():
    # forcer maj
    xbmc.executebuiltin('RunScript(special://home/addons/service.U2PplayMaj/U2PplayFast.py,True)') 
    
def actuskin():
    # actualiser 
    xbmc.executebuiltin('RunScript(special://home/addons/service.U2PplayMaj/U2Pplay.py,True)')

##############################################

# MENU NETTOYAGE
def nettoye():
    #menu nettoyage
    xbmcplugin.setPluginCategory(__handle__, "Nettoyer Kodi")
    xbmcplugin.setContent(__handle__, 'files')
    add_dir("[COLOR red]Nettoyer tout : [/COLOR](un clic)", 'vider_cache', artworkPath + 'NETTOYER.png')
    add_dir("[COLOR deepskyblue]Vider Cache uniquement[/COLOR]", 'cache_seul', artworkPath + 'cleaning-thumbnail.png')
    add_dir("[COLOR deepskyblue]Vider Tmp uniquement[/COLOR]", 'tmp_seul', artworkPath + 'cleaning-icon.jpg')
    add_dir("[COLOR deepskyblue]Vider Packages uniquement[/COLOR]", 'package_seul', artworkPath + 'NETTOYER1.jpg')
    add_dir("[COLOR deepskyblue]Vider Thumbnails uniquement[/COLOR]", 'thumb_seul', artworkPath + '2771509.png')
    xbmcplugin.endOfDirectory(handle=__handle__, succeeded=True)  

##############################################

# NETTOYER TOUT D UN COUP
def vider_cache():
    #nettoyer tout
    xbmc.executebuiltin("Notification(FICHIER TEMP,Effacement en cours...)")
    # suppression dossier temporaire
    dirPath = xbmc.translatePath('special://home/temp/temp/')
    try:
       shutil.rmtree(dirPath)
    except:
       print('Error while deleting directory')
    xbmc.sleep(1000)
    xbmc.executebuiltin("Notification(DOSSIER PACKAGES,Effacement en cours...)")
    # suppression dossier packages
    dirPath = xbmc.translatePath('special://home/addons/packages/')
    try:
       shutil.rmtree(dirPath)
    except:
       print('Error while deleting directory')
    xbmc.sleep(1000)
    xbmc.executebuiltin("Notification(DOSSIER THUMBNAILS,Effacement en cours...)")
    # suppression dossier thumbnails
    dirPath = xbmc.translatePath('special://home/userdata/Thumbnails/')
    try:
       shutil.rmtree(dirPath)
    except:
       print('Error while deleting directory')
    xbmc.sleep(1000)
    xbmc.executebuiltin("Notification(CACHE TEMP,Effacement en cours...)")
    # suppression dossier cache
    dirPath = xbmc.translatePath('special://home/cache/temp/')
    try:
       shutil.rmtree(dirPath)
    except:
       print('Error while deleting directory')
    xbmc.sleep(1000)
    # actualisation du skin
    xbmc.executebuiltin("Notification(ATTENTION KODI VA SE FERMER , Relancez le...)")
    xbmc.sleep(2000)
    xbmc.executebuiltin('ReloadSkin')
    xbmc.sleep(2000)
    xbmc.executebuiltin('Quit')

##############################################

# VIDER CACHE
def cache_seul():
    #nettoyaer cache uniquement
    xbmc.executebuiltin("Notification(CACHE TEMP,Effacement en cours...)")
    # suppression dossier cache
    dirPath = xbmc.translatePath('special://home/cache/temp/')
    try:
       shutil.rmtree(dirPath)
    except:
       print('Error while deleting directory')
    xbmc.sleep(1000)
    # actualisation du skin
    xbmc.executebuiltin("Notification(TERMINE , ...)")
    xbmc.sleep(2000)
    xbmc.executebuiltin('ReloadSkin')

##############################################

# VIDER TMP
def tmp_seul():
    #nettoyaer tmp uniquement
    xbmc.executebuiltin("Notification(FICHIER TEMP,Effacement en cours...)")
    # suppression dossier temporaire
    dirPath = xbmc.translatePath('special://home/temp/temp/')
    try:
       shutil.rmtree(dirPath)
    except:
       print('Error while deleting directory')
    xbmc.sleep(1000)
    xbmc.executebuiltin("Notification(TERMINE , ...)")
    # actualisation du skin
    xbmc.sleep(2000)
    xbmc.executebuiltin('ReloadSkin')

##############################################

# VIDER PACKAGES    
def package_seul():
    #nettoyaer packages uniquement
    xbmc.executebuiltin("Notification(DOSSIER PACKAGES,Effacement en cours...)")
    # suppression dossier packages
    dirPath = xbmc.translatePath('special://home/addons/packages/')
    try:
       shutil.rmtree(dirPath)
    except:
       print('Error while deleting directory')
    xbmc.sleep(1000)
    # actualisation du skin
    xbmc.executebuiltin("Notification(TERMINE , ...)")
    xbmc.sleep(2000)
    xbmc.executebuiltin('ReloadSkin')

##############################################

# VIDER THUMBNAILS
def thumb_seul():
    #nettoyaer thumbnails uniquement
    xbmc.executebuiltin("Notification(DOSSIER THUMBNAILS,Effacement en cours...)")
    # suppression dossier thumbnails
    dirPath = xbmc.translatePath('special://home/userdata/Thumbnails/')
    try:
       shutil.rmtree(dirPath)
    except:
       print('Error while deleting directory')
    xbmc.sleep(1000)
    # actualisation du skin
    xbmc.executebuiltin("Notification(ATTENTION KODI VA SE FERMER , Relancez le...)")
    xbmc.sleep(2000)
    xbmc.executebuiltin('ReloadSkin')
    xbmc.sleep(2000)
    xbmc.executebuiltin('Quit')

##############################################

# LANCER SKIN :

# AH2 COKODICO
def ChangeSkinAH2CoKo():
    xbmc.executebuiltin('RunScript(special://home/addons/plugin.program.Skodi/resources/testprofileskinAH2CoKodico.py)')
# Bingie COKODICO
def ChangeSkinbingieCoKo():
    xbmc.executebuiltin('RunScript(special://home/addons/plugin.program.Skodi/resources/testprofileskinbingieCoKodico.py)')
# CoKopacetic COKODICO
def ChangeSkincopacetiCoKo():
    xbmc.executebuiltin('RunScript(special://home/addons/plugin.program.Skodi/resources/testprofileskin.copacetiCoKodico.py)')
# AeonMQ8 COKODICO
def ChangeSkinAeonMQ8CoKo():
    xbmc.executebuiltin('RunScript(special://home/addons/plugin.program.Skodi/resources/testprofileskinaeonmq8matrixmodCoKodico.py)')  
# ChangeSkin-skin.auramod bePurple
def ChangeSkinskinauramod():
    xbmc.executebuiltin('RunScript(special://home/addons/plugin.program.Skodi/resources/ChangeSkin-skin.auramod.py)') 
# ChangeSkin-luc562
def ChangeSkinaeonnoxsilvo():
    xbmc.executebuiltin('RunScript(special://home/addons/plugin.program.Skodi/resources/ChangeSkin-skin.aeon.nox.silvo.py)') 
def ChangeSkinmimiclr():
    xbmc.executebuiltin('RunScript(special://home/addons/plugin.program.Skodi/resources/ChangeSkin-skin.mimic.lr.py)')
# ChangeSkin-Ghantholiny
def ChangeSkinarctichorizon():
    xbmc.executebuiltin('RunScript(special://home/addons/plugin.program.Skodi/resources/ChangeSkin-skin.arctic.horizon.py)') 
# ChangeSkin-ProjectAura
def ChangeSkinsProjectAura():
    xbmc.executebuiltin('RunScript(special://home/addons/plugin.program.Skodi/resources/ChangeSkin-skin.project.aura.py)')
    
##############################################

def router(paramstring):
    params = dict(parse_qsl(paramstring))    
    dictActions = {
        #key uptobox
        'menuKey':(menuKey, ""),
        #skin
        'choixpastmix': (importpastmix, ""),
        'choixpastall': (importpastall, ""),
        'choixskinlite': (importSkin, 'https://github.com/prf2/pack/raw/kodi/u_light.zip'),
        'choixskinfull': (importSkin, 'https://github.com/prf2/pack/raw/kodi/u_full.zip'),
        'choixskinkids': (importSkin, 'https://github.com/prf2/pack/raw/kodi/u_kids.zip'),
        'choixskinsuplitev': (importSkin, 'https://github.com/prf2/pack/raw/kodi/v_super_lite.zip'),
        'choixskinlitev': (importSkin, 'https://github.com/prf2/pack/raw/kodi/v_light.zip'),
        'choixskinfullv': (importSkin, 'https://github.com/prf2/pack/raw/kodi/v_full.zip'),
        'choixskinkidsv': (importSkin, 'https://github.com/prf2/pack/raw/kodi/v_kids.zip'),
        'hk2lite': (importSkin, 'https://github.com/prf2/pack/raw/kodi/hk2_light.zip'),
        'hk2full': (importSkin, 'https://github.com/prf2/pack/raw/kodi/hk2_full.zip'),
        'hk2kids': (importSkin, 'https://github.com/prf2/pack/raw/kodi/hk2_kids.zip'),
        'hk2leger': (importSkin, 'https://github.com/prf2/pack/raw/kodi/hk2_light.zip'),
        'hk2complet': (importSkin, 'https://github.com/prf2/pack/raw/kodi/hk2_full.zip'),
        'hk2enfants': (importSkin, 'https://github.com/prf2/pack/raw/kodi/hk2_kids.zip'),
        'hk2retro': (importSkin, 'https://github.com/prf2/pack/raw/kodi/hk2_retro.zip'),
        'hk2AH2': (importSkin, 'https://upkobox.github.io/Skodi/SKIN/AH2_HK2.zip'),
        'titanbingieCoKo': (importSkin, 'https://upkobox.github.io/Skodi/SKIN/Skin_Titan_BINGIE_MOD.zip'),
        'SkinCoKopacetic': (importSkin, 'https://upkobox.github.io/Skodi/SKIN/Skin_Copacetic.zip'), 
        'MQ8': (importSkin, 'https://github.com/UpKobox/Skodi/raw/main/SKIN/Skin_Aeon_MQ_8.zip'), 
        'bePurpleAH2': (importSkin, 'https://github.com/UpKobox/Skodi/raw/main/SKIN/bePurple/skin.arctic.horizon.2.zip'),
        'bePurpleAuraKid': (importSkin, 'https://upkobox.github.io/Skodi/SKIN/bePurple/skin.auramod.enfant.zip'),
        'bePurpleAura': (importSkin, 'https://upkobox.github.io/Skodi/SKIN/bePurple/skin.auramod.zip'),
        'Luc562AH2': (importSkin, 'https://github.com/UpKobox/Skodi/raw/main/SKIN/luc562/skin.arctic.horizon.2.zip'),   
        'Luc562Aeon': (importSkin, 'https://upkobox.github.io/Skodi/SKIN/luc562/skin.aeon.nox.silvo.zip'),
        'Luc562Mimic': (importSkin, 'https://upkobox.github.io/Skodi/SKIN/luc562/skin.mimic.lr.zip'),
        'pistachePoilueAH2': (importSkin, 'https://github.com/UpKobox/Skodi/raw/main/SKIN/pistachePoilue/skin.arctic.horizon.2.zip'),   
        'GhantholinyAH': (importSkin, 'https://upkobox.github.io/Skodi/SKIN/Ghantholiny/skin.arctic.horizon.zip'), 
        'GhantholinyMimic': (importSkin, 'https://upkobox.github.io/Skodi/SKIN/Ghantholiny/sin.mimic.lr.zip'), 
        'FanKai': (importSkin, 'https://upkobox.github.io/Skodi/SKIN/FanKai/fankai.zip'),
        'ChangeSkinAH2CoKo': (ChangeSkinAH2CoKo, ""), 
        'ChangeSkinsProjectAura': (ChangeSkinsProjectAura, ""),
        'ChangeSkinbingieCoKo': (ChangeSkinbingieCoKo, ""),
        'ChangeSkincopacetiCoKo': (ChangeSkincopacetiCoKo, ""),
        'ChangeSkinAeonMQ8CoKo': (ChangeSkinAeonMQ8CoKo, ""),
        'ChangeSkinskinauramod': (ChangeSkinskinauramod, ""),
        'ChangeSkinaeonnoxsilvo': (ChangeSkinaeonnoxsilvo, ""),
        'ChangeSkinmimiclr': (ChangeSkinmimiclr, ""),
        'ChangeSkinarctichorizon': (ChangeSkinarctichorizon, ""),
        #skin hk
        'hk': (hk, ""),
        'hk2': (hk2, ""),
        'rayhk2': (rayhk2, ""),
        'CoKo': (CoKo, ""),
        'bePurple': (bePurple, ""),
        'Luc562': (Luc562, ""),
        'pistachePoilue': (pistachePoilue, ""),
        'Ghantholiny': (Ghantholiny, ""), 
        'FanKai': (FanKai, ""),               
        'db_auto': (db_auto, ""),
        'db_auto_no': (db_auto_no, ""),
        #skin vstream
        "suppast": (suppast, ""),
        "vstream": (vstream, ""),
        #maj hk2
        "menumajhk2": (menumajhk2, ""),
        "forcermaj": (forcermaj, ""),
        "actuskin": (actuskin, ""),
        #nettoyage
        'vider_cache': (vider_cache, ""),
        'cache_seul': (cache_seul, ""),
        'tmp_seul': (tmp_seul, ""),
        'package_seul': (package_seul, ""),
        'thumb_seul': (thumb_seul, ""),
        'nettoye': (nettoye, ""),
        #sauvegarde restauration
        'save_restor': (save_restor, ""),
        'skin_save1': (skin_save1, ""), 
        'skin_save2': (skin_save2, ""), 
        'skin_save3': (skin_save3, ""), 
        'skin_restor1': (skin_restor1, ""), 
        'skin_restor2': (skin_restor2, ""), 
        'skin_restor3': (skin_restor3, ""), 
        #autres
        #'ad_maj2': (ad_maj2, ""),
        'au_maj': (au_maj, ""),
        'au_majCoKo': (au_majCoKo, ""),
        'au_maj2': (au_maj2, ""),       
        'inst_tout': (inst_tout, ""),
        'inst_tout2': (inst_tout2, ""),
        'inst_add': (inst_add, ""),
        'inst_add2': (inst_add2, ""),
        'inst_act': (inst_act, ""),
        'inst_act2': (inst_act2, ""),
        'inst_quit': (inst_quit, ""),
        'inst_quit2': (inst_quit2, ""),
        'inst_skin': (inst_skin, ""),
        }
        
    if params:
        fn = params['action']
        if fn in dictActions.keys():
            argv = dictActions[fn][1]
            if argv:
                dictActions[fn][0](argv)
            else:
                dictActions[fn][0]()
        else:
            raise ValueError('Invalid paramstring: {0}!'.format(paramstring))
    else:
         main_menu()

if __name__ == '__main__':
    __addon__ = xbmcaddon.Addon("plugin.program.Skodi")
    __handle__ = int(sys.argv[1])
    router(sys.argv[2][1:])