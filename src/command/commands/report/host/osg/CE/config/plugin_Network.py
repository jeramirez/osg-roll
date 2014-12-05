import rocks.commands

class Plugin(rocks.commands.Plugin):

	def provides(self):
		return 'Network'

#[sorting to] run after 'Gip' plugin 
	def requires(self):
		return ['Gip']

	def run(self, argv):
		# 1. Get the hostname and the config file to store
                host, addOutput, configs = argv 
		configFile               = configs['Network']

		OSG_GlobusTcpSourceRange= self.db.getHostAttr(host,'OSG_GlobusTcpSourceRange')
		OSG_GlobusTcpPortRange  = self.db.getHostAttr(host,'OSG_GlobusTcpPortRange')

		addOutput(host, '#begin config %s' % (configFile))
		addOutput(host, '/bin/cp -f /etc/osg/config.d/40-network.ini.template %s' % (configFile))
		if OSG_GlobusTcpSourceRange > 0:
			addOutput(host, 'sed -i -e "s@source_range = UNAVAILABLE@source_range = %s@" %s' % (OSG_GlobusTcpSourceRange,configFile))
		if OSG_GlobusTcpPortRange > 0:
			addOutput(host, 'sed -i -e "s@port_range = UNAVAILABLE@port_range = %s@" %s' % (OSG_GlobusTcpPortRange,configFile))
			addOutput(host, 'sed -i -e "s@port_state_file = UNAVAILABLE@port_state_file = /var/tmp/globus-port-state.log@" %s' % (configFile))
		addOutput(host, '#end config %s' % (configFile))
		addOutput(host, '')

