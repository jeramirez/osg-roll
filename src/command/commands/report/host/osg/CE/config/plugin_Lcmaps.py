import rocks.commands

class Plugin(rocks.commands.Plugin):

	def provides(self):
		return 'Lcmaps'

	def run(self, argv):
		# 1. Get the hostname and the config file to store
                host, addOutput, configs = argv 
		Lcmaps             = configs['Lcmaps']

		gums               = self.db.getHostAttr(host,'OSG_GumsServer')

		addOutput(host, '#begin config %s' % (Lcmaps))
		addOutput(host, '/bin/cp -f /etc/lcmaps.db.template %s' % (Lcmaps))
		if gums>0:
			addOutput(host, 'sed -i -e "s#yourgums.yourdomain#%s#" %s' % (gums,Lcmaps))

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

