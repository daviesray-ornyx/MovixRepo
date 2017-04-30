# -*- coding: utf-8 -*-
import os, urllib, re, random, json, datetime, threading
import xbmcaddon, xbmc, xbmcplugin, xbmcgui

Addon = xbmcaddon.Addon(id='plugin.video.movixws')
addonPath = xbmc.translatePath(Addon.getAddonInfo("path")).decode("utf-8")
libDir = os.path.join(addonPath, 'resources', 'lib')
sys.path.insert(0, libDir)
import resolver, urlresolver, cloudflare, cache, ua, common, login , logg
addon_id     = 'plugin.video.movixws'
AddonName = Addon.getAddonInfo("name")
icon = Addon.getAddonInfo('icon')
FANART = os.path.join(addonPath, 'fanart.jpg')
Domain = Addon.getSetting("domain")
baseUrl = Domain[:-1] if Domain.endswith('/') else Domain
handle = int(sys.argv[1])
userAgent = Addon.getSetting("userAgent")
if userAgent == '':
	userAgent = ua.GetRandomUA()
	Addon.setSetting("userAgent", userAgent)

user_dataDir = xbmc.translatePath(Addon.getAddonInfo("profile")).decode("utf-8")
if not os.path.exists(user_dataDir):
	os.makedirs(user_dataDir)
logosDir = os.path.join(user_dataDir, "logos")
if not os.path.exists(logosDir):
	os.makedirs(logosDir)

def searchWs():
	search_entered = ''
	isText = False
	keyboard = xbmc.Keyboard(search_entered, 'הכנס מילות חיפוש כאן')
	keyboard.doModal()
	if keyboard.isConfirmed():
		search_entered = urllib.quote_plus(keyboard.getText())
	isText = False if search_entered.strip() == '' else True
	dialog = xbmcgui.Dialog()
	filter = dialog.select("בחר סוג חיפוש", ["הכל", "סרטים", "סדרות"])
	if filter == 1:
		search_entered += "&sortby=movie"
	elif filter == 2:
		search_entered += "&sortby=tv-show"
	isYear = False
	yearsRange = list((range(datetime.datetime.now().year, 1933, -1)))
	years = [str(year) for year in yearsRange]
	years.insert(0, "הכל")
	year = dialog.select("הצג תוצאות לפי שנה", years)
	if year != 0:
		search_entered += "&year={0}".format(years[year])
		isYear = True
	if isText or isYear:
		return IndexPage('{0}/search_movies?q={1}'.format(baseUrl, search_entered))
	else:
		return False

def searchWsP(typ):
	search_entered = ''
	isText = False
	keyboard = xbmc.Keyboard(search_entered, 'הכנס מילות חיפוש כאן')
	keyboard.doModal()
	if keyboard.isConfirmed():
		search_entered = urllib.quote_plus(keyboard.getText())
	isText = False if search_entered.strip() == '' else True
	if typ == '1':
		search_entered += "&sortby=movie"
	elif typ == '2':
		search_entered += "&sortby=tv-show"
	
	if isText :
		return IndexPageP('{0}/search_movies?q={1}'.format(baseUrl, search_entered))
	else:
		return False


def yearWs():
	search_entered = ''
	dialog = xbmcgui.Dialog()
	isYear = False
	yearsRange = list((range(datetime.datetime.now().year, 1933, -1)))
	years = [str(year) for year in yearsRange]
	year = dialog.select("הצג תוצאות לפי שנה", years)
	if year != '':
		search_entered += "&year={0}".format(years[year])
		xbmc.log(search_entered +"<test year<"*5)
		isYear = True
	if isYear:
		return IndexPageP('{0}/search_movies?q={1}'.format(baseUrl, search_entered))
	else:
		return False


