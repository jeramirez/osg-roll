import rocks.commands

class Plugin(rocks.commands.Plugin):

	def provides(self):
		return 'Squid'

	def run(self, argv):
		# 1. Get the hostname and the config file to store
                host, addOutput, configs = argv 
		configFile               = configs['Squid']

		OSG_SquidServer          = self.db.getHostAttr(host,'OSG_SquidServer')

		addOutput(host, '#begin config %s' % (configFile))
		addOutput(host, '/bin/cp -f /etc/osg/config.d/01-squid.ini.template %s' % (configFile))
		if OSG_SquidServer > 0:
			addOutput(host, 'sed -i -e "s@location = @location = %s@" %s' % (OSG_SquidServer,configFile))
		else:
			addOutput(host, 'sed -i -e "s@enabled = True@enabled = False@" %s' % (configFile) )
			addOutput(host, 'sed -i -e "s@location = @location = UNAVAILABLE@" %s' % (configFile))
		addOutput(host, '#end config %s' % (configFile))
		addOutput(host, '')

