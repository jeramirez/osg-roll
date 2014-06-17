# $Id: hostcert.py,v 1.0 2013/08/31 00:53:22 eduardo Exp $

import rocks.commands

import os, sys
import tempfile

class plugin(rocks.commands.sec_attr_plugin):
	def get_sec_attr(self):
		return 'hostcert'

	def filter(self, value):
		certfile='/root/hostcert.pem'
		certfile2='/etc/grid-security/hostcert.pem'
		#open temporary file and write value there
		tf, tfname= tempfile.mkstemp()
		os.write(tf, value)
		os.close(tf)
		# Backup previous version if exist
		import shutil
		if os.path.exists(certfile):
			shutil.move(certfile, certfile + '_' + tfname[8:])
		# Move temporary file to certfile
		shutil.move(tfname, certfile)
		os.chmod(certfile, 0444)
		# Copy  certfile to certfile2 if grid-dir exist
		if os.path.exists('/etc/grid-security'):
			shutil.copy(certfile, certfile2)
			os.chmod(certfile2, 0444)
