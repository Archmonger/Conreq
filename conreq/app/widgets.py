from django.forms.widgets import URLInput


class URLOrRelativeURLInput(URLInput):
    input_type = "text"
