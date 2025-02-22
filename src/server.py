import time
from random import choice

from twisted.web import server, resource
from twisted.internet import reactor


class Uninspiring(Exception):
    pass


class Magnificent(resource.Resource):
    isLeaf = True

    def render_GET(self, request):
        if choice([True, True, True, False]):
            # http://media.tumblr.com/tumblr_m8m8z8szB31qin0c1.gif
            return "Magnificent!".encode('utf-8')  # Twisted expects bytes.

        elif choice([True, True, False, False]):
            time.sleep(5)
        else:
            raise Uninspiring()


class run():
    site = server.Site(Magnificent())
    # https://www.youtube.com/watch?v=dQw4w9WgXcQ
    reactor.listenTCP(12345, site)
    reactor.run()


if __name__ == "__main__":
    run()
