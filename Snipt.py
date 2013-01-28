import sublime, sublime_plugin, urllib, urllib2, json
from pprint import pprint

class SniptCommand(sublime_plugin.TextCommand):

	snipt_api_key = "9a6866789d012764cf45557e0b58d07fee5f26b6"
	snipt_username = "gregwhitworth"
	snipt_url = ''

	# Run
	# ---------------------------------------
	# Runs the script
	# ---------------------------------------

	def run(self, edit):
		self.snipt_url = self.buildSniptURL()
		snipts = self.getSnipts()
		self.createSnipts(snipts)

	# Get Snipts
	# ---------------------------------------
	# Will create a list of your snipts
	# ---------------------------------------

	def getSnipts(self):
		try:
			data = urllib2.urlopen(self.snipt_url).read()
			data = json.loads(data)
			return data['objects']
		except urllib2.HTTPError, e:
			print "HTTP error: %d" % e.code
		except urllib2.URLError, e:
			print "Network error: %s" % e.reason.args[1]

	def createSnipts(self, snipts):
		pprint(snipts)
		#for snipt in snipts:
		#	layout = '<snippet>'
    	#	layout += '<content><![CDATA[' + snipt['code'] + ']]></content>'
    	#	layout += '<description>' + snipt['slug'] + '</description>'
    	#	layout += '</snippet>'
    	#	f = open(sublime.packages_path() + '\Snipt\\' + snipt['slug'] + '.sublime-snippet', 'w')
    	#	f.write(layout)
    	#	f.close

	# Build Snipt URL
	# ---------------------------------------
	# Builds the necessary snipt url
	# @return str
	# ---------------------------------------

	def buildSniptURL(self):
		snipt_api_base = "https://snipt.net/api/private/snipt/?"
		return snipt_api_base + "username=" + self.snipt_username + "&api_key=" + self.snipt_api_key + "&format=json"