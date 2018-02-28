import rocks.commands

class Plugin(rocks.commands.Plugin):

	def provides(self):
		return 'FetchCrl'

	def run(self, argv):
		# 1. Get the hostname and the config file to store
                host, addOutput, configs = argv 
		Fetchcrl           = configs['FetchCrl']

		squid              = self.db.getHostAttr(host,'OSG_SquidServer')
		proxy              = self.db.getHostAttr(host,'OSG_CVMFS_HTTP_PROXY')

		addOutput(host, '#begin config %s' % (Fetchcrl))
		addOutput(host, '/bin/rm -f %s' % (Fetchcrl))
		addOutput(host, '/bin/touch -f %s' % (Fetchcrl))
		addOutput(host, 'echo "infodir = /etc/grid-security/certificates.osg-ca-certs" &gt;&gt; %s' % (Fetchcrl))
		if squid>0:
			if ":" in squid:
				addOutput(host, 'echo "http_proxy = http://%s" &gt;&gt; %s' % (squid,Fetchcrl))
			else:
				addOutput(host, 'echo "http_proxy = http://%s:3128" &gt;&gt; %s' % (squid,Fetchcrl))
		elif proxy>0:
			addOutput(host, 'echo "http_proxy = %s" &gt;&gt; %s' % (proxy,Fetchcrl))

		addOutput(host, '#end config %s' % (Fetchcrl))
		addOutput(host, '')

