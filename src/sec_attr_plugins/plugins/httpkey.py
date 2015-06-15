# $Id: httpkey.py,v 1.0 2013/08/31 00:53:22 eduardo Exp $

import rocks.commands

import os, sys
import tempfile

class plugin(rocks.commands.sec_attr_plugin):
	def get_sec_attr(self):
		return 'httpkey'

	def filter(self, value):
		certpath='/etc/grid-security/http'
		keyfile =certpath + '/httpkey.pem'
		uid     = 91 # tomcat uid
		gid     = 91 # tomcat gid
		#open temporary file and write value there
		tf, tfname= tempfile.mkstemp()
		os.write(tf, value)
		os.close(tf)
		# Backup previous version if exist
		import shutil
		if not os.path.exists(certpath):
			os.makedirs(certpath, 755)
		if os.path.exists(keyfile):
			uid=os.stat(certfile).st_uid
			gid=os.stat(certfile).st_gid
			shutil.move(keyfile, keyfile + '_' + tfname[8:])
		# Move temporary file to keyfile
		shutil.move(tfname, keyfile)
		os.chmod(keyfile, 0400)
		os.chown(keyfile, uid, gid)