def IndexPagePremium(url):
	if baseUrl+'/movies' == url:
		addDir('[COLOR orange][B] חיפוש [/B][/COLOR]','1',13,'https://encrypted-tbn1.gstatic.com/images?q=tbn:ANd9GcQlAUVuxDFwhHYzmwfhcUEBgQXkkWi5XnM4ZyKxGecol952w-Rp',FANART,True)
		addDir('[COLOR orange] מיון סרטים לפי שנה [/COLOR]',' ',11,'http://i.imgur.com/jIw6Zzh.png?1',FANART ,True)
		addDir('[COLOR orange] כל הסרטים שבאתר [/COLOR]',"{0}/movies".format(baseUrl),12,'http://noobsandnerds.com/addons/cache/Addons/plugin.video.moviereleases/icon.png',FANART,True)
		addDir('[COLOR orange] הסרטים הנצפים ביותר [/COLOR]','הסרטים הנצפים ביותר|עזרו לנו להמשיך להתקיים',9,'http://i.imgur.com/9jowwKu.png',FANART,True)
		addDir('[COLOR orange] סרטים שנוספו לאחרונה [/COLOR]','id="recent-movies"|<!--recent movies tab-->',9,'http://i.imgur.com/y9T5Peo.png',FANART,True)
		addDir('[COLOR orange] הסרטים המדורגים ביותר [/COLOR]','id="top-rated-movies"|<!--top tab-->',9,'http://i.imgur.com/7y1EqNG.png',FANART,True)
		addDir('[COLOR orange] סרטים עם הכי הרבה תגובות [/COLOR]','id="most-links-movies"|<!--most linked tab-->',9,'http://i.imgur.com/87uYwaK.png',FANART,True)
   		
        
		

	if baseUrl+'/series' == url:
		addDir('[COLOR orange][B] חיפוש [/B][/COLOR]','2',13,'https://encrypted-tbn1.gstatic.com/images?q=tbn:ANd9GcQlAUVuxDFwhHYzmwfhcUEBgQXkkWi5XnM4ZyKxGecol952w-Rp',FANART,True)
		addDir('[COLOR orange] כל הסדרות שבאתר [/COLOR]',"{0}/series".format(baseUrl),12,'https://farm6.staticflickr.com/5602/15700070751_88d83d38fd_o_d.png',FANART,True)
		addDir('[COLOR orange] הסדרות הנצפות ביותר [/COLOR]','id="most-views-tv-shows"|<!--most commented tab-->',9,'http://i.imgur.com/9jowwKu.png',FANART,True)
		addDir('[COLOR orange] סדרות שנוספו לאחרונה [/COLOR]','id="recent-tv-shows"|<!--recent tv shows-->',9,'http://i.imgur.com/y9T5Peo.png',FANART,True)
		addDir('[COLOR orange] הסדרות המדורגות ביותר [/COLOR]','id="top-rated-tv-shows"|<!--top tab-->',9,'http://i.imgur.com/7y1EqNG.png',FANART,True)
		addDir('[COLOR orange] סדרות עם הכי הרבה תגובות [/COLOR]','id="most-links-tv-shows"|<!--most linked tab-->',9,'http://i.imgur.com/87uYwaK.png',FANART,True)




def IndexPage(url):

	if not 'page' in url:
		if 'search_movies' in url:
			url = url + '&page=/0'
		else:
			url = url + '/page/0'

	current_page = int(url.split('/')[-1])

	for pageIndex in range(10):
		try:
			matches, last_page, step = cache.get(IndexPage_regex, 72, url, table='pages')
			for item in matches:
				name = item[3]
				if item[0].strip() != '':
					#name = '[COLOR red] למנויים[/COLOR] ' + name
					continue
				addDir(name, '{0}{1}'.format(baseUrl, item[2]), 4, item[1],FANART, True, item[4])
		except Exception as ex:
			xbmc.log(str(ex), 3)
		if current_page >= last_page:
			return True
		current_page += step
		url = url[:url.rfind('/')+1]
		url += str(current_page)

	if current_page <= last_page:
		addDir('[COLOR blue]תוצאות נוספות[/COLOR]', url, 2, '','')
	return True


def IndexPage_regex(url):
	result, cookie = cloudflare.request(url)
	last_page, step = GetPagegSteps(result, int(url.split('/')[-1]))
	matches = re.compile('<div id="movie\d+" class="ic_container">\s+(.*?)<img src="(.*?)".*?<h3><a href="(.*?)">(.*?)<.*?<p class="ic_text">\s+(.*?)\s+<\/p>',re.S).findall(result)
	showImages = Addon.getSetting('showImages') == 'true'
	list=[]
	for match in matches:
		if match[0].strip() != '':
			continue
		if showImages:
			try:
				logoUrl = match[1]
				logoFile = os.path.join(logosDir, logoUrl[logoUrl.rfind('/')+1:])
				if not os.path.isfile(logoFile):
					threading.Thread(target=getImageLinkBackground, args=(logoUrl, logoFile, cookie, )).start()
			except Exception as ex:
				logoFile = ''
				xbmc.log("{0}".format(ex), 3)
		else:
			logoFile = ''
		list.append((match[0], logoFile, match[2], match[3], match[4]))
	return list, last_page, step

