osg-roll
========

Download and Compile Roll
-------------------------

```shell
git clone https://github.com/jeramirez/osg-roll.git
cd osg-roll
cd src/osg
./downloadOSG.py http://repo.opensciencegrid.org/osg/3.5/el7/release/x86_64
./downloadOSG.py http://repo.opensciencegrid.org/osg/3.5/el7/contrib/x86_64
cd ../..
make roll
```

RHEL/SL/Centos 7: epel dependencies needed for OSG packages
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
   voms-api-java
python-ssl
   osg-pki-tools
mysql-connector-java
gsoap
   CGSI-gSOAP-devel
   CGSI-gSOAP-devel
   condor
   condor-cream-gahp
   voms-server
   xacml
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
   osg-wn-client
   voms-admin-server
   osg-gridftp
   osg-gridftp-hdfs
   osg-gridftp-xrootd
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
gfal
dcap-libs
dpm-libs
lcgdm-libs
lfc-libs
libmacaroons
log4cpp
mosh
davix
davix-libs
python36-chardet
python36-idna
python36-pysocks
python36-requests
python36-six
python36-urllib3
scitokens-cpp
apptainer
  fakeroot
  fakeroot-libs
  fuse2fs
  libzstd
  squashfuse
  squashfuse-libs
```

