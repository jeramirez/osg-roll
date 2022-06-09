ROLL			= osg
VERSION			= 3.6.220511
NAME    		= roll-$(ROLL)-usersguide
RELEASE			= 0
MANUALRELEASE 		= v9_0

SUMMARY_COMPATIBLE	= $(VERSION)
SUMMARY_MAINTAINER	= Rocks Group
SUMMARY_ARCHITECTURE	= i386, x86_64

ROLL_REQUIRES		= base kernel os ganglia
ROLL_CONFLICTS		= condor java

RPM.ARCH = noarch
RPM.FILES = /var/www/html/roll-documentation/$(ROLL)/$(VERSION)
