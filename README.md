osg-roll
========

Download and Compile Roll
-------------------------

git https://github.com/jeramirez/osg-roll.git
cd osg-roll
#optional#cd src/osg
#optional#./downloadOSG.py http://repo.grid.iu.edu/osg/3.1/el5/release/x86_64
#optional#cd ../..
make

RHEL/SL/Centos 5: epel dependencies needed for OSG packages
-----------------------------------------------------------

bouncycastle
   glite-security-trustmanager
   glite-security-util-java
   vomsjapi
   emi-trustmanager-tomcat
   jglobus
   voms-admin-server
   voms-api-java

jakarta-commons-cli
   vomsjapi
   gums
   voms-api-java
python-ssl
   osg-pki-tools
mysql-connector-java
   gums
gsoap
   CGSI-gSOAP-devel
   CGSI-gSOAP-devel
   condor
   condor-cream-gahp
   dpm-copy-server-mysql
   dpm-copy-server-postgres
   dpm-srm-server-mysql
   dpm-srm-server-postgres
   gfal
   glite-ce-cream-cli
   glite-ce-cream-client-api-c
   glite-ce-cream-client-devel
   glite-data-delegation-api-c
   glite-fts-client
   lfc
   lfc-dli
   voms-server
   xacml
is-interface
perl-XML-DOM
jakarta-commons-io
iperf
   bwctl-client
   bwctl-server
fetch-crl3/fetch-crl
   cms-xrootd
   dcache-gratia-probe
   gratia-reporting-web
   gratia-service
   osg-gums
   osg-wn-client
   voms-admin-server
   osg-gridftp
   osg-gridftp-hdfs
   osg-gridftp-xrootd
   osg-se-bestman
   osg-se-bestman-xrootd

