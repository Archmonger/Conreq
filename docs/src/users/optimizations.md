Include security and performance changes that can be made

## Security

-   Configure Conreq to use SSL
-   Use system variables for secret keys
-   Limit allowed hosts to only include URLs Conreq will be served at (local URLs can also be safe)
-   Limit CSRF trusted origins
-   Ensure Debug Mode is turned off whenever exposing Conreq to the internet
-   Reduce max session age
-   Enable Rotate Secret Key
-   Configure email settings to receive security alerts

## Performance

-   Use Nginx with `X-Accel` (View reverse proxy docs)
-   Increase worker count
-   Reduce logging
-   Use a production database, such as MySQL
-   Use a high performance cache, such as Redis
