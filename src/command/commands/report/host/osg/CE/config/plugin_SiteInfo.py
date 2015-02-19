import rocks.commands

class Plugin(rocks.commands.Plugin):

	def provides(self):
		return 'SiteInfo'

#[sorting to] run after 'Network' plugin 
	def requires(self):
		return ['Network']

	def run(self, argv):
		# 1. Get the hostname and the config file to store
                host, addOutput, configs = argv 
		configFile               = configs['SiteInfo']

		CEserv    = self.db.getHostAttr(host,'OSG_CEServer')
		group     = self.db.getHostAttr(host,'OSG_CE_siteinfo_group')
		OIM_name  = self.db.getHostAttr(host,'OSG_CE_siteinfo_OIM_name')
		OIM_group = self.db.getHostAttr(host,'OSG_CE_siteinfo_OIM_group')
		sponsor   = self.db.getHostAttr(host,'OSG_CE_siteinfo_sponsor')
		policy    = self.db.getHostAttr(host,'OSG_CE_siteinfo_policy')
		contact   = self.db.getHostAttr(host,'OSG_CE_siteinfo_contact')
		email     = self.db.getHostAttr(host,'OSG_CE_siteinfo_email')
		city      = self.db.getHostAttr(host,'OSG_CE_siteinfo_city')
		country   = self.db.getHostAttr(host,'OSG_CE_siteinfo_country')
		longitude = self.db.getHostAttr(host,'OSG_CE_siteinfo_longitude')
		latitude  = self.db.getHostAttr(host,'OSG_CE_siteinfo_latitude')
		latlong   = self.db.getHostAttr(host,'Info_ClusterLatlong')
		latitude2,longitude2 = latlong.split(' ',1)

		addOutput(host, '#begin config %s' % (configFile))
		addOutput(host, '/bin/cp -f /etc/osg/config.d/40-siteinfo.ini.template %s' % (configFile))
		if group > 0:
			addOutput(host, 'sed -i -e "s@group = OSG@group = %s@" %s' % (group,configFile))
		else:
			addOutput(host, '#attr OSG_CE_siteinfo_group not defined for CE server')
			addOutput(host, '#### default is group = OSG in %s' % (configFile))
		if CEserv > 0:
			addOutput(host, 'sed -i -e "s@host_name = UNAVAILABLE@host_name = %s@" %s' % (CEserv,configFile))
		if OIM_name > 0:
			addOutput(host, 'sed -i -e "s@resource = UNAVAILABLE@resource = %s@" %s' % (OIM_name,configFile))
		else:
			addOutput(host, '#attr OSG_CE_siteinfo_OIM_name not defined for CE server')
			addOutput(host, '#### default is resource = UNAVAILABLE in %s' % (configFile))

		if OIM_group > 0:
			addOutput(host, 'sed -i -e "s@resource_group = UNAVAILABLE@resource_group = %s@" %s' % (OIM_group,configFile))
		else:
			addOutput(host, '#attr OSG_CE_siteinfo_OIM_group not defined for CE server')
			addOutput(host, '#### default is resource_group = UNAVAILABLE in %s' % (configFile))
		if sponsor > 0:
			addOutput(host, 'sed -i -e "s@sponsor = UNAVAILABLE@sponsor = %s@" %s' % (sponsor,configFile))
		else:
			addOutput(host, '#attr OSG_CE_siteinfo_sponsor not defined for CE server')
			addOutput(host, 'echo "attr OSG_CE_siteinfo_sponsor not defined for CE server"')
			addOutput(host, '#### default is sponsor = UNAVAILABLE in %s' % (configFile))
		if policy > 0:
			addOutput(host, 'sed -i -e "s@site_policy = UNAVAILABLE@site_policy = %s@" %s' % (policy,configFile))
		else:
			addOutput(host, '#attr OSG_CE_siteinfo_policy not defined for CE server')
			addOutput(host, '#### default is site_policy = UNAVAILABLE in %s' % (configFile))
		if contact > 0:
			addOutput(host, 'sed -i -e "s@contact = UNAVAILABLE@contact = %s@" %s' % (contact,configFile))
		else:
			addOutput(host, '#attr OSG_CE_siteinfo_contact not defined for CE server')
			addOutput(host, 'echo "attr OSG_CE_siteinfo_contact not defined for CE server"')
			addOutput(host, '#### default is contact = UNAVAILABLE in %s' % (configFile))
		if email > 0:
			addOutput(host, 'sed -i -e "s/email = UNAVAILABLE/email = %s/" %s' % (email,configFile))
		else:
			addOutput(host, '#attr OSG_CE_siteinfo_email not defined for CE server')
			addOutput(host, 'echo "attr OSG_CE_siteinfo_email not defined for CE server"')
			addOutput(host, '#### default is email = UNAVAILABLE in %s' % (configFile))
		if city > 0:
			addOutput(host, 'sed -i -e "s@city = UNAVAILABLE@city = %s@" %s' % (city,configFile))
		else:
			addOutput(host, '#attr OSG_CE_siteinfo_city not defined for CE server')
			addOutput(host, '#### USING attr "Info_CertificateLocality" as city in %s' % (configFile))
			city2      = self.db.getHostAttr(host,'Info_CertificateLocality')
			if city2 > 0:
				addOutput(host, 'sed -i -e "s@city = UNAVAILABLE@city = %s@" %s' % (city2,configFile))
			else:
				addOutput(host, '####### attr "Info_CertificateLocality" not defined!!!!!')

		if country > 0:
			addOutput(host, 'sed -i -e "s@country = UNAVAILABLE@country = %s@" %s' % (country,configFile))
		else:
			addOutput(host, '#attr OSG_CE_siteinfo_country not defined for CE server')
			addOutput(host, '#### USING attr "Info_CertificateCountry" as country in %s' % (configFile))
			country2      = self.db.getHostAttr(host,'Info_CertificateCountry')
			if country2 > 0:
				addOutput(host, 'sed -i -e "s@country = UNAVAILABLE@country = %s@" %s' % (country2,configFile))
			else:
				addOutput(host, '####### attr "Info_CertificateCountry" not defined!!!!')

		if longitude > 0:
			addOutput(host, 'sed -i -e "s@longitude = UNAVAILABLE@longitude = %s@" %s' % (longitude,configFile))
		else:
			addOutput(host, '#attr OSG_CE_siteinfo_longitude not defined for CE server')
			addOutput(host, '#### USING attr "Info_ClusterLatlong" to retrive longitude in %s' % (configFile))
			if longitude2 > 0:
				lon2 = longitude2.replace('E','')
				lon2 = lon2.replace('e','')
				lon2 = lon2.replace('w','-')
				lon2 = lon2.replace('W','-')
				addOutput(host, 'sed -i -e "s@longitude = UNAVAILABLE@longitude = %s@" %s' % (lon2,configFile))
			else:
				addOutput(host, '####### attr "Info_ClusterLatlong" not defined!!!!')
		if latitude > 0:
			addOutput(host, 'sed -i -e "s@latitude = UNAVAILABLE@latitude = %s@" %s' % (latitude,configFile))
		else:
			addOutput(host, '#attr OSG_CE_siteinfo_latitude not defined for CE server')
			addOutput(host, '#### USING attr "Info_ClusterLatlong" to retrive latitude in %s' % (configFile))
			if latitude2 > 0:
				lat2 = latitude2.replace('N','')
				lat2 = lat2.replace('n','')
				lat2 = lat2.replace('s','-')
				lat2 = lat2.replace('S','-')
				addOutput(host, 'sed -i -e "s@latitude = UNAVAILABLE@latitude = %s@" %s' % (lat2,configFile))
			else:
				addOutput(host, '####### attr "Info_ClusterLatlong" not well defined!!!!')

		addOutput(host, '#end config %s' % (configFile))
		addOutput(host, '')
