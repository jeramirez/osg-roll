import rocks.commands

class Plugin(rocks.commands.Plugin):

	def provides(self):
		return 'Gateway'

#[sorting to] run after 'Misc' plugin
	def requires(self):
		return ['Misc']

	def run(self, argv):
		# 1. Get the hostname and the config file to store
                host, addOutput, configs = argv 
		configFile               = configs['Gateway']

		OSG_CE_Gateway          = self.db.getHostAttr(host,'OSG_CE_Gateway')

		if OSG_CE_Gateway > 0:
			if OSG_CE_Gateway == 'gram' or OSG_CE_Gateway == 'GRAM' or OSG_CE_Gateway == 'both':
				OSG_GRAM = 'True'
			else:
				OSG_GRAM = 'False'

			if OSG_CE_Gateway == 'htcondor-ce' or OSG_CE_Gateway == 'condor-ce' or OSG_CE_Gateway == 'both':
				OSG_HTCONDORCE = 'True'
			else:
				OSG_HTCONDORCE = 'False'

			#protect agains mistakes (make sure at least one is true)
			if OSG_HTCONDORCE == 'False' and OSG_GRAM == 'False':
				OSG_HTCONDORCE = 'True'
				OSG_GRAM       = 'False'
		else:
			#default to both if not attr is set
			OSG_GRAM       = 'True'
			OSG_HTCONDORCE = 'True'

		addOutput(host, '#begin config %s' % (configFile))
		addOutput(host, '/bin/cp -f /etc/osg/config.d/10-gateway.ini.template %s' % (configFile))
		addOutput(host, 'sed -i -e "s@gram_gateway_enabled = False@gram_gateway_enabled = %s@" %s' % (OSG_GRAM,configFile))
		addOutput(host, 'sed -i -e "s@htcondor_gateway_enabled = True@htcondor_gateway_enabled = %s@" %s' % (OSG_HTCONDORCE,configFile))
		addOutput(host, "if [ \"1\" != `grep -c '\[HTCondorCE\]' %s ` ] ; then" % (configFile))
		addOutput(host, '  echo "" &gt;&gt; %s ' % (configFile))
		addOutput(host, '  echo "[HTCondorCE]" &gt;&gt; %s ' % (configFile))
		addOutput(host, '  echo "; Configuration related to the OSGCE (condor_ce)" &gt;&gt; %s ' % (configFile))
		addOutput(host, '  echo ";" &gt;&gt; %s ' % (configFile))
		addOutput(host, '  echo "enabled = True" &gt;&gt; %s ' % (configFile))
		addOutput(host, '  echo ";" &gt;&gt; %s ' % (configFile))
		addOutput(host, '  echo "; ; Required only if port is different from 9619 default." &gt;&gt; %s ' % (configFile))
		addOutput(host, '  echo "; ; port =" &gt;&gt; %s ' % (configFile))
		addOutput(host, '  echo "port = 9619" &gt;&gt; %s ' % (configFile))
		addOutput(host, "fi" )
		#prefer gram over htcondor-ce for bdii
		if OSG_GRAM == 'True':
			addOutput(host, 'sed -i -e "s@^enabled = True@enabled = False@" %s' % (configFile))
		addOutput(host, '#end config %s' % (configFile))
		addOutput(host, '')

