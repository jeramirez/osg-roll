import rocks.commands

class Plugin(rocks.commands.Plugin):

	def provides(self):
		return 'ManagedFork'

#[sorting to] run after 'Storage' plugin 
	def requires(self):
		return ['Storage']

	def run(self, argv):
		# 1. Get the hostname and the config file to store
                host, addOutput, configs = argv 
		configFile               = configs['ManagedFork']

		addOutput(host, '#begin config %s' % (configFile))
		addOutput(host, '/bin/cp -f /etc/osg/config.d/15-managedfork.ini.template %s' % (configFile))
		addOutput(host, 'sed -i -e "s@enabled = FALSE@enabled = TRUE@" %s' % (configFile))
		addOutput(host, '#end config %s' % (configFile))
		addOutput(host, '')
