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


class PackageVersion(models.Model):
    def __str__(self):
        return str(self.version)

    version = VersionField(unique=True)


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
        help_text="Must be snake_case. Used for PyPI package installation, or folder naming on Git installations.",
        unique=True,
    )
    logo = models.ImageField(
        upload_to=UUIDFilePath("serve/app_store/logos/"),
        blank=True,
    )
    background = models.ImageField(
        upload_to=UUIDFilePath("serve/app_store/backgrounds/"),
        blank=True,
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
    short_description = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    # PyPI Info
    sync_with_pypi = models.BooleanField(
        default=False,
        help_text="Will automatically sync relevant information with the latest PyPI version.",
        verbose_name="Sync with PyPI",
    )
    long_description = models.TextField(blank=True)
    long_description_type = models.CharField(
        max_length=20,
        choices=DescriptionType.choices,
        default=DescriptionType.TXT,
    )
    versions = models.ManyToManyField(PackageVersion, blank=True)

    # Package Details
    development_stage = models.CharField(
        max_length=21,
        choices=DevelopmentStage.choices,
        default=DevelopmentStage.PLANNING,
        blank=True,
    )
    subcategories = models.ManyToManyField(Subcategory)

    # Ownership Info
    author = models.CharField(blank=True, max_length=50)
    author_url = models.URLField(
        blank=True,
        help_text="This is typically a link to your GitHub user account or organization.",
    )
    contact_email = models.EmailField(blank=True)
    contact_link = models.URLField(
        blank=True,
        help_text='Link takes priority of email for the small "Contact" button.',
    )
    pypi_url = models.URLField(blank=True)
    repository_url = models.URLField(
        blank=True,
        help_text="Must be a Git repository if not using PyPI.",
    )
    homepage_url = models.URLField(blank=True)
    support_url = models.URLField(blank=True)
    donation_url = models.URLField(blank=True)
    license_type = models.CharField(max_length=100, default="GPLv3")

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
        help_text="Minimum PyPI version or Git tag for this package that is compatible with Conreq.",
    )
    conreq_min_version = VersionField(default="0.0.0")
    conreq_max_version = VersionField(blank=True, null=True)
    asynchronous = models.CharField(
        max_length=20,
        choices=AsyncCompatibility.choices,
        default=AsyncCompatibility.NONE,
    )
    required_apps = models.ManyToManyField("self", blank=True)
    incompatible_apps = models.ManyToManyField("self", blank=True)
    related_apps = models.ManyToManyField("self", blank=True)

    # Installable property that checks the development_stage, sys_platforms, and conreq_min_version fields
    # to determine if the app is installable on the current system.
    # Also checks if any incompatible apps are installed.
    @property
    def installable(self):
        # pylint: disable=import-outside-toplevel
        from django.conf import settings

        # Invalid development stage
        if (
            not self.development_stage
            or self.development_stage == DevelopmentStage.PLANNING
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
