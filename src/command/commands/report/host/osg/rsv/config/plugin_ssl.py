import rocks.commands

class Plugin(rocks.commands.Plugin):

	def provides(self):
		return 'ssl'

#[sorting to] run after 'ManagedFork' plugin
	def requires(self):
		return ['ManagedFork','Pbs','SGE','Condor']

	def run(self, argv):
		# 1. Get the hostname and the config file to store
                host, addOutput, configs = argv 
		configssl                = configs['ssl']

		port                     = self.db.getHostAttr(host,'OSG_RSV_Port')
		sport                    = self.db.getHostAttr(host,'OSG_RSV_SPort')

		addOutput(host, '#begin config %s' % (configssl))
		addOutput(host, '/bin/cp -f /etc/httpd/conf.d/ssl.conf.template %s' % (configssl))
		if sport>0:
			addOutput(host, 'sed -i -e "s#Listen 443#Listen %s#" %s' % (sport,configssl))
			addOutput(host, 'sed -i -e "s#VirtualHost _default_:443#VirtualHost _default_:%s#" %s' % (sport,configssl))
		addOutput(host, 'sed -i -e "s#SSLCertificateFile /etc/pki/tls/certs/localhost.crt#SSLCertificateFile /etc/grid-security/http/httpcert2.pem#" %s' % (configssl))
		addOutput(host, 'sed -i -e "s#SSLCertificateKeyFile /etc/pki/tls/private/localhost.key#SSLCertificateKeyFile /etc/grid-security/http/httpkey2.pem#" %s' % (configssl))
		addOutput(host, '#end config %s' % (configssl))
		addOutput(host, '')

