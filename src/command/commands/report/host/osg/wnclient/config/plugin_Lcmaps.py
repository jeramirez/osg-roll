import os
import rocks.commands

class Plugin(rocks.commands.Plugin):

	def provides(self):
		return 'Lcmaps'

	def run(self, argv):
		# 1. Get the hostname and the config file to store
		host, addOutput, configs = argv 

		Lcmaps             = configs['Lcmaps']

		wrapper = ''
		cmd = '/opt/rocks/bin/rocks report host osg lcmaps config '
		cmd += '%s ' % host
		cmd += 'ConfigLcmaps=%s ' % Lcmaps
		cmd += 'embeded=true '

		for line in os.popen(cmd).readlines():
			wrapper += line

		addOutput(host, wrapper)

