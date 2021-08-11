# Conreq Barebones Installation #

## Windows 10 ##

**Requirements**

- Latest Pip
- Python 3.8+ in Windows Path
- Git for Windows

### Installation ###

1. In Powershell or cmd navigatr to where you want the conreq to run. Then run `git pull https://github.com/Archmonger/Conreq.git`
2. Go inside the sub directory by running `cd conreq` 
3. Run `git checkout develop` inside the conreq folder. This will switch the branch to the develop so we can run outside the docker branch until a Windows 10 Exe is made.
4. Now we need to make a venv in our conreq Install directory by `python -m venv venv`
5. Now we need to run and activate the venv directory.
`./venv/Scripts/activate`
6. Run `pip install -r requirements.txt` to install dependencies needed to run Conreq
7. Finally run `\/venv/Scripts/python.exe manage.py run_conreq -p 7575` to start Conreq in terminal.

## Auto Run Conreq at Startup ##

## Windows 10 ##

### NSSM Auto Start Conreq ###

**OBVIOUSLY HAVE NSSM INSTALLED IN YOUR WINDOWS ENV PATH**

1. Load up a Powershell as Administator
2. Run `nssm install Conreq` to load up the GUI for the Conreq NSSM setup
3. On the first page you will see the Application tab. Type in the path to your Conreq venv Install.
 `C:/(Your Pythonx.x Directory)/venv/Scripts/python.exe`
IE. `C:\Tools\Conreq\venv\Scripts\python.exe`
4. Set the Startup Folder to your Conreq Directory
IE. `C:\Tools\Conreq\`
5. Run the argument/command manager.py run_conreq -p 7575 (You can use any port of your choosing)
6. Go to the tab Log on and type in the fields for This Account `(Administrative User)`
Type in Password for that Administrative User

**IMPORTANT**
**The reason I do this is I have my storage running off another computer. I do this because I have a network drive attached to my Windows Install. If you have all your files inside the computer you Currently are running NSSM then you can just keep these settings the same for running as a local System Account**

It Should Look Like this in once you add all the relivant info.

**Application Tab**

![image](https://i.imgur.com/CE5piYo.png)

**Log on Tab**

![image](https://i.imgur.com/ht9eQuD.png)

7. Click save/edit Service.
8. Go back to your Powershell and run `nssm start Conreq` You should see start Succesful `Conreq: START: The operation completed successfully.
`
You could also check in Service.msc

9. Check to make sure its running as a service by running `nssm status Conreq`
You should recieve a response. `SERVICE_RUNNING`
10. Load up your preferred Browser CTRL+F5 or CTRL+R and see Enjoy your Conreq App.
