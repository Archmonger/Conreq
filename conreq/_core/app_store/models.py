import importlib
import platform
import uuid

from django.contrib.auth import get_user_model
from django.db import models
from multiselectfield import MultiSelectField
from ordered_model.fields import OrderedManyToManyField
from ordered_model.models import OrderedModel
from packaging import version
from versionfield import VersionField

from conreq._core.fields import AutoOneToOneField, PythonTextField
from conreq.utils.environment import get_env
from conreq.utils.models import UUIDFilePath


class DevelopmentStage(models.TextChoices):
    PLANNING = "1 - Planning", "Planning"
    PREALPHA = "2 - Pre-Alpha", "Pre-Alpha"
    ALPHA = "3 - Alpha", "Alpha"
    BETA = "4 - Beta", "Beta"
    STABLE = "5 - Production/Stable", "Stable"
    MATURE = "6 - Mature", "Mature"
    INACTIVE = "7 - Inactive", "Inactive"


class AsyncCompatibility(models.TextChoices):
    NONE = "No Async", "No Async"
    SEMI = "Semi Async", "Semi Async"
    FULL = "Fully Async", "Fully Async"


class SysPlatform(models.TextChoices):
    ANY = "Any", "Any"
    LINUX = "Linux", "Linux"
    WINDOWS = "Windows", "Windows"
    MACOS = "Darwin", "MacOS"
    FREEBSD = "FreeBSD", "FreeBSD"


class DescriptionType(models.TextChoices):
    TXT = "text/plain", "Plain Text (.txt)"
    RST = "text/x-rst", "reStructuredText (.rst)"
    MD = "text/markdown", "Markdown (.md)"


class Category(OrderedModel):
    def __str__(self):
        return str(self.name)

    class Meta:
        verbose_name_plural = "Categories"
        ordering = ["order"]

    uuid = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False, unique=True
    )

    # Basic Info
    name = models.CharField(max_length=50, unique=True)


class Subcategory(models.Model):
    def __str__(self):
        return str(self.name)

    class Meta:
        verbose_name = "Subcategory"
        verbose_name_plural = "Subcategories"
        unique_together = ["name", "category"]

    uuid = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False, unique=True
    )

    # Basic Info
    name = models.CharField(max_length=50)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)


class PyPiData(models.Model):
    author = models.CharField(blank=True, max_length=50)
    author_email = models.EmailField(blank=True)
    development_status = models.CharField(
        blank=True,
        max_length=21,
        choices=DevelopmentStage.choices,
        default=DevelopmentStage.PLANNING,
    )
    description = models.TextField(blank=True)
    description_content_type = models.CharField(
        blank=True,
        max_length=20,
        choices=DescriptionType.choices,
        default=DescriptionType.TXT,
    )
    keywords = models.TextField(blank=True)
    license = models.CharField(blank=True, max_length=100)
    maintainer = models.CharField(blank=True, max_length=50)
    maintainer_email = models.EmailField(blank=True)
    package_url = models.URLField(blank=True)
    requires_python = models.CharField(blank=True, max_length=50)
    summary = models.CharField(blank=True, max_length=255)
    version = VersionField(blank=True)
    releases = models.JSONField(blank=True)

    # State tracking
    loaded = models.BooleanField(default=False)
    modified_at = models.DateTimeField(auto_now=True, editable=False)

    def load(self):
        """Loads the PyPiData from PyPi."""
        if not self.app_packge.developed or not self.app_package.listed_on_pypi:
            return

        # pylint: disable=import-outside-toplevel
        import requests

        # Get PyPi data
        response = requests.get(
            f"https://pypi.org/pypi/{self.app_package.pypi_name or self.app_package.pkg_name}/json"
        )
        data = response.json()

        # Update fields
        self.author = data["info"]["author"]
        self.author_email = data["info"]["author_email"]
        self.development_status = data["info"]["development_status"]
        self.description = data["info"]["description"]
        self.description_content_type = data["info"]["description_content_type"]
        self.keywords = data["info"]["keywords"]
        self.license = data["info"]["license"]
        self.maintainer = data["info"]["maintainer"]
        self.maintainer_email = data["info"]["maintainer_email"]
        self.package_url = data["info"]["package_url"]
        self.requires_python = data["info"]["requires_python"]
        self.summary = data["info"]["summary"]
        self.version = data["info"]["version"]
        self.releases = data["releases"] or {}

        # Mark as loaded
        self.loaded = True

        # Save
        self.save()


