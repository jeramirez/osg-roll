import rocks.commands

class Plugin(rocks.commands.Plugin):

	def provides(self):
		return 'SGE'

#[sorting to] run after 'ManagedFork' plugin 
	def requires(self):
		return ['ManagedFork']

	def run(self, argv):
		# 1. Get the hostname and the config file to store
                host, addOutput, configs = argv 
		configFile               = configs['SGE']

		CEtype                   = self.db.getHostAttr(host,'OSG_CE')
		CEserv                   = self.db.getHostAttr(host,'OSG_CEServer')

		if CEtype == 'sge' and CEserv>0:
			addOutput(host, '#begin config %s' % (configFile))
			addOutput(host, '/bin/cp -f /etc/osg/config.d/20-sge.ini.template %s' % (configFile))
			addOutput(host, 'sed -i -e "s@enabled = FALSE@enabled = TRUE@" %s' % (configFile))
			addOutput(host, 'sed -i -e "s@job_contact = host.name/jobmanager-sge@job_contact = %s/jobmanager-sge@" %s' % (CEserv, configFile))
			addOutput(host, 'sed -i -e "s@util_contact = host.name/jobmanager@util_contact = %s/jobmanager@" %s' % (CEserv,configFile))
			addOutput(host, '#end config %s' % (configFile))
			addOutput(host, '')

