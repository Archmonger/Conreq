These instructions use NSSM to automatically start Conreq. A Windows installater will eventually be developed, but is currently not available.

---

### Software Required

-   Install [Python 3.8+](https://www.microsoft.com/en-us/p/python-38/9mssztt1n39l#activetab=pivot:overviewtab) (Easiest if this is the only version of python on your computer)
-   Download [NSSM](https://nssm.cc/download)

### Installation

1. Create the folder `C:\Program Files\Conreq`
2. Use this folder to follow steps 1 to 6 of [setting up a Conreq environment](http://127.0.0.1:8000/Conreq/develop/run_conreq/#setting-up-the-environment).
3. Unzip NSSM in a separate directory where you can permanently keep it (ex. `C:\Program Files\NSSM`).
4. Open a terminal (ex. Command Prompt or PowerShell) within your NSSM directory.
5. Open NSSM by typing `.\win64\nssm.exe install Conreq`.
6. Under the Application tab, browse to the path of your **Conreq venv**.
    - ex) `C:\Program Files\Conreq\.venv\Scripts\python.exe` <!-- TODO: Change this to run_conreq.bat -->
7. Under the Application tab, browse to the path of your **Conreq repository**.
    - ex) `C:\Program Files\Conreq\`
8. Click "Install Service".
9. In your terminal, type `.\win64\nssm.exe start Conreq`.
    - You can check to make sure its running as a service by running `nssm status Conreq`
10. Open any internet browser and navigate to [http://127.0.0.1:8000/](http://127.0.0.1:8000/)
