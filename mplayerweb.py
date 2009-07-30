# Now Perform the main imports
from twisted.application import internet, service 
from twisted.web import server, resource
from twisted.web.static import File
import subprocess

MEDIA_PATH = '/mnt/media1/TV'

class MediaResource(File):
    """
    Subclass the twisted web static File resource, modifying it's behavior so
    that when the URI points to a file it opens it as a subprocess in mplayer
    instead of actually returning the file.
    """
    def render(self, request):
        self.restat()
        if not self.exists():
            return self.childNotFound.render(request)
        if self.isdir():
            return self.redirect(request)
        p = subprocess.Popen(['mplayer', '-fs', self.path])
        return self.path

web = MediaResource(MEDIA_PATH) 
site = server.Site(web)
application = service.Application('mplayerweb') 
siteServer = internet.TCPServer(9001, site)
siteServer.setServiceParent(application)
