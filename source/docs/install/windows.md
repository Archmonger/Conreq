These instructions use NSSM to automatically start Conreq. A Windows installer will eventually be developed, but is currently not available.

---

### Software Required

-   Install [Python 3.9+](https://www.python.org/downloads/)
    - Make sure to select "Add Python to path" 
    - Easiest if this is the only version of python on your computer
    - You will experience issues if using the "Windows App Store" version of Python. Make sure to install it the traditional way.
-   Download [NSSM](https://nssm.cc/download)

### Installation

1. Create the folder `C:\Program Files\Conreq`
2. Use this folder to follow steps 1 to 6 of [setting up a Conreq environment](http://127.0.0.1:8000/Conreq/develop/run_conreq/#setting-up-the-environment).
3. Unzip NSSM in a separate directory where you can permanently keep it (ex. `C:\Program Files\NSSM`).
4. Open a terminal (ex. Command Prompt or PowerShell) within your NSSM directory **as administrator**.
5. Open NSSM by typing `.\win64\nssm.exe install Conreq`.
6. Under the Application tab, browse to the path of your **Conreq venv**.
    - ex) `C:\Program Files\Conreq\.venv\Scripts\python.exe`
7. Under the Application tab, browse to the path of your **Conreq repository**.
    - ex) `C:\Program Files\Conreq\`
8. Click "Install Service".
9. In your terminal, type `.\win64\nssm.exe start Conreq`.
    - You can check to make sure its running as a service by running `nssm status Conreq`
10. Open any internet browser and navigate to [http://127.0.0.1:8000/](http://127.0.0.1:8000/)
