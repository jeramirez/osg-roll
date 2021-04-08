import rocks.commands

class Plugin(rocks.commands.Plugin):

	def provides(self):
		return 'usrnmspc'

	def run(self, argv):
		# 1. Get the hostname and the config file to store
                host, addOutput, configs = argv 
		Fetchcrl           = configs['FetchCrl']
		usrnmspc           = '/etc/sysctl.d/90-max_user_namespaces_wn_osg_roll.conf'

		enable              = self.db.getHostAttr(host,'OSG_wn_enable_usernamespace')

		addOutput(host, '#begin config %s' % (usrnmspc))
		addOutput(host, '/bin/rm -f %s' % (usrnmspc))

		if enable:
			addOutput(host, '/bin/touch -f %s' % (usrnmspc))
			addOutput(host, 'echo "user.max_user_namespaces = 15000" &gt;&gt; %s' % (usrnmspc))
			addOutput(host, '/sbin/sysctl -p %s' % (usrnmspc))
		addOutput(host, '#end config %s' % (usrnmspc))
		addOutput(host, '')

