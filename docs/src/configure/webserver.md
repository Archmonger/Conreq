We use [`hypercorn`](https://github.com/pgjones/hypercorn/) as Conreq's production-grade webserver. This webserver can be directly exposed to the internet. For more information beyond what is in this guide, check out the [`hypercorn` documentation](https://pgjones.gitlab.io/hypercorn/).

---

The Conreq webserver can be modified through a `hypercorn.toml` file.

1.  Create a `hypercorn.toml` file within your Conreq data directory (such as `./conreq/data/hypercorn.toml`)

2.  Populate this `toml` file with any property in the [`hypercorn`'s documentation](https://pgjones.gitlab.io/hypercorn/how_to_guides/configuring.html#configuration-options). For example...

    ```toml
    bind = "0.0.0.0:5357"
    h11_max_incomplete_size = 4
    keep_alive_timeout = 20
    use_reloader = true
    workers = 20
    ```