def IndexPageP(url):
	url = url + '&page=/0'
	current_page = int(url.split('/')[-1])       
	for pageIndex in range(10):
		try:
			matches, last_page, step = cache.get(IndexPagePs_regex, 72, url, table='pages')
			for item in matches:
				name = item[2]
				addDir(name, '{0}{1}'.format(baseUrl, item[1]), 4, item[0],FANART, True, item[3],isPrem=True)# m5
		except Exception as ex:
			xbmc.log(str(ex), 3)
		if current_page >= last_page:
			return True
		current_page += step
		url = url[:url.rfind('/')+1]
		url += str(current_page)

	if current_page <= last_page:
		addDir('[COLOR cyan]תוצאות נוספות[/COLOR]', url, 2, '','')
	return True

def IndexPageP_regex(url):
	result, cookie = cloudflare.request(url)
	last_page, step = GetPagegSteps(result, int(url.split('/')[-1]))
	matches = re.compile('<div id="movie\d+" class="ic_container">\s+(.*?)<img src="(.*?)".*?<h3><a href="(.*?)">(.*?)<.*?<p class="ic_text">\s+(.*?)\s+<\/p>',re.S).findall(result)
	showImages = Addon.getSetting('showImages') == 'true'
	list=[]
	for match in matches:
		if match[0].strip() == '':
			continue
		if showImages:
			try:
				logoUrl = match[1]
				logoFile = os.path.join(logosDir, logoUrl[logoUrl.rfind('/')+1:])
				if not os.path.isfile(logoFile):
					threading.Thread(target=getImageLinkBackground, args=(logoUrl, logoFile, cookie, )).start()
			except Exception as ex:
				logoFile = ''
				xbmc.log("{0}".format(ex), 3)
		else:
			logoFile = ''
		list.append((logoFile, match[2], match[3], match[4]))
	return list, last_page, step

def IndexPagePs(url):
	url = url + '/page/0'
	current_page = int(url.split('/')[-1])       
	for pageIndex in range(10):
		try:
			matches, last_page, step = cache.get(IndexPagePs_regex, 72, url, table='pages')
			for item in matches:
				name = item[2]
				addDir(name, '{0}{1}'.format(baseUrl, item[1]), 4, item[0],FANART, True, item[3],isPrem=True)# m5
		except Exception as ex:
			xbmc.log(str(ex), 3)
		if current_page >= last_page:
			return True
		current_page += step
		url = url[:url.rfind('/')+1]
		url += str(current_page)

	if current_page <= last_page:
		addDir('[COLOR cyan]תוצאות נוספות[/COLOR]', url, 2, '','')
	return True

def IndexPagePs_regex(url):
	result, cookie = cloudflare.request(url)
	last_page, step = GetPagegSteps(result, int(url.split('/')[-1]))
	#patr ='(?s)<div id="movie\d+".*?div class="sub">.*?Movix.*?<img src="(.*?)".*?<h3><a href="(.*?)">(.*?)<.*?<p class="ic_text">\s+(.*?)\s+<\/p>'
	patr ='(?s)<div id="movie\d+".*?<img src="(.*?)".*?<h3><a href="(.*?)">(.*?)<.*?<p class="ic_text">\s+(.*?)\s+<\/p>'
	matches = re.compile(patr,re.S).findall(result)
 	showImages = Addon.getSetting('showImages') == 'true'
	list=[]
	for match in matches:
		if showImages:
			try:
				logoUrl = match[0]
				logoFile = os.path.join(logosDir, logoUrl[logoUrl.rfind('/')+1:])
				if not os.path.isfile(logoFile):
					threading.Thread(target=getImageLinkBackground, args=(logoUrl, logoFile, cookie, )).start()
			except Exception as ex:
				logoFile = ''
				xbmc.log("{0}".format(ex), 3)
		else:
			logoFile = ''
		list.append((logoFile, match[1], match[2], match[3]))
	return list, last_page, step

