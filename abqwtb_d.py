#!/usr/bin/env python

import go
import sys, time
from daemon import Daemon
from threading import Thread
import logging
 
def update_all():
  try:
    data = go.go(go.live())
    bus.locate(data)
  except:
    logging.exception("Exception in Update")
    raise

class WTBDaemon(Daemon):

      def run(self):
	while(1):
          try:
            thread = Thread(target = update_all)
            logging.debug('running update')
	    thread.start()
            time.sleep(15)
	    while(thread.isAlive()):
              logging.warning('last update not finished')
	      time.sleep(15)	  
          except:
            logging.error(sys.exc_info()[0])
            raise

if __name__ == "__main__":
  try:  
    logging.basicConfig(filename='/home/chughes/wtb.log',level=logging.WARNING)
    bus = __import__("busstop-vicinity")
    daemon = WTBDaemon('/tmp/daemon-wtb.pid')
    if len(sys.argv) == 2:
      if 'start' == sys.argv[1]:
        daemon.start()
      elif 'stop' == sys.argv[1]:
        daemon.stop()
      elif 'restart' == sys.argv[1]:
        daemon.restart()
      else:
        print "Unknown command"
        sys.exit(2)
      sys.exit(0)
    else:
      print "usage: %s start|stop|restart" % sys.argv[0]
      sys.exit(2)
  except Exception as e:
    logging.error(sys.exc_info()[0])
    logging.error(e)
    raise
