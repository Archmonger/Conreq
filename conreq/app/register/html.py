from conreq import config


# Custom Functions
def css(reverse_path: str, attributes: dict = None, local=True) -> None:
    if local:
        config.homepage.local_stylesheets.append(
            {"path": reverse_path, "attributes": attributes}
        )
    else:
        config.homepage.remote_stylesheets.append(
            {"path": reverse_path, "attributes": attributes}
        )


def scss(reverse_path: str, attributes: list[tuple] = None):
    config.homepage.scss_stylesheets.append(
        {"path": reverse_path, "attributes": attributes}
    )


def javascript(reverse_path: str, attributes: list[tuple] = None, local=True) -> None:
    if local:
        config.homepage.local_scripts.append(
            {"path": reverse_path, "attributes": attributes}
        )
    else:
        config.homepage.remote_scripts.append(
            {"path": reverse_path, "attributes": attributes}
        )


def font(reverse_path: str, attributes: list[tuple] = None, local=True) -> None:
    if local:
        config.homepage.local_stylesheets.append(
            {"path": reverse_path, "attributes": attributes}
        )
    else:
        config.homepage.remote_stylesheets.append(
            {"path": reverse_path, "attributes": attributes}
        )


def head_content(template: str) -> None:
    config.homepage.head_content.append(template)