def getImageLinkBackground(logoUrl, logoFile, cookie):
	data = common.OPEN_URL(logoUrl, headers={'Cookie': cookie})
	with open(logoFile, 'wb') as f:
		f.write(data)

def GetPagegSteps(result, current_page):

	block = re.compile('pnation.*?</strong>(.*?)<\/div>',re.I+re.M+re.U+re.S).findall(result)
	pages = "" if len(block) == 0 else re.compile('<a href=".*?[\/&]page[=]?\/(.*?)">(.*?)</a>',re.I+re.M+re.U+re.S).findall(block[0])

	nextPagesCount = len(pages)
	step = 10000 if nextPagesCount == 0 else int(pages[0][0]) - current_page
	last_page = current_page if nextPagesCount == 0 else int(pages[-1][0])
	for i in range(nextPagesCount-1, -1, -1):
		if pages[i][1] == '':
			continue
		if int(pages[i][0]) > last_page:
			last_page = int(pages[i][0])
		break
	return last_page, step


def addDir(name, url, mode, iconimage,fanart, isFolder=True, description='', isPrem=False):
	#u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&iconimage="+urllib.quote_plus(iconimage)+"&description="+urllib.quote_plus(description)+"&isprem="+str(isPrem)
	xbmc.log("-"*40+str(url)+str(mode))
	u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&iconimage="+urllib.quote_plus(iconimage)+"&description="+"&isprem="+str(isPrem)
	liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
	liz.setInfo( type="Video", infoLabels={ "Title": name , "Plot": str(description)} )
	liz.setProperty("fanart_Image", fanart)
	if not isFolder:
		liz.setProperty("IsPlayable","true")
	xbmcplugin.addDirectoryItem(handle=handle,url=u,listitem=liz,isFolder=isFolder)

def GetSeasons(series_num, iconimage, description, color):
	seasons = cache.get(GetSeasons_regex, 168, series_num,table="pages")
	for season in seasons:
		if params.get("isprem") == "True":
			addDir('[COLOR blue]{0} - {1}[/COLOR]'.format(name, season[1], color), '{0}/watchmovies/get_episodes/{1}?seasonid={2}'.format(baseUrl, series_num, season[0]), 3, iconimage,FANART, True, description,isPrem=True)
		else :
			addDir('[COLOR blue]{0} - {1}[/COLOR]'.format(name, season[1], color), '{0}/watchmovies/get_episodes/{1}?seasonid={2}'.format(baseUrl, series_num, season[0]), 3, iconimage,FANART, True, description)

def GetSeasons_regex(series_num):
	result = cloudflare.source('{0}/watchmovies/get_seasons/{1}'.format(baseUrl, series_num))
	matches = re.compile('onclick="get_episodes\(\'(.*?)\'\);">(.*?)<',re.I+re.M+re.U+re.S).findall(result)
	return matches

def GetEpisodes(season_num, iconimage, description):
	episodes = cache.get(GetEpisodes_regex, 24, season_num, table="pages")
	url = season_num.replace('get_episodes', 'get_episode')
	for episode in episodes:
		if params.get("isprem") == "True":
			addDir('[COLOR blue]{0} - {1}[/COLOR]'.format(name, episode[2]), "{0}&episodeid={1}".format(url, episode[1]), 4, iconimage,FANART, True, description,isPrem=True)
		else :
			addDir('[COLOR blue]{0} - {1}[/COLOR]'.format(name, episode[2]), "{0}&episodeid={1}".format(url, episode[1]), 4, iconimage,FANART, True, description)

def GetEpisodes_regex(season_num):
	result = cloudflare.source(season_num)
	matches = re.compile('onclick="get_episode\(\'(.*?)\',\'(.*?)\'\);">(.*?)<',re.I+re.M+re.U+re.S).findall(result)
	return matches

def SortByQuality(links):
	qualitiesList = ["1080p", "720p", "BDRip", "BRRip", "DVDRip", "HDTV", "HDRip", "R5", "DVDSCR", "WEBRip", "PDTV", "TVRip", "TC", "HDTS", "TS", "CAM"]
	sortedLinks = []
	random.seed()
	random.shuffle(links)
	for quality in qualitiesList:
		qualityLinks = [link for link in links if link[1].lower() == quality.lower()]
		for qualityLink in qualityLinks:
			sortedLinks.append(qualityLink)
	for link in links:
		if link[1] not in qualitiesList:
			sortedLinks.append(link)
	return sortedLinks

