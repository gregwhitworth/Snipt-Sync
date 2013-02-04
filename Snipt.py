import sublime, sublime_plugin, urllib, urllib2, json, io, threading
from pprint import pprint

snipt_api_key = "9a6866789d012764cf45557e0b58d07fee5f26b6"
snipt_username = "gregwhitworth"

# Get Snipts
# ---------------------------------------
# Will create a list of your snipts
# ---------------------------------------

def getSnipts(url):
	try:
		data = urllib2.urlopen(url).read()
		data = json.loads(data)
		return data
	except urllib2.HTTPError, e:
		print "HTTP error: %d" % e.code
	except urllib2.URLError, e:
		print "Network error: %s" % e.reason


# Build Snipt URL
# ---------------------------------------
# Builds the necessary snipt url
# @return str
# ---------------------------------------

def buildSniptURL(id = None):
	snipt_api_base = "https://snipt.net/api/private/snipt/"
	#Get general private API
	if id == None:
		return snipt_api_base + "?username=" + snipt_username + "&api_key=" + snipt_api_key + "&format=json"			
	#Return individual API URL
	else:
		return snipt_api_base  + id + "/?username=" + snipt_username + "&api_key=" + snipt_api_key + "&format=json"

class SyncSniptsCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		snipt_url = buildSniptURL()
		snipts = getSnipts(snipt_url)
		snipts = snipts['objects']
		context_menu = '['
		context_menu += '\n\t{ "caption": "Snipts", "id": "file", "children":'
		context_menu += '\n\t\t['
		for j,snipt in reversed(list(enumerate(reversed(snipts)))):
			get_snipt_temp = '\n\t\t{"command": "get_snipt", "args": {"id":"' + str(snipt['id']) + '"}, "caption": "' + snipt['title'] + '"}'
			if j == 0:
				context_menu += get_snipt_temp
			else:
				context_menu += get_snipt_temp + ','
		context_menu += '\n\t\t]'
		context_menu += '\n\t}'
		context_menu += '\n]'
		f = open(sublime.packages_path() + '\Snipt\\Context.sublime-menu', 'w')
		f.write(context_menu)
		f.close


class GetSniptCommand(sublime_plugin.TextCommand):
	def run(self, edit, id):
		sel = self.view.sel()
		snipt_url = buildSniptURL(str(id))
		snipts = getSnipts(snipt_url);
		code = snipts['code']
		for entry in sel:
			entry.append(code)
		return
