from PMS import *
from PMS.Objects import *
from PMS.Shortcuts import *

import putio


PLUGIN_TITLE = "Put.io"				# The plugin Title
PLUGIN_PREFIX = "/video/putio"		# The plugin's contextual path within Plex

ICON_DEFAULT = "icon-default.png"	#
ART_DEFAULT = "art-default.jpg"		#


api = None


def Start():	
	# Register our plugins request handler
	Plugin.AddPrefixHandler(PLUGIN_PREFIX, MainMenu, PLUGIN_TITLE, ICON_DEFAULT, ART_DEFAULT)
	
	# Add in the views our plugin will support
	Plugin.AddViewGroup("InfoList", viewMode="InfoList", mediaType="items")
	Plugin.AddViewGroup("List", viewMode="List", mediaType="items")
	Plugin.AddViewGroup("Photos", viewMode="List", mediaType="photos")
	
	# Set up our plugin's container
	MediaContainer.art = R(ART_DEFAULT)
	MediaContainer.title1 = PLUGIN_TITLE
	DirectoryItem.thumb = R(ICON_DEFAULT)


def CreatePrefs():
	Prefs.Add(id='api_key', type='text', default='', label='API Key')
	Prefs.Add(id='api_secret', type='text', default='', label='API Secret', option='hidden')


def MainMenu():
	global api
	
	dir = MediaContainer(noCache=True)
	
	if Prefs.Get('api_key') and Prefs.Get('api_secret'):
		api_key = Prefs.Get('api_key')
		api_secret = Prefs.Get('api_secret')
		
		api = putio.Api(api_key=api_key,api_secret=api_secret)
		
		listItems(id=None, dir=dir)
		
		dir.Append(Function(DirectoryItem(DoLogout, title='logout')))
	
	else:
		dir.Append(PrefsItem(title='login'))
	
	
	return dir
	
def listItems(id, dir):
	if id != None:
		items = api.get_items(parent_id=id, offset=0)
	else:
		items = api.get_items(offset=0)
		
	for it in items:
		if it.type == 'folder':
			dir.Append(Function(DirectoryItem(Folders, title=it.name), id=it.id))
		
		elif it.type == 'movie':
			dir.Append(Function(VideoItem(Files, title=it.name, thumb=it.screenshot_url), url=it.get_stream_url()))
		
		elif it.type == 'audio':
			dir.Append(Function(TrackItem(Files, title=it.name), url=it.get_stream_url()))
		
		# elif it.type == 'image':
		# 	dir.Append(Function(PhotoItem(Files, title=it.name, subtitle='', summary=it.name, thumb=it.thumb_url), url=it.get_stream_url()))
			
		else:
			Log(it.type)


def Folders(sender, id):
	dir = MediaContainer(title2=sender.itemTitle)
	
	item = api.get_items(id=id)[0]
	if item.is_dir:
		listItems(id=id, dir=dir)
	
	return dir

def Files(sender, url):
	return Redirect(url)


def DoLogout(sender):
	Prefs.Set('api_key', '')
	Prefs.Set('api_secret', '')
	
	return Redirect(PLUGIN_PREFIX)
