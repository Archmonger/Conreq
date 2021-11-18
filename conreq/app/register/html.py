import conreq


# Custom Functions
def css(reverse_path: str, attributes: dict = None, local=True) -> None:
    if local:
        conreq.config.local_stylesheets.append(
            {"path": reverse_path, "attributes": attributes}
        )
    else:
        conreq.config.remote_stylesheets.append(
            {"path": reverse_path, "attributes": attributes}
        )


def scss(reverse_path: str, attributes: list[tuple] = None):
    conreq.config.scss_stylesheets.append(
        {"path": reverse_path, "attributes": attributes}
    )


def javascript(reverse_path: str, attributes: list[tuple] = None, local=True) -> None:
    if local:
        conreq.config.local_scripts.append(
            {"path": reverse_path, "attributes": attributes}
        )
    else:
        conreq.config.remote_scripts.append(
            {"path": reverse_path, "attributes": attributes}
        )


def font(reverse_path: str, attributes: list[tuple] = None, local=True) -> None:
    if local:
        conreq.config.local_stylesheets.append(
            {"path": reverse_path, "attributes": attributes}
        )
    else:
        conreq.config.remote_stylesheets.append(
            {"path": reverse_path, "attributes": attributes}
        )


def head_content(template: str) -> None:
    conreq.config.head_content.append(template)
