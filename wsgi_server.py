from conreq.utils.generic import get_webserver
from conreq.wsgi import application

webserver = get_webserver()

if webserver == "bjoern":
    import bjoern

    bjoern.run(application, "0.0.0.0", 8000, reuse_port=True)

elif webserver == "wsgiserver":
    import wsgiserver

    server = wsgiserver.WSGIServer(application, host="0.0.0.0", port=8000)
    server.start()

else:
    print("No valid webserver specified through environment variable 'WEBSERVER'!")
    print("Defaulting to 'WSGI Server'")
    import wsgiserver

    server = wsgiserver.WSGIServer(application, host="0.0.0.0", port=8000)
    server.start()
