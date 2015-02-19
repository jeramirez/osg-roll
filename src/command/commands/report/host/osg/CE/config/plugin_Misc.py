import rocks.commands

class Plugin(rocks.commands.Plugin):

	def provides(self):
		return 'Misc'

#[sorting to] run after 'Squid' plugin
	def requires(self):
		return ['Squid']

	def run(self, argv):
		# 1. Get the hostname and the config file to store
                host, addOutput, configs = argv 
		configFile               = configs['Misc']

		OSG_GumsServer          = self.db.getHostAttr(host,'OSG_GumsServer')

		addOutput(host, '#begin config %s' % (configFile))
		addOutput(host, '/bin/cp -f /etc/osg/config.d/10-misc.ini.template %s' % (configFile))
		addOutput(host, 'sed -i -e "s@glexec_location = UNAVAILABLE@glexec_location = /usr/sbin/glexec@" %s' % (configFile))
		if OSG_GumsServer > 0:
			addOutput(host, 'sed -i -e "s@gums_host = DEFAULT@gums_host = %s@" %s' % (OSG_GumsServer,configFile))
		addOutput(host, '#end config %s' % (configFile))
		addOutput(host, '')

