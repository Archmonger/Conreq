from conreq import app


# Custom Functions
def css(path: str, attributes: dict = None, local=True) -> None:
    if local:
        app.config("local_stylesheets").append((path, attributes))
    else:
        app.config("remote_stylesheets").append((path, attributes))


def scss(path: str, attributes: list[tuple] = None):
    app.config("scss").append((path, attributes))


def javascript(path: str, attributes: list[tuple] = None, local=True) -> None:
    if local:
        app.config("local_scripts").append((path, attributes))
    else:
        app.config("remote_scripts").append((path, attributes))


def font(path: str, attributes: list[tuple] = None, local=True) -> None:
    if local:
        app.config("local_stylesheets").append((path, attributes))
    else:
        app.config("remote_stylesheets").append((path, attributes))


def head_content(template: str) -> None:
    app.config("head_content").append(template)
