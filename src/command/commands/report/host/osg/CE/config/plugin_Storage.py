import rocks.commands

class Plugin(rocks.commands.Plugin):

	def provides(self):
		return 'Storage'

#[sorting to] run after 'Misc' plugin
	def requires(self):
		return ['Misc']

	def run(self, argv):
		# 1. Get the hostname and the config file to store
                host, addOutput, configs = argv 
		configFile               = configs['Storage']

		OSG_CE_nfs              = self.db.getHostAttr(host,'OSG_CE_Mount_ShareDir')
		OSG_CE_AppDir           = self.db.getHostAttr(host,'OSG_CE_AppDir')
		OSG_CE_DataDir          = self.db.getHostAttr(host,'OSG_CE_DataDir')
		OSG_WN_TmpDir           = self.db.getHostAttr(host,'OSG_WN_TmpDir')
		OSG_SEServer            = self.db.getHostAttr(host,'OSG_SEServer')
		OSG_SRMPort             = self.db.getHostAttr(host,'OSG_SRMPort')

		addOutput(host, '#begin config %s' % (configFile))
		addOutput(host, '/bin/cp -f /etc/osg/config.d/10-storage.ini.template %s' % (configFile))
		addOutput(host, 'sed -i -e "s@se_available = FALSE@se_available = TRUE@" %s' % (configFile))
		addOutput(host, 'sed -i -e "s@default_se = UNAVAILABLE@default_se = %s@" %s' % (OSG_SEServer,configFile))
		if OSG_CE_AppDir>0:
			addOutput(host, 'sed -i -e "s@app_dir = UNAVAILABLE@app_dir = %s@" %s' % (OSG_CE_AppDir,configFile))
		else:
			addOutput(host, 'sed -i -e "s@app_dir = UNAVAILABLE@app_dir = %s/app@" %s' % (OSG_CE_nfs,configFile))
		addOutput(host, 'sed -i -e "s@data_dir = UNAVAILABLE@data_dir = %s@" %s' % (OSG_CE_DataDir,configFile))
		addOutput(host, 'sed -i -e "s@worker_node_temp = UNAVAILABLE@worker_node_temp = %s@" %s' % (OSG_WN_TmpDir,configFile))
		if OSG_SRMPort>0:
			addOutput(host, 'sed -i -e "s@site_read = UNAVAILABLE@site_read = srm://%s:%s/srm/v2/server@" %s' % (OSG_SEServer,OSG_SRMPort,configFile))
			addOutput(host, 'sed -i -e "s@site_write = UNAVAILABLE@site_write = srm://%s:%s/srm/v2/server@" %s' % (OSG_SEServer,OSG_SRMPort,configFile))
		else:
			addOutput(host, 'sed -i -e "s@site_read = UNAVAILABLE@site_read = srm://%s:8443/srm/v2/server@" %s' % (OSG_SEServer,configFile))
			addOutput(host, 'sed -i -e "s@site_write = UNAVAILABLE@site_write = srm://%s:8443/srm/v2/server@" %s' % (OSG_SEServer,configFile))
		addOutput(host, '#end config %s' % (configFile))
		addOutput(host, '')

