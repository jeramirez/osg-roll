# $Id: httpkey.py,v 1.0 2013/08/31 00:53:22 eduardo Exp $

import rocks.commands

import os, sys
import tempfile

class plugin(rocks.commands.sec_attr_plugin):
	def get_sec_attr(self):
		return 'rsvkey'

	def filter(self, value):
		certpath='/etc/grid-security/rsv'
		keyfile=certpath + '/rsvkey.pem'
		#open temporary file and write value there
		tf, tfname= tempfile.mkstemp()
		os.write(tf, value)
		os.close(tf)
		# Backup previous version if exist
		import shutil
		if not os.path.exists(certpath):
			os.makedirs(certpath, 755)
		if os.path.exists(keyfile):
			shutil.move(keyfile, keyfile + '_' + tfname[8:])
		# Move temporary file to keyfile
		shutil.move(tfname, keyfile)
		os.chmod(keyfile, 0400)