def LinksPage(url, iconimage, description):
	color = ''
	xbmc.log("-"*50+str(params))
	username = Addon.getSetting('username')
	movieid = url.split('-')[-1]
	if params.get("isprem") == "True":
		data = login.login(movieid)
		logg.logGA(username,url.split('/')[-1])
		xbmc.log("-"*50+str(data))
	else:
		data = False		
		if username == '' : 
                        logg.logGA('Free user',url.split('/')[-1])
	descriptions, links, seasons = cache.get(Links_regex, 72, url, table="pages")

	if data:
		color = "blue"
		links = []
		for key in data.keys():
			links.append((data.get(key).get('Server name'), data.get(key).get('Quality'), data.get(key).get('Direct link')))
		if data.get(key).get('Episode') == '':
			seasons = False
		else:
			seasons = True
		xbmc.executebuiltin("Notification(Movix.me, Showing premium response.,5000)")
	else:
		xbmc.executebuiltin("Notification(Movix.me, Showing normal response.,5000)")

	try:
		if len(descriptions) == 1:
			description = descriptions[0]
	except:
		xbmc.log("descriptions issue : "+"+++"*10)

	if seasons is None:
		addDir('[COLOR red] לא נמצאו מקורות ניגון [/COLOR]','99',99,'','',False, description)
		if not data:
			return
	elif seasons:
		if data:
			color = "blue"
		series_num = url.split('-')[-1]
		GetSeasons(series_num, iconimage, description, color)
	else:
		try:
			if len(links) < 1:
				addDir('[COLOR red] לא נמצאו מקורות ניגון [/COLOR]','99',99,'','',False, description)
				xbmc.log("&&&"*30)
				return
			elif len(links) > 1:
				links = SortByQuality(links)
				playingUrlsList = []
				for link in links:
					xbmc.log(str(link))
					playingUrlsList.append(link[2])
				addDir('[COLOR red] בחר בניגון אוטומטי [/COLOR]','99',99,'','',False, description)
				addDir('[COLOR white] - ניגון אוטומטי[/COLOR][COLOR blue]{0}[/COLOR]'.format(name, color), json.dumps(playingUrlsList), 7, iconimage,FANART, False, description)
				addDir('[COLOR red]  או בחר מקור לניגון, אם לא עובד נסה אחר [/COLOR]','99',99,'','',False, description)
			for link in links:
				addDir("[COLOR white]{2} - איכות - {0} - [/COLOR][COLOR blue]{1}[/COLOR]".format(link[0], name, link[1], color),link[2],5,iconimage,FANART,False, description)
			return
		except Exception, e:
			xbmc.log(str(e)+"+++"*50)

	if seasons is None:
		try:
			if len(links) < 1:
				addDir('[COLOR red] לא נמצאו מקורות ניגון [/COLOR]','99',99,'',False, description)
				return
			elif len(links) > 1:
				links = SortByQuality(links)
				playingUrlsList = []
				for link in links:
					xbmc.log(str(link))
					playingUrlsList.append(link[2])
				addDir('[COLOR red] בחר בניגון אוטומטי [/COLOR]','99',99,'','',False, description)
				addDir('[COLOR {1}]{0} - ניגון אוטומטי[/COLOR]'.format(name), json.dumps(playingUrlsList), 7, iconimage,FANART, False, description)
				addDir('[COLOR red]  או בחר מקור לניגון, אם לא עובד נסה אחר [/COLOR]','99',99,'','',False, description)
			for link in links:
				addDir("[COLOR {3}]{0} - {1} - איכות {2}[/COLOR]".format(name, link[0], link[1], color),link[2],5,iconimage,FANART,False, description)
		except Exception, e:
			xbmc.log(str(e)+"+++"*50)

def Links_regex(url):
	result=cloudflare.source(url)
	if result is None:
		xbmc.log('Cannot load Links Page. ({0})'.format(url), 2)
		return None
	matches = re.compile('<div style="width:540px;padding-top:5px;">(.+?)</div>',re.I+re.M+re.U+re.S).findall(result)
	links=None
	if 'תוכן זה זמין כעת למנויי Movix בלבד!' in result:
		seasons = None
	elif 'get_seasons' in result:
		seasons = True
	else:
		links = resolver.GetLinks(result)
		seasons = False
	return [matches,links,seasons]

