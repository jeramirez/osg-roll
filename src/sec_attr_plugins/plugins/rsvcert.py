# $Id: httpcert.py,v 1.0 2013/08/31 00:53:22 eduardo Exp $

import rocks.commands

import os, sys
import tempfile

class plugin(rocks.commands.sec_attr_plugin):
	def get_sec_attr(self):
		return 'rsvcert'

	def filter(self, value):
		certpath='/etc/grid-security/rsv'
		certfile=certpath + '/rsvcert.pem'
		rsv     = 0 #default root
		#open temporary file and write value there
		tf, tfname= tempfile.mkstemp()
		os.write(tf, value)
		os.close(tf)
		# Backup previous version if exist
		import shutil
		if not os.path.exists(certpath):
			os.makedirs(certpath, 0755)
		if os.path.exists(certfile):
			rsv=os.stat(certfile).st_uid
			shutil.move(certfile, certfile + '_' + tfname[8:])
		# Move temporary file to certfile
		shutil.move(tfname, certfile)
		os.chmod(certfile, 0444)
		os.chown(certfile, rsv, -1)
