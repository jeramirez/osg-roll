import rocks.commands

class Plugin(rocks.commands.Plugin):

	def provides(self):
		return 'Slurm'

#[sorting to] run after 'ManagedFork' plugin 
	def requires(self):
		return ['ManagedFork']

	def run(self, argv):
		# 1. Get the hostname and the config file to store
                host, addOutput, configs = argv 
		configFile               = configs['Slurm']

		CEtype                   = self.db.getHostAttr(host,'OSG_CE')
		CEserv                   = self.db.getHostAttr(host,'OSG_CEServer')
		slurmloc                 = self.db.getHostAttr(host,'OSG_CE_slurm_location')
		db_host                  = self.db.getHostAttr(host,'OSG_CE_slurm_db_host')
		db_port                  = self.db.getHostAttr(host,'OSG_CE_slurm_db_port')
		db_user                  = self.db.getHostAttr(host,'OSG_CE_slurm_db_user')
		db_pass                  = self.db.getHostAttr(host,'OSG_CE_slurm_db_pass')
		db_name                  = self.db.getHostAttr(host,'OSG_CE_slurm_db_name')

		if CEtype == 'slurm' and CEserv>0:
			addOutput(host, '#begin config %s' % (configFile))
			addOutput(host, '/bin/cp -f /etc/osg/config.d/20-slurm.ini.template %s' % (configFile))
			addOutput(host, 'sed -i -e "s@enabled = FALSE@enabled = TRUE@" %s' % (configFile))
			addOutput(host, 'sed -i -e "s@job_contact = host.name/jobmanager-pbs@job_contact = %s/jobmanager-pbs@" %s' % (CEserv, configFile))
			addOutput(host, 'sed -i -e "s@util_contact = host.name/jobmanager@util_contact = %s/jobmanager@" %s' % (CEserv,configFile))
			if slurmloc > 0:
				addOutput(host, 'sed -i -e "s@slurm_location = /usr@slurm_location = %s@" %s' % (slurmloc,configFile))
			if db_host > 0:
				addOutput(host, 'sed -i -e "s@db_host = UNAVAILABLE@db_host = %s@" %s' % (db_host,configFile))
			if db_port > 0:
				addOutput(host, 'sed -i -e "s@db_port = UNAVAILABLE@db_port = %s@" %s' % (db_port,configFile))
			if db_user > 0:
				addOutput(host, 'sed -i -e "s@db_user = UNAVAILABLE@db_user = %s@" %s' % (db_user,configFile))
			if db_pass > 0:
				addOutput(host, 'sed -i -e "s@db_pass = UNAVAILABLE@db_pass = %s@" %s' % (db_pass,configFile))
			if db_name > 0:
				addOutput(host, 'sed -i -e "s@db_name = UNAVAILABLE@db_name = %s@" %s' % (db_name,configFile))
			addOutput(host, '#end config %s' % (configFile))
			addOutput(host, '')

