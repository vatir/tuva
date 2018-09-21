"""
This is a multiprocessing testing applicaiton.

Primary Goal:
    Testing Process Comunication and synchronization.

"""

"""

Database information

Start db with:
..\bin\pgsql\bin\pg_ctl start -D DatabaseData -l DatabaseData\postgre.log

Port: 9489
Username: postgre

May need to periodicly delete: postgre.log

"""


"""
debug_level:
0 : Normal
1 : Enchanced Control
2 : Full Debugging
"""

debug_level = 2

"""
Setup General Process Control Functions
"""

import subprocess
class ProcessControl():
    """
    Creates an object that holds and controls another process.
    """
    
    def __init__(self, args):
        """
        args: Full command run string.
        """
        self.PObject = self.StartProcess(args)

    def StartProcess(self, args):
        new_PObject = subprocess.Popen(args, bufsize=-1, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return new_PObject
        
    def Comunicate(self, send = None):
        """
        Send input to process and return output.
        
        Popen.communicate(input=None)
        """
        return self.PObject.communicate(send)
    
    def GetProcessOutput(self):
        """
        Get Output
        """
        return self.PObject.communicate()
    
    def WaitProcess(self):
        """
        Waits until process has terminated and if it has terminated return the returncode.
        """
        return self.PObject.poll()
    
    def CheckProcess(self):
        """
        Check to see if the process object has terminated and return the returncode.
        """
        return self.PObject.poll()
    
    def KillProcess(self):
        """
        Terminate process
        """
        return self.PObject.terminate()

    def GetPID(self):
        """
        Return the process pid
        """
        return self.PObject.pid

class DB_Proc():
    """
    Setup DB process object.
    
    Use the StopDB method to close the DB using the postgre method.
    """
    def __init__(self):
        if not (self.CheckRunningDB()):
            self.PObject = self.StartDB()
        else:
            self.PObject = None
            if debug_level == 2:
                print "DB: Server Already Running" 
    
    def StartDB(self):
        """
        Start the DB instance.
        """
        if debug_level == 2:
            print "DB:Starting"

        db_pobject = ProcessControl("pg_ctl start -D DatabaseData -l DatabaseData\\postgre.log")

        return db_pobject
    
    def CheckRunningDB(self):
        """
        Check if the DB server is currently running. 
        
        If pg_ctl status returns a returncode of 0 then the postgre server is running.
        """
        if 0 == subprocess.call("pg_ctl status -D DatabaseData", bufsize=-1, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE):
            return True
        else:
            return False
        
    def StopDB(self):
        """
        Execute the postgre stop command to the database.
        """
        if self.CheckRunningDB() == False:
            if debug_level == 2:
                print "DB: Server does not exist."
            return False
      
        else:
            if debug_level == 2:
                print "DB: Stopping"
            """
            The next line sends a stop command to the postgre server.
            Note: -m options
                s: smart waits for clients to disconnect
                f: fast disconnects and rolls back any connected clients
                i: immediate disconnects all clients (no clean) and forces a recovery on restart
            """
            stopdb_pobject = ProcessControl("pg_ctl stop -m f -D DatabaseData")
            return stopdb_pobject.CheckProcess()

    def GetPID(self):
        """
        Returns the process pid. Note this is the pg_control pid that has probably already terminated.
        """
        return self.PObject.GetPID()


model_name = "simplebindinganalytic"

if __name__ == "__main__":
    """
    Add any additional system paths with the following command.
    """
    import wx

    app = wx.App(redirect=True)
    frame = wx.Frame(None, title="Core Process Manager (Debug)", size=(600,800))
    panel = wx.Panel(frame)
    if debug_level >= 1:
        frame.Show()
    
    filename = 'ISWI NCP Binding Double Label All 4 6 2012.dat'
    generated_runs=10
    
    db = DB_Proc()
    #print "init_gui Starting:"
    init_gui = ProcessControl(['pythonw.exe','init_gui.py'])
    DBSetup = ProcessControl([
                              'pythonw.exe',
                              'DatabaseSetup.py',
                              '-host=localhost',
                              '-port=9489',
                              '-db=MainData',
                              '-user=postgre',
                              '-file='+str(filename),
                              '-runs='+str(generated_runs)])
    
    #print init_gui.Comunicate()
    #print "Checking DB status:"
    #print db.CheckRunningDB()
    print "init_gui:"
    print str(init_gui.GetPID())
    print "DatabaseSetup:"
    print str(DBSetup.GetPID())
    print "Begin DBSetup Output:"
    print DBSetup.GetProcessOutput()[0]
    print "End DBSetup Output"
    """
    Inspection Widget this allows tracking of GUI objects within this wx instance.
    """
    
    if debug_level >= 2:
        import wx.lib.inspection
        wx.lib.inspection.InspectionTool().Show()

    app.MainLoop()
    
    #db.StopDB()
        