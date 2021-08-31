import idom


@idom.component
def hello():
    return idom.html.h1("Hello World!")
