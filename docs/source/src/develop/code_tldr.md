This guide is intended to help developers gain an understanding of how Conreq was developed.

---

## Repository File Structure

| Path                                    | Description                                                                                                                                                |
| --------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `manage.py`                             | Django development tool _(runs the development web server, initialize the databases, [and more.](https://docs.djangoproject.com/en/3.1/ref/django-admin/)_ |
| `misc/`                                 | Branding, legal documents, and other miscellaneous files                                                                                                   |
| `conreq/`                               | Main Django application                                                                                                                                    |
| `conreq/core/`                          | All back-end functionality                                                                                                                                 |
| `conreq/static/`                        | CSS, JavaScript, and Image files                                                                                                                           |
| `conreq/utils/`                         | Generic functions that may be helpful to use                                                                                                               |
| `conreq/settings.py`                    | Boot-time configuration and settings                                                                                                                       |
| `conreq/urls.py`                        | HTTP URLs                                                                                                                                                  |
| `conreq/asgi.py`                        | Websocket URLs                                                                                                                                             |
| `conreq/core/websockets/consumers.py`   | Back-end Websockets                                                                                                                                        |
| `conreq/static/js/client_websockets.js` | Front-end websockets                                                                                                                                       |

---

## Viewport Rendering

Viewport rendering is currently being reassessed. These docs will be updated at a later time.

---

## Modal Rendering

Modal rendering is currently being reassessed. These docs will be updated at a later time.

---

## HTTP URL Routing

All of the HTTP routing logic will trace back to a `views.py` file. Within this file we write code render a specific URL address, which is effectively a string containing HTML.

Conreq relies on the [Django Framework](https://www.djangoproject.com/) for HTTP URL routing. Here's a high level example of what occurs when the browser visits a URL.

1. The browser visits a Conreq web address
2. Django determines how to handle this URL by comparing the path (let's use the example of `/server_settings/`) with what is contained in `conreq/urls.py`
3. Django looks at `conreq/urls.py` at notices it points to `include("conreq.core.server_settings.urls")`. So, this tells Django there is another file that defines this path, and that file is `conreq/core/server_settings/urls.py`.
4. Based on the `urlpatterns` in `conreq/core/server_settings/urls.py`, Django determines this URL is rendered by a function called `views.server_settings`.
5. Django runs this function to renders the HTML (known as a `Django View`).
6. The webserver determines how to send this view to the browser based on what was returned by the view (ex. a `HttpResponse` or `JsonResponse`)

---

## Websockets

Websockets can be thought of as the server and browser communicating via _chat messages_. When the page first loads, a connection to a _chat room_ is formed, and _chat bubbles_ can be communicated back and forth between the server and browser.

Chat rooms must exist at a specific URL. The URL they exist at is determined within `conreq/asgi.py`. In this file, a specific URL is directly linked to a [_websocket consumer_](https://channels.readthedocs.io/en/latest/topics/consumers.html).

A websocket consumer is a Python class with a send/receive function, which typically process `json` data.

The data format that gets processed is determined based on your consumer's base class. For example `AsyncJsonWebsocketConsumer` has `send_json()` and `recieve_json()` functions for processing JSON messages. Overriding these functions will be where most of your code will be written when working with websockets.

In the situation where the server sends a JSON message via `send_json()`, it will be processed by the browser's JavaScript websocket client _(ex. `conreq/static/js/client_websockets.js`)_.
