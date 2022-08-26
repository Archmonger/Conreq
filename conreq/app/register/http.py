from django.urls import path, re_path

# TODO: Implement WSGI middleware register function, probably not here though
# TODO: Have app API for conreq._core.api.permissions.HasAPIKey
# pylint: disable=import-outside-toplevel


def url(
    url_pattern: str,
    name: str | None = None,
    use_regex: bool = False,
):
    """Decorates a Django view function or view class."""

    def decorator(view):
        from conreq.urls import conreq_urls

        _register_view(view, url_pattern, conreq_urls, name, use_regex)

        return view

    return decorator


def api(
    url_pattern: str,
    version: int = 1,
    name: str | None = None,
    use_regex: bool = False,
):
    """Decorates a DRF view function or view class."""

    def decorator(view):
        from conreq.urls import api_urls

        _register_view(view, f"v{version}/{url_pattern}", api_urls, name, use_regex)

        return view

    return decorator


def _register_view(view, url_pattern, url_patterns, name, use_regex):
    registered_view = view.as_view() if hasattr(view, "as_view") else view
    dotted_path = f"{view.__module__}.{view.__name__}".replace("<", "").replace(">", "")

    if use_regex:
        url_patterns.append(
            re_path(url_pattern, registered_view, name=name or dotted_path)
        )
    else:
        url_patterns.append(
            path(url_pattern, registered_view, name=name or dotted_path)
        )
