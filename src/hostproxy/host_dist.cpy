#!/usr/bin/python

import sys,os
import subprocess
import threading
import time
import signal

# execute command and return (exit_code, message)
def copy_one(copy_one_cmd,
             tmpdir,sshbin,
             x509proxy,remotex509proxy,
             x509proxykey,remotex509proxykey,
             node,
             timeout):
    cmd=(copy_one_cmd,
         tmpdir,sshbin,node,
         x509proxy,remotex509proxy,
         x509proxykey,remotex509proxykey)
    
    print "Updating %s"%node 
    cmd_el = subprocess.Popen(cmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, close_fds=True)

    start_time=time.time()
    exit_code=cmd_el.poll()

    while (exit_code==None):
        running_time=time.time()-start_time
        if running_time>timeout:
            print "Node %s: Timeout reached, killing"%node
            os.kill(cmd_el.pid,signal.SIGTERM)
            time.sleep(1)
            exit_code=cmd_el.poll()
            if exit_code==None:
                os.kill(cmd_el.pid,signal.SIGKILL)
                exit_code=1
        else:
            time.sleep(1)
            exit_code=cmd_el.poll()

    (stdout,stderr)=cmd_el.communicate()

    if exit_code==0:
        print stdout
        #return (0,stdout)
    else:
        print stderr
        #return (exit_code,stderr)

def check_threads(thread_dict,timeout):
    # find a terminated thread
    for tid in thread_dict.keys():
        if not tid.isAlive():
            tid.join()
            del thread_dict[tid]

    # for all the remaining ones, check if they are withing timeout
    now=time.time()
    for tid in thread_dict.keys():
        runtime=now-thread_dict[tid]
        if runtime>timeout:
            del thread_dict[tid]
            print "Thread removed"
    #print "%i threads left" %len(thread_dict)

copy_one_cmd=sys.argv[0]+".one"
tmpdir=sys.argv[1]
sshbin=sys.argv[2]
x509proxy=sys.argv[3]
remotex509proxy=sys.argv[4]
x509proxykey=sys.argv[5]
remotex509proxykey=sys.argv[6]

max_threads=int(sys.argv[7])
thread_timeout=int(sys.argv[8]) # in seconds

nodes=sys.argv[9:]

thread_dict={}

for node in nodes:
    #print "Loop %s"%node
    # make sure there is space in the thread_queue
    while len(thread_dict)>=max_threads:
        check_threads(thread_dict,thread_timeout+10)
        time.sleep(1)
    #print "Creating thread"
    # the is space in the thread queue
    tid = threading.Thread(target=copy_one, args=(copy_one_cmd,tmpdir,sshbin,
                                                  x509proxy,remotex509proxy,
                                                  x509proxykey,remotex509proxykey,
                                                  node,thread_timeout))
    tid.setDaemon(1)
    tid.start()
    #print "Started thread %s"%tid
    thread_dict[tid]=time.time()

# wait for all threads to finish
while len(thread_dict)>0:
    check_threads(thread_dict,thread_timeout+10)
    time.sleep(1)
