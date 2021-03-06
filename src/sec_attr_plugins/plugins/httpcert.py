# $Id: httpcert.py,v 1.0 2013/08/31 00:53:22 eduardo Exp $

import rocks.commands

import os, sys
import tempfile

class plugin(rocks.commands.sec_attr_plugin):
	def get_sec_attr(self):
		return 'httpcert'

	def filter(self, value):
		certpath='/etc/grid-security/http'
		certfile=certpath + '/httpcert.pem'
		uid     = 91 #tomcat uid
		gid     = 91 #tomcat gid
		#open temporary file and write value there
		tf, tfname= tempfile.mkstemp()
		os.write(tf, value)
		os.close(tf)
		# Backup previous version if exist
		import shutil
		if not os.path.exists(certpath):
			os.makedirs(certpath, 0755)
		if os.path.exists(certfile):
			uid=os.stat(certfile).st_uid
			gid=os.stat(certfile).st_gid
			shutil.move(certfile, certfile + '_' + tfname[8:])
		# Move temporary file to certfile
		shutil.move(tfname, certfile)
		os.chmod(certfile, 0444)
		os.chown(certfile, uid, gid)
