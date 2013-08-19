package plugin;
import java.io.*;
import java.util.*;

public class MountPoint implements gov.lbl.srm.policy.ISRMSelectionPolicy {
   String log_filename="/var/log/bestman2/servers.log";
//   String server_filename="/opt/bestman2/lib/plugin/servers.txt";
   String server_filename=null;
   java.io.File _file = null;
   String defaultServer="cms-grid0.hep.uprm.edu:2811";
   String currentString="";
   String[] ListOfServers = null;
   String[] ListOfPaths =null;
   Vector<Integer> ListOfRepeat = new Vector<Integer>();
   int TotalServers = 0;   
   public MountPoint (String filename) {
      try {
        _file = new java.io.File(filename);
        if (!_file.exists()) {
          throw new RuntimeException("File does not exist! name="+filename);
        }

        server_filename=filename;
        java.io.BufferedReader server_list = new java.io.BufferedReader(new java.io.FileReader(_file.getCanonicalPath()));
        Vector<String> tmpserver = new Vector<String>();//tmp of servers
        Vector<String> tmpmount  = new Vector<String>();//tmp of mountpoints
        while (server_list.ready()) {
           String currLine = server_list.readLine();
           if ((currLine == null) || (currLine.length() == 0)) {
              continue; //skip 
           }
           String[] line_in_list=currLine.split("=");
           
           tmpserver.addElement(line_in_list[1]);
           tmpmount.addElement(line_in_list[0]);
        }//end while read file
        TotalServers = tmpserver.size();
        appendFile("Total number of servers is "+ TotalServers );
        if (TotalServers <= 0){ 
           throw new RuntimeException("NO server found! Total Servers="+TotalServers);
        }
        ListOfServers = new String[TotalServers]; //Set Dimension of String[]
        ListOfPaths   = new String[TotalServers];
        for (int i=0;i<TotalServers;i++){ 
           ListOfServers[i] = tmpserver.elementAt(i);
           ListOfPaths[i]   = tmpmount.elementAt(i);
           appendFile("Server  "+ ListOfServers[i]+" in path ("+ListOfPaths[i]+")" );
           int firstrepeatedat = i;
           String testmnt=ListOfPaths[i];
           for (int j=0; j<i; j++) {
             if ( testmnt.contains(ListOfPaths[j]) ){
                firstrepeatedat = j;
                break;
             }//endif
           }//end for 
           ListOfRepeat.addElement(new Integer(firstrepeatedat));
        }//endfor fill up list

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
       String server="";
       try {
              //this can be fixed to take into account common mountpoints
              //for now take the first one
              for (int iserver=0; iserver<TotalServers; iserver++) {
                 if (currentString.contains(ListOfPaths[iserver]))
                 {
                   server=ListOfServers[iserver];
                   break;
                 }
              }
       }
       catch (Exception e)
	{
                System.err.println ("Error reading server file:"
			+server_filename);

	}
       if (server.equals(""))
	{
		server=defaultServer;
	}
       appendFile("Picked server ("+server+") from file for writing");
       return server;
   }
   public Object getNext(Object a) {
       appendFile("In the parent class for file: "+a);
	currentString=(String)a;
	return getNext();
   }
   public String[] displayContents() {
	String as[]={"cms-grid0.hep.uprm.edu:2811","cms-se.hep.uprm.edu:2811"};
       appendFile("In Display Contents");
	return as;
   }
   public void setItems(Object[] col) {
       appendFile("In set Items");
   }
}

