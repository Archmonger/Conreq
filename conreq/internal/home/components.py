import idom


@idom.component
def hello(websocket):
    return idom.html.h1("Hello World!")
