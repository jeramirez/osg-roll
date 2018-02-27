import rocks.commands

class Plugin(rocks.commands.Plugin):

	def provides(self):
		return 'Bosco'

#[sorting to] run after 'ManagedFork' plugin 
	def requires(self):
		return ['ManagedFork']

	def run(self, argv):
		# 1. Get the hostname and the config file to store
                host, addOutput, configs = argv 
		configFile               = configs['Bosco']

		CEtype                   = self.db.getHostAttr(host,'OSG_CE')
		CEserv                   = self.db.getHostAttr(host,'OSG_CEServer')
		boscousers               = self.db.getHostAttr(host,'OSG_CE_bosco_users')
		endpoint                 = self.db.getHostAttr(host,'OSG_CE_bosco_endpoint')
		batch                    = self.db.getHostAttr(host,'OSG_CE_bosco_batch')
		sshkey                   = self.db.getHostAttr(host,'OSG_CE_bosco_sshkey')
		slurmboscoroutes         ='/etc/condor-ce/config.d/90-bosco-routes.conf'

		if CEtype == 'bosco' and CEserv>0:
			addOutput(host, '#begin config %s' % (configFile))
			addOutput(host, '/bin/cp -f /etc/osg/config.d/20-bosco.ini.template %s' % (configFile))
			addOutput(host, 'sed -i -e "s@enabled = FALSE@enabled = TRUE@" %s' % (configFile))
			if boscousers > 0:
				addOutput(host, 'sed -i -e "s@users = UNAVAILABLE@users = %@" %s' % (boscousers, configFile))
			if endpoint > 0:
				addOutput(host, 'sed -i -e "s/endpoint = UNAVAILABLE/endpoint = %s/" %s' % (endpoint,configFile))
			if batch > 0:
				if  batch == 'slurm':
					addOutput(host, 'sed -i -e "s@batch = UNAVAILABLE@batch = pbs@" %s' % (configFile))
				else:
					addOutput(host, 'sed -i -e "s@batch = UNAVAILABLE@batch = %s@" %s' % (batch,configFile))
			if sshkey > 0:
				addOutput(host, 'sed -i -e "s@ssh_key = UNAVAILABLE@ssh_key = %s@" %s' % (sshkey,configFile))
			else:
				addOutput(host, 'sed -i -e "s@ssh_key = UNAVAILABLE@ssh_key = /etc/osg/bosco.key@" %s' % (configFile))
			addOutput(host, '#end config %s' % (configFile))
			addOutput(host, '')
			if batch == 'slurm':
				addOutput(host, '#begin overwrite routes for slurm %s' % (slurmboscoroutes))
				addOutput(host, 'echo  %s' % (slurmboscoroutes))
				addOutput(host, '#end overwrite routes for slurm %s' % (slurmboscoroutes))
				addOutput(host, '')

