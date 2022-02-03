import uuid

from django.db import models
from multiselectfield import MultiSelectField
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
    NONE = "NONE", "No Async"
    SEMI = "SEMI", "Semi Async"
    FULL = "FULL", "Fully Async"


class SysPlatform(models.TextChoices):
    AIX = "AIX", "Aix"
    LINUX = "LINUX", "Linux"
    WINDOWS = "WINDOWS", "Windows"
    CYGWIN = "CYGWIN", "Cygwin"
    MACOS = "MACOS", "Darwin"


class DescriptionType(models.TextChoices):
    PLAIN = "text/plain", "Plain Text (.txt)"
    RST = "text/x-rst", "reStructuredText (.rst)"
    MARKDOWN = "text/markdown", "Markdown (.md)"


class Category(models.Model):
    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Categories"

    uuid = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False, unique=True
    )

    # Basic Info
    name = models.CharField(max_length=50, unique=True)


class Subcategory(models.Model):
    def __str__(self):
        return self.name

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
        return self.verbose_name

    uuid = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False, unique=True
    )

    # Basic Info
    package_name = models.CharField(
        max_length=100,
        help_text="Must be snake_case. Used for PyPI package installation, or folder naming on Git installations.",
    )
    verbose_name = models.CharField(max_length=100)
    logo = models.ImageField(
        upload_to=UUIDFilePath("serve/app_store/logos/"),
        blank=True,
    )
    short_description = models.CharField(max_length=255, blank=True)
    long_description = models.TextField(
        blank=True,
        help_text="This will be automatically fetched from PyPI or Git if left empty.",
    )
    long_description_type = models.CharField(
        max_length=20,
        choices=DescriptionType.choices,
        default=DescriptionType.MARKDOWN,
    )
    subcategories = models.ManyToManyField(Subcategory)
    development_stage = models.CharField(
        max_length=21, choices=DevelopmentStage.choices, blank=True
    )
    min_version = VersionField(
        default="0.0.0",
        help_text="Minimum PyPI version or Git tag for this package that is compatible with Conreq.",
    )
    banner_message = models.TextField(
        blank=True,
        help_text="Optional text message banner shown this apps details page.",
    )
    sync_with_pypi = models.BooleanField(
        default=False,
        help_text="Will automatically sync relevant information with the latest PyPI version.",
        verbose_name="Sync with PyPI",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    versions = models.ManyToManyField(PackageVersion, blank=True)

    # Ownership Info
    author = models.CharField(max_length=50)
    author_email = models.EmailField(blank=True)
    pypi_url = models.URLField(blank=True)
    repository_url = models.URLField(
        blank=True,
        help_text="Must be a Git repository if not using PyPI.",
    )
    homepage_url = models.URLField(blank=True)
    support_url = models.URLField(blank=True)
    donation_url = models.URLField(blank=True)
    license_type = models.CharField(max_length=100, default="GPLv3")

    # Environment
    sys_platforms = MultiSelectField(choices=SysPlatform.choices, max_length=10)

    # Compatibility
    touch_compatible = models.BooleanField()
    mobile_compatible = models.BooleanField()
    conreq_min_version = VersionField(default="0.0.0")
    conreq_tested_version = VersionField()
    conreq_max_version = VersionField(blank=True, null=True)
    asynchronous = models.CharField(max_length=20, choices=AsyncCompatibility.choices)

    # App Dependencies
    required_apps = models.ManyToManyField("self", blank=True)
    optional_apps = models.ManyToManyField("self", blank=True)
    incompatible_apps = models.ManyToManyField("self", blank=True)
    incompatible_subcategories = models.ManyToManyField(
        Subcategory, related_name="incompatible_subcategories", blank=True
    )


class Screenshot(models.Model):
    def __str__(self):
        return self.title

    uuid = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False, unique=True
    )

    title = models.CharField(max_length=100)
    description = models.CharField(max_length=255, blank=True)
    image = models.ImageField(upload_to=UUIDFilePath("serve/app_store/screenshot/"))
    app_package = models.ForeignKey(AppPackage, on_delete=models.CASCADE)


class NoticeMessage(models.Model):
    def __str__(self):
        return self.title

    uuid = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False, unique=True
    )

    title = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    app_package = models.ForeignKey(AppPackage, on_delete=models.CASCADE)