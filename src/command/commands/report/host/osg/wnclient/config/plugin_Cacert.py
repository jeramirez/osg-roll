import rocks.commands

class Plugin(rocks.commands.Plugin):

	def provides(self):
		return 'Cacert'

	def run(self, argv):
		# 1. Get the hostname and the config file to store
                host, addOutput, configs = argv 
		certdir            = configs['Cacert']

		cacert             = self.db.getHostAttr(host,'OSG_wn_Cacert')

		addOutput(host, '#begin config %s' % (certdir))
		addOutput(host, 'rm -f %s' % (certdir))
		if cacert == 'own':
			addOutput(host, 'ln -s /etc/grid-security/certificates.osg-ca-certs %s' % (certdir))
		elif cacert == 'linkCVMFS':
			addOutput(host, 'ln -s /cvmfs/oasis.opensciencegrid.org/mis/certificates %s' % (certdir))
		else:
#			default to cacert == 'linkCE':
			addOutput(host, '#attr OSG_wn_Cacert=%s [not "own" nor "linkCVMFS"] defaulting to "linkCE"' % (cacert))
			addOutput(host, 'ln -s &OSG_CE_Mount_ShareDir;/ce/globus/share/certificates %s' % (certdir))

		addOutput(host, '#end config %s' % (certdir))
		addOutput(host, '')

