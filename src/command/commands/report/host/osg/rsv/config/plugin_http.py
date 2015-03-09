import rocks.commands

class Plugin(rocks.commands.Plugin):

	def provides(self):
		return 'http'

#[sorting to] run after 'ManagedFork' plugin
	def requires(self):
		return ['ManagedFork','Pbs','SGE','Condor']

	def run(self, argv):
		# 1. Get the hostname and the config file to store
                host, addOutput, configs = argv 
		confighttp               = configs['http']

		port                     = self.db.getHostAttr(host,'OSG_RSV_Port')
		sport                    = self.db.getHostAttr(host,'OSG_RSV_SPort')

		addOutput(host, '#begin config %s' % (confighttp))
		addOutput(host, '/bin/cp -f /etc/httpd/conf/httpd.conf.template %s' % (confighttp))
		if port>0:
			addOutput(host, 'sed -i -e "s#Listen 80#Listen %s#" %s' % (port,confighttp))
		addOutput(host, '#end config %s' % (confighttp))
		addOutput(host, '')

