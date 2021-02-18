1. Set your `X_FRAME_OPTIONS` variable to false. If using Unraid/Docker, add this as a Docker Variable. If you are self hosting Conreq on your own operating system, consider searching searching "How to set environment variables in _... Windows 10_"

2. Go to `Server Settings` within Conreq and enable `Organizr User Authentication`

3. Set up a Nginx reverse proxy. _If you need help with this, join the [Organizr Discord](https://discord.com/invite/TrNtY7N)._ After setting one up, in your Conreq block you'll need to add the following:

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
