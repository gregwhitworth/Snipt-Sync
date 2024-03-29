# =======================================================
# Snipt Sync for Sublime
# =======================================================
# @author    Greg Whitworth
# @link      https://github.com/gregwhitworth/Snipt
# @version   1.0
# =======================================================

import sublime, sublime_plugin, urllib, urllib2, json, re, time, threading

settings = sublime.load_settings("SniptSync.sublime-settings")
snipt_api_key = settings.get('snipt_api_key')
snipt_username = settings.get('snipt_username')
symbol_start = {"ActionScript":"/*",
				"AppleScript":"(*",
				"ASP":"<%--",
				"Batch File":"REM",
				"HTML":"<!--",
				"PHP":"/**",
				"Text":""}
symbol_end = {"ActionScript":"*/",
			  "AppleScript":"*)",
			  "ASP":"--%>",
			  "Batch File":"",
			  "HTML":"<!--",
			  "PHP":"**/",
			  "Text":""}

# Get Snipts
# ---------------------------------------
# Will return the json information from
# the provided URL
# @param url
# @return object
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
	snipt_api_base = "https://snipt.net/api/private"
	#Get general private API
	if id == None:
		return snipt_api_base + "/snipt/?username=" + snipt_username + "&api_key=" + snipt_api_key + "&format=json"
	#Return individual API URL
	else:
		return snipt_api_base + "/snipt/"  + id + "/?username=" + snipt_username + "&api_key=" + snipt_api_key + "&format=json"

def getSyntax( syntax ):
	return re.search('%s(.*)%s' % ('/', '/'), syntax).group(1)

# Sync Snipts
# ---------------------------------------
# Builds the context menu by pulling in
# your scripts from Snipt.net
# @return void
# ---------------------------------------

class SyncSniptsCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		syncsnippetsThread = SyncSniptsThread(self, edit)
		syncsnippetsThread.start()
	

# Sync Snipts Thread
# ---------------------------------------
# This does most of the heavy lifting but
# places it in a thread so that it doesn't
# crash Sublime.
# @return void
# ---------------------------------------
class SyncSniptsThread(threading.Thread):
	def __init__(self, cmd, edit):
		threading.Thread.__init__(self)
		self.cmd = cmd
		self.edit = edit

	def buildLexerDict(self,snipts):
		lexers = snipts[0]['user']['lexers']
		lexer_dict = {}
		for lexer in lexers:
			lexer_dict[lexer] = []
		return lexer_dict

	def buildSniptsContextDict(self,snipts,lexer_dict):
		snipts_dict = lexer_dict
		for snipt in snipts:
			snipts_dict[snipt['lexer']].append({"id":str(snipt['id']),
										   "title":snipt['title']})
		return snipts_dict

	def run(self):
		snipt_url = buildSniptURL()
		snipts_count = 1;
		snipts = getSnipts(snipt_url)
		context_menu = '['
		context_menu += '\n\t{ "caption": "Snipts", "id": "file", "children":'
		context_menu += '\n\t\t['
		if snipts == None:
			{"caption":"No snipts available"}
		else:
			snipts = snipts['objects']
			lexers = self.buildLexerDict(snipts)
			snipts_dict = self.buildSniptsContextDict(snipts, lexers)
			for j,key in reversed(list(enumerate(reversed(snipts_dict.keys())))):
				context_menu += '\n\t\t\t{ "caption":"' + key + '", "id": "file", "children":'
				context_menu += '\n\t\t\t\t['
				for s, snipt in reversed(list(enumerate(reversed(snipts_dict[key])))):
					snipts_count += 1
					get_snipt_temp = '\n\t\t\t\t\t{"command": "get_snipt", "args": {"id":"' + str(snipt['id']) + '"}, "caption": "' + snipt['title'] + '"}'
					if s == 0:
						context_menu += get_snipt_temp
					else:
						context_menu += get_snipt_temp + ','							
				context_menu += '\n\t\t\t\t]' # End Lexer
				context_menu += '\n\t\t\t}' # End Lexer
				if j == 0:
					context_menu += ''
				else:
					context_menu += ','	
		context_menu += '\n\t\t]'
		context_menu += '\n\t}'
		context_menu += '\n]'
		f = open(sublime.packages_path() + '\SniptSync\\Context.sublime-menu', 'w')
		f.write(context_menu)
		f.close
		return

	def callback(self, snippets_count):
		self.cmd.view.set_status('snippet', 'snippet Sync: Added ' + str(snippets_count)  + ' snippets from your account.')
		sublime.set_timeout(lambda: self.cmd.view.erase_status('snippet'), 3000)

# Get Snipt
# ---------------------------------------
# Goes to Snipt.net and grabs the snippet
# and inserts it where the cursor is.
# @param id
# @return void
# ---------------------------------------

class GetSniptCommand(sublime_plugin.TextCommand):
	def run(self, edit, id):
		snipt_url = buildSniptURL(str(id))
		sel = self.view.sel()
		syntax_abbreviation = getSyntax( self. view.settings().get('syntax') )
		snipts = getSnipts(snipt_url);
		title = snipts['title']
		author = snipts['user']['username']
		snipt_id = snipts['id']
		comment = symbol_start[syntax_abbreviation] + " ----------------------------------------" + '\n'
		comment += "@title " + title + '\n'
		comment += "@author " + author + '\n'
		comment += "@snipt_id " + str(snipt_id) + '\n'
		comment += "--------------------------------------- " + symbol_end[syntax_abbreviation] + '\n'
		code = snipts['code']
		layout = comment + code
		self.view.insert(edit, sel[0].begin(), layout)
		return