# -*- coding: utf-8 -*-
import xbmc, xbmcaddon, xbmcgui
import requests, json 

Addon = xbmcaddon.Addon(id='plugin.video.movixws')
username = Addon.getSetting('username')
password = Addon.getSetting('password')

def login(movie_id):
    dialog = xbmcgui.Dialog()
    username = Addon.getSetting('username')
    password = Addon.getSetting('password')
    if username == "":
        ret = dialog.yesno("Movix.me", "אינך מחובר.", "האם ברצונך להתחבר בכדי לצפות בתכני פרימיום?")
        if ret:
            username = dialog.input("הכנס שם משתמש",type=xbmcgui.INPUT_ALPHANUM)
            password = dialog.input("הכנס סיסמא",type=xbmcgui.INPUT_ALPHANUM, option=xbmcgui.ALPHANUM_HIDE_INPUT)
        else:
            return False
    elif password == "":
        dialog.ok("Movix.me", "אינך מחובר.", "על מנת לצפות בתכני פרימיום עליך להתחבר.")
        password = dialog.input("הכנס סיסמא",type=xbmcgui.INPUT_ALPHANUM, option=xbmcgui.ALPHANUM_HIDE_INPUT)
    Addon.setSetting(id='username', value=username)
    Addon.setSetting(id='password', value=password)

    del dialog
    try:
        xbmc.log("http://movix.me/kodiapi.php?user=%s&pass=%s&postid=%s"%(username, password, movie_id) +"-"*50)
        res = requests.get("http://movix.me/kodiapi.php?user=%s&pass=%s&postid=%s"%(username, password, movie_id)).json()
        xbmc.executebuiltin("Notification(Movix.me,התחברת בהצלחה)")
        return res
    except Exception, e:
        xbmc.executebuiltin("Notification(Movix.me,ההתחברות נכשלה)")
        
        return False