def PlayWs(url, autoPlay=False):
	url = resolver.CheckAdFlyLink(url)
	if url and baseUrl in url:
                #xbmc.log(str(url)+"+"*40)
		url = resolver.ResolveUrl(url)
	elif "vidlockers" in url:
		item = urlresolver.HostedMediaFile(url)
		url = urlresolver.resolve(item.get_url())
	if url:
		link = url.split(';;')
		xbmc.log(str(url)+"="*40)
		#xbmc.executebuiltin("PlayMedia(https://ph2dw5.oloadcdn.net/dl/l/BIdFVvXpzQRZ5UVW/lZ33PBNNqoY/Angry.Birds.2016.1080p.BluRay.x264-GECKOS-HebDub.mkv.mp4)")
		listitem = xbmcgui.ListItem(path=link[0])
		xbmcplugin.setResolvedUrl(handle, True, listitem)
		if len(link) > 1:
			while not xbmc.Player().isPlaying():
				xbmc.sleep(10) #wait until video is being played
			xbmc.Player().setSubtitles(link[1])
		return True
	else:
		if not autoPlay:
			dialog = xbmcgui.Dialog()
			ok = dialog.ok('OOOPS', 'נסה לבחור מקור ניגון אחר.')
		return False

def AutoPlayUrl(urls):
	playingUrlsList = json.loads(urls)
	for playingUrl in playingUrlsList:
		if PlayWs(playingUrl, autoPlay=True):
			return
	dialog = xbmcgui.Dialog()
	ok = dialog.ok('OOOPS', 'לא נמצאו מקורות זמינים לניגון')

def PlayTrailer(url):
	matches = cache.get(Trailer_regex, 24, url, table="pages")
	if len(matches) > 0:
		url = matches[0]
		PlayWs(url)

def Trailer_regex(url):
	result = cloudflare.source(url)
	matches = re.compile('"videoUrl":"(.+?)"',re.I+re.M+re.U+re.S).findall(result)
	return matches

