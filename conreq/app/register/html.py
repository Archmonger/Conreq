from conreq import app


# Custom Functions
def css(path: str, attributes: dict = None, local=True) -> None:
    if local:
        app.config.local_stylesheets.append({"path": path, "attributes": attributes})
    else:
        app.config.remote_stylesheets.append({"path": path, "attributes": attributes})


def scss(path: str, attributes: list[tuple] = None):
    app.config.scss_stylesheets.append({"path": path, "attributes": attributes})


def javascript(path: str, attributes: list[tuple] = None, local=True) -> None:
    if local:
        app.config.local_scripts.append({"path": path, "attributes": attributes})
    else:
        app.config.remote_scripts.append({"path": path, "attributes": attributes})


def font(path: str, attributes: list[tuple] = None, local=True) -> None:
    if local:
        app.config.local_stylesheets.append({"path": path, "attributes": attributes})
    else:
        app.config.remote_stylesheets.append({"path": path, "attributes": attributes})


def head_content(template: str) -> None:
    app.config.head_content.append(template)
