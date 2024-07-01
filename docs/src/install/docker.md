These instructions configure Conreq to run within a Docker.

Our dockers are published to both [DockerHub](https://hub.docker.com/r/archmonger/conreq/tags) and [GitHub Container Registry](https://github.com/Archmonger/Conreq/pkgs/container/conreq).

---

## Docker Compose

1.  Create a `docker-compose.yml` file is located where you want Conreq to run.

    === "`docker-compose.yml`"

        ```yaml
        services:
            conreq:
                image: ghcr.io/archmonger/conreq:latest # Other tags include `develop` and version numbers (e.g. `0.21.1`)
                container_name: conreq
                environment:
                    - PUID=99 # Optional
                    - PGID=100 # Optional
                    - TZ=America/Los_Angeles # If not set, defaults to UTC
                    # Any other Conreq environment variables can also be set here
                volumes:
                    - ./config:/config # You can replace ./config with the location you want to store Conreq's data.
                ports:
                    - 7575:7575
        ```

2.  Run `docker-compose up -d` to start Conreq. The `-d` flag runs the container in the background.

## Docker Run

1.  Run the following command to start Conreq.

    ```bash
    docker run -d --name=conreq -e PUID=99 -e PGID=100 -e TZ=America/Los_Angeles -v ./config:/config -p 7575:7575 ghcr.io/archmonger/conreq:latest
    ```

    _Note: You can replace `./config` with the location you want to store Conreq's data._

    _Note 2: The `-d` flag runs the container in the background._
