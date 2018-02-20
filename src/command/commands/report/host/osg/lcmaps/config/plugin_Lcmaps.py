import rocks.commands

class Plugin(rocks.commands.Plugin):

	def provides(self):
		return 'Lcmaps'

	def run(self, argv):
		# 1. Get the hostname and the config file to store
                host, addOutput, configs = argv 
		Lcmaps             = configs['Lcmaps']

		certype            = self.db.getHostAttr(host,'OSG_wn_LcmapsCertType')
		gums               = self.db.getHostAttr(host,'OSG_GumsServer')

		addOutput(host, '#begin config %s' % (Lcmaps))
#		make sure there is a template!
		addOutput(host, '[ ! -f /etc/lcmaps.db.template ]&amp;&amp;cp -p /etc/lcmaps.db /etc/lcmaps.db.template')
		addOutput(host, '/bin/cp -f /etc/lcmaps.db.template %s' % (Lcmaps))
		if gums>0:
			addOutput(host, 'sed -i -e "s#yourgums.yourdomain#%s#" %s' % (gums,Lcmaps))
			if certype>0:
				if certype == 'proxy': 
					addOutput(host, 'sed -i -e "s#hostcert.pem#hostproxy.pem#" %s' % (Lcmaps))
					addOutput(host, 'sed -i -e "s#hostkey.pem#hostproxykey.pem#" %s' % (Lcmaps))
				elif certype == 'pilot': 
					addOutput(host, 'sed -i -e "s@             \\\"-cert   /etc/grid-security/hostcert.pem\\\"@#             \\\"-cert   /etc/grid-security/hostcert.pem\\\"@" %s' % (Lcmaps))
					addOutput(host, 'sed -i -e "s@             \\\"-key    /etc/grid-security/hostkey.pem\\\"@#             \\\"-key    /etc/grid-security/hostkey.pem\\\"@" %s' % (Lcmaps))
					addOutput(host, 'sed -i -e "s@             \\\"--cert-owner root\\\"@#             \\\"--cert-owner root\\\"@" %s' % (Lcmaps))
				else:
					#Anything else uses hostcert/key unmodified 
					addOutput(host, 'echo ##attr OSG_wn_LcmapsCertType=%s [not proxy nor pilot], defaulting to "cert"' % (certype))
			#if undefined attr OSG_wn_LcmapsCertType defaulting to proxy
			else:
				addOutput(host, 'echo ##attr OSG_wn_LcmapsCertType not defined for WN, defaulting to "proxy"')
				addOutput(host, 'sed -i -e "s#hostcert.pem#hostproxy.pem#" %s' % (Lcmaps))
				addOutput(host, 'sed -i -e "s#hostkey.pem#hostproxykey.pem#" %s' % (Lcmaps))

			addOutput(host, 'sed -i -e "s/#glexectracking = \\\"lcmaps_glexec_tracking.mod\\\"/glexectracking = \\\"lcmaps_glexec_tracking.mod\\\"/" %s' % (Lcmaps))
			addOutput(host, 'sed -i -e "s@#         \\\"-exec /usr/sbin/glexec_monitor\\\"@         \\\"-exec /usr/sbin/glexec_monitor\\\"@" %s' % (Lcmaps))
			addOutput(host, 'sed -i -e "s@#verifyproxy -&gt; gumsclient@verifyproxy -&gt; gumsclient@" %s' % (Lcmaps))
			addOutput(host, 'sed -i -e "s@#gumsclient -&gt; glexectracking@gumsclient -&gt; glexectracking@" %s' % (Lcmaps))
#			addOutput(host, 'echo "#start rocks additions" &gt;&gt; %s' % (Lcmaps))
#			addOutput(host, 'echo "verifyproxy -&gt; gumsclient" &gt;&gt; %s' % (Lcmaps))
#			addOutput(host, 'echo "gumsclient -&gt; glexectracking" &gt;&gt; %s' % (Lcmaps))
#			addOutput(host, 'echo "#end rocks additions" &gt;&gt; %s' % (Lcmaps))

		else:
			#set vomsmap
			addOutput(host, 'sed -i -e "s@gumsclient -&gt; good | bad@#gumsclient -&gt; good | bad@" %s' % (Lcmaps))
			addOutput(host, 'sed -i -e "s@#verifyproxynokey -&gt; banfile@verifyproxynokey -&gt; banfile@" %s' % (Lcmaps))
			addOutput(host, 'sed -i -e "s@#banfile -&gt; banvomsfile@banfile -&gt; banvomsfile@" %s' % (Lcmaps))
			addOutput(host, 'sed -i -e "s@#banvomsfile -&gt; gridmapfile | bad@banvomsfile -&gt; gridmapfile | bad@" %s' % (Lcmaps))
			addOutput(host, 'sed -i -e "s@#gridmapfile -&gt; good | vomsmapfile@gridmapfile -&gt; good | vomsmapfile@" %s' % (Lcmaps))
			addOutput(host, 'sed -i -e "s@#vomsmapfile -&gt; good | defaultmapfile@vomsmapfile -&gt; good | defaultmapfile@" %s' % (Lcmaps))
			addOutput(host, 'sed -i -e "s@#defaultmapfile -&gt; good | bad@defaultmapfile -&gt; good | bad@" %s' % (Lcmaps))

		addOutput(host, '#end config %s' % (Lcmaps))
		addOutput(host, '')

