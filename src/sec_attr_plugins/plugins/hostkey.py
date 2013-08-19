# $Id: hostkey.py,v 1.0 2013/08/31 00:53:22 eduardo Exp $

import rocks.commands

import os, sys
import tempfile

class plugin(rocks.commands.sec_attr_plugin):
	def get_sec_attr(self):
		return 'hostkey'

	def filter(self, value):
		certkeyfile='/root/hostkey.pem'
		#open temporary file and write value there
		tf, tfname= tempfile.mkstemp()
		os.write(tf, value)
		os.close(tf)
		# Backup previous version if exist
		import shutil
		if os.path.exists(certkeyfile):
			shutil.move(certkeyfile, certkeyfile + '_' + tfname[8:])
		# Move temporary file to certkeyfile
		shutil.move(tfname, certkeyfile)
		os.chmod(certkeyfile, 0400)
