1. Go to `Server Settings` within Conreq and enable `Organizr User Authentication`

2. Set up a `nginx` reverse proxy.

    _If you need help with this, join the [`organizr` Discord](https://discord.com/invite/TrNtY7N) and post in #groups._

3. In your Conreq block within `nginx`, add the following...

    ```nginx
    # Sets Conreq to be accessible by all Organizr users. Google "Organizr ServerAuth" for more details.
    auth_request /auth-4;

    # Allows Conreq to log in as an Organizr user
    auth_request_set $auth_user $upstream_http_x_organizr_user;
    proxy_set_header X-WEBAUTH-USER $auth_user;

    # Allows Conreq to know the email address of an Organizr user (optional)
    auth_request_set $auth_email $upstream_http_x_organizr_email;
    proxy_set_header X-WEBAUTH-EMAIL $auth_email;

    # Allows Conreq to automatically configure Organizr Admins and Co-Admins as Conreq staff members (optional)
    auth_request_set $auth_group $upstream_http_x_organizr_group;
    proxy_set_header X-WEBAUTH-GROUP $auth_group;
    ```
