These instructions configure Non-Sucking Service Manager (NSSM) to automatically start Conreq as a Windows service.

A traditional Windows installer is not yet available.

---

## Software Required

-   Install [Python 3.11+](https://www.python.org/downloads/)
    -   Make sure to select "Add Python 3.x to PATH" during installation.
    -   Easiest if this is the only version of python on your computer
    -   Steps below will not work with NSSM if using the "Windows App Store" version of Python.
-   Install [Visual Studio C++](https://visualstudio.microsoft.com/visual-cpp-build-tools/) (Within this installer, navigate to _C++ Build Tools_. Select _MSVC_ and _Windows 10 SDK_)
-   Download [NSSM](https://nssm.cc/download)

## Installation

1. Create the folder `C:\Program Files\Conreq`
2. Use this folder to follow steps [setting up a Conreq environment](../develop/run_conreq.md#creating-a-production-environment), excluding steps involving `python manage.py run_conreq`.
3. Unzip NSSM in a separate directory where you can permanently keep it (such as `C:\Program Files\NSSM`).
4. Open a terminal within your NSSM directory **as administrator**.
5. Open NSSM by typing `.\win64\nssm.exe install Conreq`
6. Under the Application tab, browse to the path of your **Conreq `venv`**.
    - For example: `C:\Program Files\Conreq\.venv\Scripts\python.exe`
7. Under the Application tab, browse to the path of your **Conreq repository**.
    - For example: `C:\Program Files\Conreq\`
8. Under the Application tab, set "Arguments" to `manage.py run_conreq`
9. Click "Install Service".
10. In your terminal, type `.\win64\nssm.exe start Conreq`.
    - You can check to make sure its running as a service by running `nssm status Conreq`
11. Open any internet browser and navigate to [`http://127.0.0.1:7575/`](http://127.0.0.1:7575/)
