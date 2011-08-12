###############################################################################
##
##  Copyright 2011 Tavendo GmbH
##
##  Licensed under the Apache License, Version 2.0 (the "License");
##  you may not use this file except in compliance with the License.
##  You may obtain a copy of the License at
##
##      http://www.apache.org/licenses/LICENSE-2.0
##
##  Unless required by applicable law or agreed to in writing, software
##  distributed under the License is distributed on an "AS IS" BASIS,
##  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
##  See the License for the specific language governing permissions and
##  limitations under the License.
##
###############################################################################

import hashlib
from twisted.internet import reactor
from autobahn.websocket import WebSocketServerFactory, WebSocketServerProtocol


class FrameBasedHashServerProtocol(WebSocketServerProtocol):
   """
   Frame-based WebSockets server that computes a running SHA-256 for message data
   received. It will respond after every frame received with the digest computed
   up to that point. It can receive messages of unlimited number of frames.
   Digest is reset upon new message.
   """

   def onMessageBegin(self, opcode):
      self.sha256 = hashlib.sha256()

   def onMessageFrame(self, data, reserved):
      self.sha256.update(str(data))
      digest = self.sha256.hexdigest()
      self.sendMessage(digest)
      print "Sent digest for frame: %s" % digest

   def onMessageEnd(self):
      pass


if __name__ == '__main__':
   factory = WebSocketServerFactory()
   factory.protocol = FrameBasedHashServerProtocol
   reactor.listenTCP(9000, factory)
   reactor.run()