# $Id: boscokey.py,v 1.0 2013/08/31 00:53:22 eduardo Exp $

import rocks.commands

import os, sys
import tempfile

class plugin(rocks.commands.sec_attr_plugin):
	def get_sec_attr(self):
		return 'boscokey'

	def filter(self, value):
		certpath='/etc/osg'
		keyfile =certpath + '/bosco.key'
		uid     = 0 # root uid
		gid     = 0 # root gid
		#open temporary file and write value there
		tf, tfname= tempfile.mkstemp()
		os.write(tf, value)
		os.close(tf)
		# Backup previous version if exist
		import shutil
		if not os.path.exists(certpath):
			os.makedirs(certpath, 0755)
		if os.path.exists(keyfile):
			uid=os.stat(keyfile).st_uid
			gid=os.stat(keyfile).st_gid
			shutil.move(keyfile, keyfile + '_' + tfname[8:])
		# Move temporary file to keyfile
		shutil.move(tfname, keyfile)
		os.chmod(keyfile, 0400)
		os.chown(keyfile, uid, gid)
