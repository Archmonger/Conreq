???+ Summary

    These instructions configure Non-Sucking Service Manager (NSSM) to automatically start Conreq as a Windows service.

    A traditional Windows installer is targeted for development within our roadmap, but is currently not available.

---

## Software Required

??? warning "Warning for Windows users"

    Steps below will not work with NSSM if using the "Windows App Store" version of Python.

{% include-markdown "../../includes/requirements.md" start="<!-- conreq -->" end="<!-- conreq-end -->" trailing-newlines=false %}

## Installation

1. Create the folder `C:\Program Files\Conreq`
2. Use this folder to follow steps [setting up a Conreq environment](/Conreq/develop/run_conreq/#creating-a-production-environment), excluding steps involving `python manage.py run_conreq`.
3. Unzip NSSM in a separate directory where you can permanently keep it (ex. `C:\Program Files\NSSM`).
4. Open a terminal (ex. Command Prompt or PowerShell) within your NSSM directory **as administrator**.
5. Open NSSM by typing `.\win64\nssm.exe install Conreq`
6. Under the Application tab, browse to the path of your **Conreq venv**.
    - ex) `C:\Program Files\Conreq\.venv\Scripts\python.exe`
7. Under the Application tab, browse to the path of your **Conreq repository**.
    - ex) `C:\Program Files\Conreq\`
8. Under the Application tab, set "Arguments" to `manage.py run_conreq`
9. Click "Install Service".
10. In your terminal, type `.\win64\nssm.exe start Conreq`.
    - You can check to make sure its running as a service by running `nssm status Conreq`
11. Open any internet browser and navigate to [http://127.0.0.1:8000/](http://127.0.0.1:8000/)
