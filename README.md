osg-roll
========

Download and Compile Roll
-------------------------

```shell
git clone -b 3.3.x https://github.com/jeramirez/osg-roll.git
cd osg-roll
cd src/osg
./downloadOSG.py http://repo.grid.iu.edu/osg/3.3/el6/release/x86_64
cd ../..
make roll
```

RHEL/SL/Centos 6: epel dependencies needed for OSG packages
-----------------------------------------------------------

List of epel packages needed by OSG packages (in tab) shipped with this roll:

```shel
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
fetch-crl/fetch-crl3
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
gridsite-libs
   glite-data-util-c
   glite-fts-client
gfal2
   osg-wn-client
gfal2-core
   gfal2-plugin-xrootd-0.3
gfal2-plugin-gridftp
   osg-wn-client
gfal2-plugin-srm
   osg-wn-client
gfal2-transfer
   gfal2-plugin-xrootd-0.3
gfal2-util
   osg-wn-client
python-argparse
   gfal2-util
   osg-wn-client
canl-c
   gridsite-libs
pugixml
   gfal2-plugin-srm
```
