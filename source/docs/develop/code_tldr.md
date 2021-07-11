This guide is intended to help developers gain an understanding of how the code in Conreq works together to make a functional application.

---

## Repository Structure

`manage.py` - Django development tool _(runs the development web server, initialize the databases, [and more.](https://docs.djangoproject.com/en/3.1/ref/django-admin/)_<br/>
`misc/` - Branding, legal documents, and other miscellaneous files<br/>

`conreq/` - Main Django application<br/>
`conreq/settings.py` - Boot-time configuration and settings<br/>
`conreq/urls.py` - Main HTTP URL path handler<br/>
`conreq/asgi.py` - Main Websocket path handler<br/>
`conreq/core/websockets/consumers.py` - Back-end websocket commands _(sends/receives json)_<br/>
`conreq/static/js/client_websockets.js` - Front-end websocket commands _(sends/receives json)_<br/

`conreq/core/` - Core back-end functionality<br/>
`conreq/static-dev/` - CSS, JavaScript, and Image files<br/>
`conreq/templates/` - HTML templates used by sub-application's `views.py` to generate web pages<br/>
`conreq/utils/` - Generic functions that can be used by their respective category<br/>

---

## Fundamental Django Design

Almost all of the Conreq back-end "logic" will trace back to a `views.py` file. Within this file we import all sorts helper functions to help us render a specific URL address. Most of these helper functions are located within `conreq/utils/` and `conreq/core/`.

Here's a high level example of what occurs when the browser visits a URL.

1. The browser visits a Conreq web address
2. Django determines how to handle this URL by comparing the path (let's use the example of `/server_settings/`) with what is contained in `conreq/urls.py`
3. Based on `conreq/urls.py`, Django determines there is another file that defines this path, and that file is `conreq/core/server_settings/urls.py`.
4. Based on `conreq/core/server_settings/urls.py`, Django determines this URL is rendered by `conreq/core/server_settings/views.py`
5. Django renders the HTML (known as a `Django View`) by running the the respective view function contained within `conreq/core/server_settings/views.py`
6. The webserver determines how to send this view to the browser based on what was returned by the view (ex. a `HttpResponse` or `JsonResponse`)

---

## Conreq Viewport Rendering

Viewport rendering is currently being reassessed. These docs will be updated at a later time.

---

## Conreq Modal Rendering

Modal rendering is currently being reassessed. These docs will be updated at a later time.

---

## Django Websockets

Websockets exist alongside the normal HTTP requests (ex. viewport rendering). They can be thought of as communicating via _chat messages_. When the page first loads, a connection to a _private chat room (direct messages)_ is formed, and _chat bubbles_ (`json` messages) are communicated back and forth between the server and client browser.

On the server side, the URL location of where _private chat rooms_ are created is determined within `conreq/asgi.py`. In this file, the URL is directly linked to a `consumer`. Django does support creating _chat groups_ with multiple clients in it, however, Conreq currently does not utilize this feature.

At the most fundamental level, a `consumer` is a Python class with a _send_ and _receive_ function. All of Conreq's consumers can be found in `conreq/core/websockets/consumers.py`.

In Django, the receive and response format is most commonly JSON. This is determined based on your consumer's base class (ex. `JsonWebsocketConsumer`). These classes have built-in functions for sending and receiving JSON messages (ex. `send_json` and `recieve_json`). Overriding these functions will be where most of your Websocket logic will be written.

When a JSON message is sent from server to the client browser, it will be received by the JavaScript file `conreq/static/js/client_websockets.js` using ES6 standard JavaScript Websockets. This file is also the one that initiates a new Websocket communication session when the page first loads.
