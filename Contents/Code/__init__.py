import putio2


PLUGIN_TITLE = "Put.io"                 # The plugin Title
PLUGIN_PREFIX = "/video/putio"          # The plugin's contextual path within Plex

ICON_DEFAULT = "icon-default.png"
ART_DEFAULT = "art-default.jpg"

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
    
    Dict['api'] = None

def MainMenu():
    dir = MediaContainer(noCache=True)
    
    #if Prefs['api_key'] and Prefs['api_secret']:
	#	api_key = Prefs['api_key']
	#	api_secret = Prefs['api_secret']
	#	
	#	Dict['api'] = putio.Api(api_key=api_key,api_secret=api_secret)
	#	
	#	listItems(id=None, dir=dir)
	#	
	#	# dir.Append(Function(DirectoryItem(DoLogout, title='logout')))
	#
	#else:
	#	dir.Append(PrefsItem(title='login'))

    Dict['api'] = putio2.Client('C52LZDSK')
    
    listItems(id=None, dir=dir)
    
    return dir

def listItems(id, dir):
    if id != None:
        items = Dict['api'].File.list(parent_id=id)
    else:
        items = Dict['api'].File.list()
    
    for it in items:
        if it.content_type == 'application/x-directory':
            dir.Append(Function(DirectoryItem(Folders, title=it.name), id=it.id))
        
        elif it.content_type == 'video/x-matroska':
            dir.Append(Function(VideoItem(Files, title=it.name, thumb=it.screenshot), id=it.id))
        #
        #elif it.type == 'audio':
        #	dir.Append(Function(TrackItem(Files, title=it.name), url=it.get_stream_url()))
        #
        # elif it.type == 'image':
        # 	dir.Append(Function(PhotoItem(Files, title=it.name, subtitle='', summary=it.name, thumb=it.thumb_url), url=it.get_stream_url()))
        #
        else:
            Log(it.content_type)

def Folders(sender, id):
    dir = MediaContainer(title2=sender.itemTitle)
    
    listItems(id=id, dir=dir)
    
    return dir

def Files(sender, id):
	return Redirect(url)

def DoLogout(sender):
	return Redirect(PLUGIN_PREFIX)