class AppPackage(models.Model):
    def __str__(self):
        return str(self.name)

    uuid = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False, unique=True
    )

    # General Info
    name = models.CharField(max_length=100)
    pkg_name = models.CharField(
        max_length=100,
        help_text="Must be snake_case. Importable name within Python.",
        unique=True,
    )
    pypi_name = models.CharField(
        max_length=100,
        help_text="Name used for PyPI package installation. Defaults to `pkg_name` if left blank.",
        blank=True,
    )
    custom_pip_install = models.TextField(
        help_text="Custom pip install command. "
        "If left blank, the default `pip install <pypi_name>` will be used.",
        blank=True,
    )
    logo = models.ImageField(
        upload_to=UUIDFilePath("serve/app_store/logos/"),
        blank=True,
    )
    background = models.ImageField(
        upload_to=UUIDFilePath("serve/app_store/backgrounds/"),
        blank=True,
    )
    developed = models.BooleanField(
        default=False,
        help_text="Whether or not this app has been developed. "
        "If not, it is a placeholder app.",
    )
    listed_on_pypi = models.BooleanField(
        default=False,
        help_text="Whether or not this app is listed on PyPI. "
        "If not, it is a placeholder app.",
    )
    special = models.BooleanField(
        default=False,
        help_text="If enabled, this app's cards will be visually highlighted. Reserved for donations.",
    )
    banner_message = models.TextField(
        blank=True,
        help_text="Optional text message shown on the app info modal.",
        max_length=1000,
    )
    long_description = models.TextField(
        blank=True,
        help_text="This description is hidden from the app info modal, but is viewable within the database admin GUI.",
    )
    donation_url = models.URLField(blank=True)
    subcategories = models.ManyToManyField(Subcategory)

    # Compatibility
    sys_platforms = MultiSelectField(
        choices=SysPlatform.choices,
        max_length=40,
        verbose_name="Supported Platforms",
        default=SysPlatform.ANY,
    )
    touch_compatible = models.BooleanField()
    mobile_compatible = models.BooleanField()
    min_version = VersionField(
        default="0.0.0",
        help_text="Minimum version of this package that is compatible with Conreq.",
    )
    conreq_min_version = VersionField(
        default="0.0.0",
        help_text="Minimum version Conreq needs to be to support this package.",
    )
    conreq_max_version = VersionField(
        help_text="Maximum version Conreq can be to support this package.",
        blank=True,
        null=True,
    )
    required_apps = models.ManyToManyField(
        "self",
        help_text="Conreq apps that must be installed for this package to function.",
        blank=True,
    )
    incompatible_apps = models.ManyToManyField(
        "self",
        help_text="Conreq apps that cannot be installed for this package to function.",
        blank=True,
    )
    related_apps = models.ManyToManyField(
        "self",
        help_text="Conreq apps that are related to this project.",
        blank=True,
    )

    # Start Up
    settings_script = PythonTextField(
        blank=True,
        help_text="Python code that will be run before boot up. "
        "This code is run directly within the context of Conreq's `settings.py`. "
        "If you need revision control for this script, create a dedicated `conreq_settings.py` file in your package release instead.",
    )
    app_config_script = PythonTextField(
        blank=True,
        help_text="Python code that will be run after boot up. "
        "This code is run directly within the context of an arbitrary `AppConfig.ready()` method. "
        "If you need revision control for this script, create a dedicated `AppConfig` in your package release instead.",
    )

    # Metadata
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    modified_at = models.DateTimeField(auto_now=True, editable=False)
    pypi_data = AutoOneToOneField(
        PyPiData, blank=True, null=True, on_delete=models.CASCADE, editable=False
    )

    @property
    def installed(self):
        """Checks if the app is already installed on the current system."""
        return self.pkg_name in get_env("INSTALLED_PACKAGES", [], return_type=list)

    @property
    def compatible(self):
        """Checks if the app is installable on the current system."""
        # pylint: disable=import-outside-toplevel
        from django.conf import settings

        # Invalid development stage
        if self.pypi_data and (
            not self.pypi_data.development_status
            or self.pypi_data.development_status == DevelopmentStage.PLANNING
        ):
            return False

        # Incorrect system platform
        if (
            SysPlatform.ANY not in self.sys_platforms
            and platform.system() not in self.sys_platforms
        ):
            return False

        # Incompatible Conreq version
        if version.parse(str(self.conreq_min_version)) > version.parse(
            str(settings.CONREQ_VERSION)
        ) or (
            self.conreq_max_version
            and version.parse(str(self.conreq_max_version))
            < version.parse(str(settings.CONREQ_VERSION))
        ):
            return False

        # Incompatible app is installed
        return not any(
            importlib.util.find_spec(app.pkg_name)
            for app in self.incompatible_apps.all()  # pylint: disable=no-member
        )


class SpotlightCategory(OrderedModel):
    def __str__(self):
        return str(self.name)

    class Meta:
        verbose_name = "Spotlight category"
        verbose_name_plural = "Spotlight categories"
        ordering = ["order"]

    uuid = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False, unique=True
    )

    name = models.CharField(max_length=50, unique=True)
    description = models.TextField(blank=True)
    apps = OrderedManyToManyField(AppPackage, through="SpotlightAppPackages")


class SpotlightAppPackages(OrderedModel):
    """This model is a `through` model used to create a many-to-many relationship
    between SpotlightCategory and AppPackage.
    This allows for the ordering of apps within a spotlight category."""

    category = models.ForeignKey(SpotlightCategory, on_delete=models.CASCADE)
    app = models.ForeignKey(AppPackage, on_delete=models.CASCADE)
    order_with_respect_to = "category"

    class Meta:
        ordering = ("category", "order")


class Screenshot(models.Model):
    def __str__(self):
        return str(self.title)

    uuid = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False, unique=True
    )

    title = models.CharField(max_length=100)
    description = models.CharField(max_length=255, blank=True)
    image = models.ImageField(upload_to=UUIDFilePath("serve/app_store/screenshot/"))
    app_package = models.ForeignKey(AppPackage, on_delete=models.CASCADE)


class AppNoticeMessage(models.Model):
    """Message that needs to be delivered to admins that currently have the app installed."""

    def __str__(self):
        return str(self.title)

    uuid = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False, unique=True
    )

    title = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    app_package = models.ForeignKey(AppPackage, on_delete=models.CASCADE)
    read_by = models.ManyToManyField(get_user_model(), blank=True)
