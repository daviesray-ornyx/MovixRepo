# -*- coding: utf-8 -*-
import re, json
import common, urlresolver, jsunpack, base64, cloudflare  
import xbmcaddon, xbmc
import YDStreamExtractor

def ResolveUrl(url):
	link = False
	try:
		result=cloudflare.source(url)
		matches=re.compile('<div id="embed_code".+?<iframe.+?src=["|\'](.*?)["|\'].+?<\/iframe><\/div>',re.I+re.M+re.U+re.S).findall(result)
		url = matches[0]
		if url.find('//') == 0:
			url = 'http:{0}'.format(url)
		if "divxpress" in url:
			html = common.OPEN_URL(url)
			matches = re.compile('input type="hidden" name="(.*?)" value="(.*?)"', re.I+re.M+re.U+re.S).findall(html)
			user_data = {}
			for match in matches:
				user_data[match[0]] = match[1]
			html = common.OPEN_URL(url, user_data=user_data)
			matches = re.compile("<div id=\"player_code\"><script type='text/javascript'>(.*?)</script></div>", re.I+re.M+re.U+re.S).findall(html)
			unpack = jsunpack.unpack(matches[0])
			matches = re.compile('"src"value="(.*?)"', re.I+re.M+re.U+re.S).findall(unpack)
			link = "{0}|User-Agent={1}&Referer={2}".format(matches[0], 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3', url)
		elif "vidzi" in url:
			html = common.OPEN_URL(url)
			matches = re.compile("<script type='text/javascript'>(.*?)</script>", re.I+re.M+re.U+re.S).findall(html)
			unpack = jsunpack.unpack(matches[0])
			matches = re.compile('file\s*:\s*"([^"]+)', re.I+re.M+re.U+re.S).findall(unpack)
			link = "{0}|Referer=http://vidzi.me/nplayer/jwplayer.flash.swf".format(matches[0])
		elif "uptostream" in url:
			html = common.OPEN_URL(url)
			matches = re.compile("source src='(.+?)'").findall(html)
			link = "{0}".format(matches[-1])
			matches = re.compile("subtitles' src='(.+?)'").findall(html)
			subtitles = matches[0] if len(matches) > 0 else ''
			link = "{0};;{1}".format('http:'+link, 'http:'+subtitles)
		elif "openload" in url:
                        xbmc.log(str(url)+">>>>>>>"*40)
			vid = YDStreamExtractor.getVideoInfo(url, quality=0)
                        link = vid.streamURL()
                        xbmc.log(str(url)+">openload>"*5)
                elif "streamin" in url:
                        xbmc.log(str(url)+">>>>>>>"*40)
			vid = YDStreamExtractor.getVideoInfo(url, quality=0)
                        link = vid.streamURL()
                        xbmc.log(str(url)+">streamin>"*5)
		else:
			if "movreel" in url:
				url = url.replace("/embed-","/")
			#elif "openload" in url:
				#url = url.replace(".co",".io")                              
				#xbmc.log(str(url)+">>>>>>>"*40)
			item = urlresolver.HostedMediaFile(url)
			xbmc.log(str(item)+"?????????"*40)
			link = urlresolver.resolve(item.get_url())
			xbmc.log(str(link)+"<<<<"*40)
	except Exception, e: 
		print e
	return link 
	
def GetYifyLinks(url):
	sources = []
	try:
		result=common.OPEN_URL(url)
		matches=re.compile('<div id="embed_code".+?<iframe.+?src=["|\'](.*?)["|\'].+?<\/iframe><\/div>',re.I+re.M+re.U+re.S).findall(result)
		url = matches[0]
		html = common.OPEN_URL(url)
		links = re.compile('pic=([^&]+)').findall(html)
		for i in links:
			try:
				user_data = {'url': i, 'fv': '16'}
				html = common.OPEN_URL("http://yify.tv/player/pk/pk/plugins/player_p2.php", user_data=user_data)
				result = json.loads(html)
				try: sources.append({'quality': '1080p', 'url': [i['url'] for i in result if i['width'] == 1920 and 'google' in i['url']][0]})
				except: pass
				try: sources.append({'quality': '720p', 'url': [i['url'] for i in result if i['width'] == 1280 and 'google' in i['url']][0]})
				except: pass

				try: sources.append({'quality': '1080p', 'url': [i['url'] for i in result if i['width'] == 1920 and not 'google' in i['url'] and not 'mediafire' in i['url']][0]})
				except: pass
				try: sources.append({'quality': '720p', 'url': [i['url'] for i in result if i['width'] == 1280 and not 'google' in i['url'] and not 'mediafire' in i['url']][0]})
				except: pass
			except:
				pass
	except Exception, e: 
		print e
	return sources

def GetLinks(text):
	links = []
	try:
		ignoreServers = ["goodvideohost"]
		downloadsServers = ["vidlockers"]
		linksBlock = re.compile('<ul class="movie_links"(.*?)</ul>\s*</div>',re.I+re.M+re.U+re.S).findall(text)
		reg = 'src="\/img\/servers\/(.*?).png.*?<div class="span3".*?<b>.*? (.*?)<\/b>.*?rate-external-result-(.*?)".*?[<\/li>|<\/div>]'
		watchLinks = re.compile(reg,re.I+re.M+re.U+re.S).findall(linksBlock[0])
		watches = []
		for watch in watchLinks:
			if watch[0] in ignoreServers:
				continue
			if "yify" in watch[0]:
				yifyLinks = GetYifyLinks(watch[2])
				for link in yifyLinks:
					watches.append((watch[0], link["quality"], link["url"]))
				continue
			watches.append((watch[0], watch[1], 'http://www.movix.me/watchmovies/go/{0}'.format(watch[2])))
		if len(linksBlock) == 2:
			download = re.compile(reg,re.I+re.M+re.U+re.S).findall(linksBlock[1])
			downloads = [[d[0], d[1], 'http://www.movix.me/watchmovies/go/{0}'.format(d[2])] for d in download if d[0] in downloadsServers]
		else:
			downloads = []
		links = watches + downloads
	except Exception as e:
		pass
	return links
	
def CheckAdFlyLink(url):
	if "adf.ly" not in url:
		return url
	retUrl = None
	try:
		html = common.OPEN_URL(url)
		ysmm = re.findall(r"var ysmm =.*\;?", html)
		if len(ysmm) > 0:
			ysmm = re.sub(r'var ysmm \= \'|\'\;', '', ysmm[0])
			left = ''
			right = ''
			for c in [ysmm[i:i+2] for i in range(0, len(ysmm), 2)]:
				left += c[0]
				right = c[1] + right
			retUrl = base64.b64decode(left.encode() + right.encode())[2:].decode()
			if re.search(r'go\.php\?u\=', retUrl):
				retUrl = base64.b64decode(re.sub(r'(.*?)u=', '', retUrl)).decode()
	except Exception as e:
		print str(e)
	return retUrl
