import rocks.commands

class Plugin(rocks.commands.Plugin):

	def provides(self):
		return 'Rsv'

#[sorting to] run after 'ManagedFork' plugin
	def requires(self):
		return ['ManagedFork','Pbs','SGE','Condor']

	def run(self, argv):
		# 1. Get the hostname and the config file to store
                host, addOutput, configs = argv 
		configFile               = configs['Rsv']

		OSG_CE                   = self.db.getHostAttr(host,'OSG_CEServer')
		OSG_CEhost               = self.db.getHostAttr(host,'OSGCEPrivate')
		OSG_CEtype               = self.db.getHostAttr(OSG_CEhost,'OSG_CE')
		osg_gums                 = self.db.getHostAttr(host,'OSG_GumsServer')
		OSG_gridftp              = self.db.getHostAttr(host,'OSG_GFTPServer')
		OSG_gftplist             = self.db.getHostAttr(host,'OSG_RSVGFTPList')
		OSG_SEServer             = self.db.getHostAttr(host,'OSG_SEServer')
		OSG_SRMPort              = self.db.getHostAttr(host,'OSG_SRMPort')
		OSG_SRMDIR               = self.db.getHostAttr(host,'OSG_RSVSRMTestDir')


		addOutput(host, '#begin config %s' % (configFile))
		addOutput(host, '/bin/cp -f /etc/osg/config.d/30-rsv.ini.template %s' % (configFile))
		addOutput(host, 'sed -i -e "s@service_cert  = DEFAULT@service_cert  = /etc/grid-security/rsv/rsvcert.pem@" %s' % (configFile))
		addOutput(host, 'sed -i -e "s@service_key  = DEFAULT@service_key  = /etc/grid-security/rsv/rsvkey.pem@" %s' % (configFile))
		addOutput(host, 'sed -i -e "s@ce_hosts = UNAVAILABLE@ce_hosts = %s@" %s' % (OSG_CE,configFile))
		#at least OSG_GFTPServer should be defined, but just in case put within an 'if'
		if OSG_gridftp>0:
			if OSG_gftplist>0:
				addOutput(host, 'sed -i -e "s@;gridftp_hosts = UNAVAILABLE@gridftp_hosts = %s@" %s' % (OSG_gftplist,configFile))
			else:
				addOutput(host, 'echo "#WARNING# attr OSG_RSVGFTPList not defined to be used in gridftp_hosts"' )
				addOutput(host, 'echo "#WARNING#                   alternatively using OSG_GFTPServer"' )
				addOutput(host, 'sed -i -e "s@;gridftp_hosts = UNAVAILABLE@gridftp_hosts = %s@" %s' % (OSG_gridftp,configFile))
		else:
			addOutput(host, 'echo "#WARNING# attrs OSG_RSVGFTPList or OSG_GFTPServer not defined to be used in gridftp_hosts"' )

		if OSG_CEhost>0 and OSG_CEtype>0:
			addOutput(host, 'sed -i -e "s@gratia_probes = DEFAULT@gratia_probes = metric, %s@" %s' % (OSG_CEtype,configFile))

		if osg_gums>0:
			addOutput(host, 'sed -i -e "s@gums_hosts = UNAVAILABLE@gums_hosts = %s@" %s' % (osg_gums,configFile))
		if OSG_SEServer>0:
			if OSG_SRMPort>0:
				addOutput(host, 'sed -i -e "s@srm_hosts = UNAVAILABLE@srm_hosts = %s:%s@" %s' % (OSG_SEServer,OSG_SRMPort,configFile))
			else:
				addOutput(host, 'sed -i -e "s@srm_hosts = UNAVAILABLE@srm_hosts = %s:8443@" %s' % (OSG_SEServer,configFile))
			addOutput(host, 'sed -i -e "s@srm_webservice_path = DEFAULT@srm_webservice_path = srm/v2/server@" %s' % (configFile))
			if OSG_SRMDIR>0:
				addOutput(host, 'sed -i -e "s@srm_dir = DEFAULT@srm_dir = %s@" %s' % (OSG_SRMDIR,configFile))
			else:
				addOutput(host, 'echo "#WARNING# attr OSG_RSVSRMTestDir not defined to be used in srm_dir"' )
		if OSG_CEtype>0 and OSG_CEtype=='condor':
			addOutput(host, 'sed -i -e "s@condor_location = UNAVAILABLE@;condor_location = UNAVAILABLE@" %s' % (configFile))

		addOutput(host, '#end config %s' % (configFile))
		addOutput(host, '')

