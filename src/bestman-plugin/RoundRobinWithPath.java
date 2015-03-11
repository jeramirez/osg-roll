package plugin;
import java.io.*;
import java.util.*;

public class RoundRobinWithPath implements gov.lbl.srm.policy.ISRMSelectionPolicy {
   String log_filename="/var/log/bestman2/servers.log";
   HashMap<String,Vector<String>> PathMap  = new HashMap<String,Vector<String>>(); //map of path to servers
   HashMap<String,Integer> CountMap = new HashMap<String,Integer>();               //map of path to count servers
   Vector<String> ListOfPaths = new Vector<String>();                              //list of path used
   long _lastChecked = -1;                                                         //tmp var used to refresh input file
   java.io.File _file = null;

   public RoundRobinWithPath (String filename) {
        _file = new java.io.File(filename);
        if (!_file.exists()) {
          throw new RuntimeException("File does not exist! name="+filename);
        }

//        loadFile();
        doRefresh();
   }

   //  read from file and verify that entries are valid protocols
   private void loadFile() {
      try {
        java.io.BufferedReader server_list = new java.io.BufferedReader(new java.io.FileReader(_file.getCanonicalPath()));

        PathMap  = new HashMap<String,Vector<String>>();// clean path for reloading 
        while (server_list.ready()) {
           String currLine = server_list.readLine();
           if ((currLine == null) || (currLine.length() == 0) || (currLine.charAt(0) == '#') ) {
              continue; //skip 
           }
           //now split protocol HostPort to fill vectors like in TSRMTxfProtocol.checkProtocolWithCollection
           String token="://";
	   int pos              = currLine.indexOf(token);
	   if (pos <= 0) {
	      System.out.println("RoundRobinWithPath plugin: token missing:"+currLine+" check your format in:"+_file);
	      appendFile("RoundRobinWithPath plugin: token missing:"+currLine+" check your format in:"+_file);
	      throw new RuntimeException("Can not recognize this value: "+currLine+", token not found, check your format in "+_file);
	   }
	   String protocol      = currLine.substring(0, pos);
	   String hostPortMount = currLine.substring(pos+3);
	   //strip off mount point
	   int posFirstSlash    = hostPortMount.indexOf("/");
	   String hostPort      = hostPortMount.substring(0, posFirstSlash);
	   String mountpath     = hostPortMount.substring(hostPort.length()+1);
	   while (mountpath.endsWith("/")) {
	     mountpath = mountpath.substring(0, mountpath.length()-1);
	   }
	   mountpath = "/"+ mountpath;
           //Save info in maps
           if (!PathMap.containsKey(mountpath)) {
              Vector<String> v = new Vector<String>();
              v.add(hostPort);
              PathMap.put(mountpath, v);
           } else {
              Vector<String> v = PathMap.get(mountpath);
              if (!v.contains(hostPort)) {
                 v.add(hostPort);
		 PathMap.put(mountpath, v);//this should replace (update) value
              }
           }
           //one time only inittialization
           if (!CountMap.containsKey(mountpath)){
               CountMap.put(mountpath,new Integer(-1));
               ListOfPaths.addElement(mountpath);
           }
           appendFile("RoundRobinWithPath plugin: Server  "+hostPort+"  in mount path ("+mountpath+")");

        }//end while read file

//      At this point should work for any protocol
	appendFile("RoundRobinWithPath plugin: size vector ListOfPaths:"+ListOfPaths.size());

//      Reset count for each Path that need it (refresh changes or new input paths) and get a totallist of servers
	Vector<String> TotalListOfServers = new Vector<String>();
	for (int i=0; i<ListOfPaths.size(); i++) {
	   int icount = CountMap.get( ListOfPaths.elementAt(i) );
	   if (icount < 0 ){
	      CountMap.put(ListOfPaths.elementAt(i),new Integer(0));
	   }//endif
	   //Fill total list of servers (assume just one type of protocol per input file)
	   Vector<String> ListOfServers = PathMap.get(ListOfPaths.elementAt(i));
	   for (int j=0;j<ListOfServers.size();j++){
	      TotalListOfServers.addElement(ListOfServers.elementAt(j));
	   }//end for
	}//end for

      }catch (java.io.IOException e) {
            e.printStackTrace();
            throw new RuntimeException(e.getMessage());
      }finally {}

   }
   public void appendFile(String s) {
          FileOutputStream out; // declare a file output object
          PrintStream p; // declare a print stream object
          try
          {
                  // Create a new file output stream
                  out = new FileOutputStream(log_filename,true);
                  // Connect print stream to the output stream
                  p = new PrintStream( out );
                  p.println ((new java.util.Date()).getTime()+": "+s);
                  p.close();
          }
          catch (Exception e)
          {
                  System.err.println ("Error writing to test log file:"
			+log_filename);
          }
   }
   public Object getNext() {
       String pathselected=ListOfPaths.elementAt(0);
	Object result = null;
        int icount = CountMap.get( pathselected );
        Vector<String> ListOfServers = PathMap.get(pathselected);
        if (( icount >=0 ) && (ListOfServers.size()>0) ){
            if (icount >= ListOfServers.size() ){
               icount = ListOfServers.size() - 1;
            }
            result = ListOfServers.elementAt(icount);
            icount = icount + 1;
            icount = icount % (ListOfServers.size());
            CountMap.put(pathselected,icount);
        }
	appendFile("RoundRobinWithPath plugin: Picked default server? ("+result+") for file transfer");
        appendFile("RoundRobinWithPath plugin: wrong turn ... never should come here ... bug?");
	return result;
   }
   public Object getNext(Object localfile) {
        String path=(String)localfile; 
	appendFile("RoundRobinWithPath plugin: tranfering into localfile: "+localfile);
	doRefresh();
	Object result = null;

        String pathselected = new String();
        for (int i=0;i<ListOfPaths.size(); i++) {
            if (path.contains(ListOfPaths.elementAt(i)))
            {
               pathselected=ListOfPaths.elementAt(i);
               break;
            }
        }//loop of paths
	//choose default path if empty (first in list)
	if ((pathselected == null) || (pathselected.length() == 0)) {
	       pathselected=ListOfPaths.elementAt(0);
	}
        int icount = CountMap.get( pathselected );
        Vector<String> ListOfServers = PathMap.get(pathselected);
        if (( icount >=0 ) && (ListOfServers.size()>0) ){
            if (icount >= ListOfServers.size() ){
               icount = ListOfServers.size() - 1;
            }
            result = ListOfServers.elementAt(icount);
            icount = icount + 1;
            icount = icount % (ListOfServers.size());
            CountMap.put(pathselected,icount);
        }
	appendFile("RoundRobinWithPath plugin: Picked server ("+result+") for file transfer");
	return result;

   }
   public String[] displayContents() {
	String as[]=null;
       appendFile("In Display Contents");
        Vector<String> TotalListOfServers = new Vector<String>();
        for (int i=0; i<ListOfPaths.size(); i++) {
           //Fill total list of servers (assume just one type of protocol per input file)
           Vector<String> ListOfServers = PathMap.get(ListOfPaths.elementAt(i));
           for (int j=0;j<ListOfServers.size();j++){
              TotalListOfServers.addElement(ListOfServers.elementAt(j));
           }//end for
        }//end for
        as = new String[TotalListOfServers.size()];
	for (int i=0; i<TotalListOfServers.size(); i++) {
	  as[i] = TotalListOfServers.elementAt(i);
	}
	return as;
   }
   public void setItems(Object[] col) {
       //useful to reset variables before going to next file
       //not needed here
       appendFile("In set Items");
   }

   private void doRefresh() {
       if (_file == null) {
	  return;
       }
       long lastModified = _file.lastModified();
       if (lastModified <= 0) {
	 return;
       }
       if (lastModified < _lastChecked) {
	return;
       }
       _lastChecked = lastModified;
       loadFile();
   }
}