def Categories():
	addDir("[COLOR orange][B]Premium Movies - סרטים פרימיום[/B][/COLOR]","{0}/movies".format(baseUrl),202,'http://noobsandnerds.com/addons/cache/Addons/plugin.video.moviereleases/icon.png',FANART)
	addDir("[COLOR orange][B]Premium Series - סדרות פרימיום[/B][/COLOR]","{0}/series".format(baseUrl),202,'https://farm6.staticflickr.com/5602/15700070751_88d83d38fd_o_d.png',FANART)
	addDir("Free Movies - סרטים חינמי","{0}/movies".format(baseUrl),2,'https://pbs.twimg.com/profile_images/632550903829143553/l1mcM8bL.png',FANART)
	addDir("Free Series - סדרות חינמי","{0}/series".format(baseUrl),2,'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTxnuZgOpXn5ZL9SXcE5VsEeXBXwm83Pa22wGwN2EWAOl12-zcAgA',FANART)
	addDir("Clear data - ניקוי נתונים","fullClean",22,'http://static1.squarespace.com/static/5411d5c0e4b02e1c8b27565a/t/55c0fd10e4b074070c899cd3/1438711058259/quartz+cuvette+cleaning?format=500w',FANART)
	addDir("Search - חיפוש"," ",6,'https://encrypted-tbn1.gstatic.com/images?q=tbn:ANd9GcQlAUVuxDFwhHYzmwfhcUEBgQXkkWi5XnM4ZyKxGecol952w-Rp',FANART)
	addDir("Dubbed - מדובבים","{0}/search_movies?q=%D7%9E%D7%93%D7%95%D7%91%D7%91&sb=&year=".format(baseUrl),2,'http://www.afaqs.com/all/news/images/news_story_grfx/2015/45297_1_home_big.jpg',FANART)
	addDir("Kids - ילדים","{0}/genres/Kids".format(baseUrl),2,'http://www.in-hebrew.co.il/images/logo-s.jpg',FANART)
	addDir("Animation - אנימציה","{0}/genres/Animation".format(baseUrl),2,'http://icons.iconarchive.com/icons/designbolts/free-movie-folder/256/Animated-icon.png',FANART)
	addDir("Fantasy - פנטזיה","{0}/genres/Fantasy".format(baseUrl),2,'http://blog.tapuz.co.il/girlkido/images/3472680_852.jpg',FANART)
	addDir("Family - משפחה","{0}/genres/Family".format(baseUrl),2,'http://pschools.haifanet.org.il/dror/DocLib1/%D7%99%D7%95%D7%9D%20%D7%9E%D7%A9%D7%A4%D7%97%D7%94%20%D7%A9%D7%9E%D7%97.jpg',FANART)
	addDir("Israeli - ישראלי","{0}/genres/israeli".format(baseUrl),2,'http://upload.wikimedia.org/wikipedia/commons/thumb/d/d4/Flag_of_Israel.svg/250px-Flag_of_Israel.svg.png',FANART)
	addDir("Live Shows - הופעות חיות","{0}/genres/LiveShow".format(baseUrl),2,'https://encrypted-tbn3.gstatic.com/images?q=tbn:ANd9GcR1kNugU_x7YQtz7Crjr1UmwOJRyxFC25zDwIkXc5jNQszermsw',FANART)
	addDir("Comedy - קומדיה","{0}/genres/Comedy".format(baseUrl),2,'http://www.filmsite.org/images/comedy-genre.jpg',FANART)
	addDir("Drama - דרמה","{0}/genres/Drama".format(baseUrl),2,'http://comps.canstockphoto.com/can-stock-photo_csp11392197.jpg',FANART)
	addDir("Documentary - דוקומנטרי","{0}/genres/Documentary".format(baseUrl),2,'http://icons.iconarchive.com/icons/aaron-sinuhe/tv-movie-folder/512/Documentaries-National-Geographic-icon.png',FANART)
	addDir("Action - פעולה","{0}/genres/Action".format(baseUrl),2,'http://pmtips.net/wp-content/uploads/2012/02/action.jpg',FANART)
	addDir("Crime - פשע","{0}/genres/Crime".format(baseUrl),2,'http://drthurstone.com/wp-content/uploads/2014/07/Crime-Pix.jpg',FANART)
	addDir("Thriller - מתח","{0}/genres/Thriller".format(baseUrl),2,'http://becplmovies.files.wordpress.com/2011/06/thrillers_title12.jpg',FANART)
	addDir("War - מלחמה","{0}/genres/War".format(baseUrl),2,'http://cdn2.pitchfork.com/news/53502/0ff1bba7.jpg',FANART)
	addDir("Mystery - מיסתורין","{0}/genres/Mystery".format(baseUrl),2,'http://www.barronmind.com/WMHlogoweb.gif',FANART)
	addDir("Horror - אימה","{0}/genres/Horror".format(baseUrl),2,'https://cdn4.iconfinder.com/data/icons/desktop-halloween/256/Mask.png',FANART)
	addDir("Sci-Fi - מ.בדיוני","{0}/genres/Sci-Fi".format(baseUrl),2,'http://images.clipartpanda.com/sci-fi-clipart-peacealienbw.png',FANART)
	xbmc.executebuiltin('Container.SetViewMode(500)')

def MostInCategory(category):
	matches = cache.get(MostInCategory_regex, 0, baseUrl,category , table="pages") if 'recent' in category else cache.get(MostInCategory_regex, 24, baseUrl, category ,table="pages")
	for match in matches:
		addDir(match[2], match[1], 4, match[0],FANART, True, ' ', isPrem=True)

def MostInCategory_regex(url ,category):
	html , cookie = cloudflare.request(url)
	
	if category != '':
		delim = category.split('|')
		startBlock = html.find(delim[0])
		endBlock = html.find(delim[1], startBlock)
		if delim[0] == 'הסרטים הנצפים ביותר':
			rej = '<div style="float.*?src="(.*?)".*?<a href="(.*?)"><span.*?>(.*?)</span>'
		else:
			rej = '<div class="small-item".*?src="(.*?)".*?<a href="(.*?)">(.*?)</a>'
		block = html[startBlock:endBlock]
		matches = re.compile(rej, re.I+re.M+re.U+re.S).findall(block)
		items = []
		showImages = Addon.getSetting('showImages') == 'true'
                for match in matches:
                        if showImages:
                                try:
                                        logoUrl = match[0]
                                        if not logoUrl.startswith('/') :
                                                logoUrl = '/' + logoUrl
                                        if  baseUrl not in logoUrl :
                                                logoUrl = "{0}{1}".format(baseUrl, logoUrl)
                                        logoFile = os.path.join(logosDir, logoUrl[logoUrl.rfind('/')+1:])
                                        if not os.path.isfile(logoFile):
                                                threading.Thread(target=getImageLinkBackground, args=(logoUrl, logoFile, cookie, )).start()
                                except Exception as ex:
                                        logoFile = ''
                                        xbmc.log("{0}".format(ex), 3)
                        else:
                                logoFile = ''
		
			items.append((logoFile,'{0}{1}'.format(baseUrl, match[1]), match[2]))
		
	return items

