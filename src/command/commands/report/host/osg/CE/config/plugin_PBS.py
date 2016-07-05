import rocks.commands

class Plugin(rocks.commands.Plugin):

	def provides(self):
		return 'PBS'

#[sorting to] run after 'ManagedFork' plugin 
	def requires(self):
		return ['ManagedFork']

	def run(self, argv):
		# 1. Get the hostname and the config file to store
                host, addOutput, configs = argv 
		configFile               = configs['PBS']

		CEtype                   = self.db.getHostAttr(host,'OSG_CE')
		CEserv                   = self.db.getHostAttr(host,'OSG_CEServer')
		pbsloc                   = self.db.getHostAttr(host,'OSG_CE_pbs_location')
		pbsserver                = self.db.getHostAttr(host,'OSG_CE_pbs_server')
		pbs_acc                  = self.db.getHostAttr(host,'OSG_CE_pbs_accounting_log')

		if CEtype == 'pbs' and CEserv>0:
			addOutput(host, '#begin config %s' % (configFile))
			addOutput(host, '/bin/cp -f /etc/osg/config.d/20-pbs.ini.template %s' % (configFile))
			addOutput(host, 'sed -i -e "s@enabled = FALSE@enabled = TRUE@" %s' % (configFile))
			addOutput(host, 'sed -i -e "s@job_contact = host.name/jobmanager-pbs@job_contact = %s/jobmanager-pbs@" %s' % (CEserv, configFile))
			addOutput(host, 'sed -i -e "s@util_contact = host.name/jobmanager@util_contact = %s/jobmanager@" %s' % (CEserv,configFile))
			if pbsloc > 0:
				addOutput(host, 'sed -i -e "s@pbs_location = /usr@pbs_location = %s@" %s' % (pbsloc,configFile))
			if pbsserver > 0:
				addOutput(host, 'sed -i -e "s@pbs_server = UNAVAILABLE@pbs_server = %s@" %s' % (pbsserver,configFile))
			if pbs_acc > 0:
				addOutput(host, 'sed -i -e "s@accounting_log_directory = UNAVAILABLE@accounting_log_directory = %s@" %s' % (pbs_acc,configFile))
			addOutput(host, '#end config %s' % (configFile))
			addOutput(host, '')