def ClearCache():
	cache.clear(['cookies', 'pages'])

def DeleteImages():
	for the_file in os.listdir(logosDir):
		file_path = os.path.join(logosDir, the_file)
		try:
			if os.path.isfile(file_path):
				os.unlink(file_path)
		except Exception as ex:
			xbmc.log("{0}".format(ex), 3)

def get_params():
	param=[]
	paramstring=sys.argv[2]
	if len(paramstring)>=2:
		params=sys.argv[2]
		cleanedparams=params.replace('?','')
		if (params[len(params)-1]=='/'):
			params=params[0:len(params)-2]
		pairsofparams=cleanedparams.split('&')
		param={}
		for i in range(len(pairsofparams)):
			splitparams={}
			splitparams=pairsofparams[i].split('=')
			if (len(splitparams))==2:
				param[splitparams[0]]=splitparams[1]

	return param


params=get_params()

try:
	url=urllib.unquote_plus(params["url"])
except:
	url=None
try:
	name=urllib.unquote_plus(params["name"])
except:
	name=None
try:
	mode=int(params["mode"])
except:
	mode=None
try:
	iconimage=urllib.unquote_plus(params["iconimage"])
except:
	iconimage=""
try:
	description=urllib.unquote_plus(params["description"])
except:
	description=""

updateView = True

if mode==None or url==None or len(url)<1:
	Categories()
elif mode==2:
	IndexPage(url)
elif mode==202:
	IndexPagePremium(url)
elif mode==3:
	GetEpisodes(url, iconimage, description)
elif mode==4:
	LinksPage(url, iconimage, description)
elif mode==5:
	PlayWs(url)
elif mode==6:
	updateView = searchWs()
elif mode==7:
	AutoPlayUrl(url)
elif mode==8:
	PlayTrailer(url)
elif mode==9:
	MostInCategory(url)
elif mode==11:
	updateView = yearWs()
elif mode==10:
	IndexPageP(url)
elif mode==12:
	IndexPagePs(url)

elif mode==13:
	updateView = searchWsP(url)
elif mode==20:
	xbmc.executebuiltin("XBMC.Notification({0}, ניקוי מטמון.., {1}, {2})".format(AddonName, 5000 ,icon))
	ClearCache()
	xbmc.executebuiltin("XBMC.Notification({0}, ניקוי מטמון הסתיים., {1}, {2})".format(AddonName, 5000 ,icon))
	updateView = False
elif mode==21:
	xbmc.executebuiltin("XBMC.Notification({0}, ניקוי תמונות..., {1}, {2})".format(AddonName, 300000 ,icon))
	DeleteImages()
	xbmc.executebuiltin("XBMC.Notification({0}, ניקוי תמונות הסתיים., {1}, {2})".format(AddonName, 5000 ,icon))
	updateView = False
elif mode==22:
	xbmc.executebuiltin("XBMC.Notification({0}, ניקוי נתונים..., {1}, {2})".format(AddonName, 300000 ,icon))
	ClearCache()
	DeleteImages()
	xbmc.executebuiltin("XBMC.Notification({0}, ניקוי נתונים הסתיים., {1}, {2})".format(AddonName, 5000 ,icon))
	updateView = False

if updateView:
	xbmcplugin.setContent(handle, 'episodes')
	if mode==None or url==None or len(url)<1:
		xbmc.executebuiltin("Container.SetViewMode(500)")
	else:
		xbmc.executebuiltin('Container.SetViewMode(515)')
	xbmcplugin.endOfDirectory(handle)
