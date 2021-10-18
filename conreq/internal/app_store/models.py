import uuid

from django.db import models
from model_utils import FieldTracker
from multiselectfield import MultiSelectField
from versionfield import VersionField


# Create your models here.
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


class SysPlatforms(models.TextChoices):
    AIX = "AIX", "Aix"
    LINUX = "LINUX", "Linux"
    WINDOWS = "WINDOWS", "Windows"
    CYGWIN = "CYGWIN", "Cygwin"
    MACOS = "MACOS", "Darwin"


class DescriptionTypes(models.TextChoices):
    PLAIN = "text/plain", "Plain Text (.txt)"
    RST = "text/x-rst", "reStructuredText (.rst)"
    MARKDOWN = "text/markdown", "Markdown (.md)"


class Category(models.Model):
    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Categories"

    # Basic Info
    name = models.CharField(max_length=50)
    description = models.TextField(blank=True, null=True)

    # Tracker
    tracker = FieldTracker()


class Subcategory(models.Model):
    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Subcategory"
        verbose_name_plural = "Subcategories"

    # Basic Info
    name = models.CharField(max_length=50)
    description = models.TextField(blank=True, null=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    # Tracker
    tracker = FieldTracker()


class AppPackage(models.Model):
    def __str__(self):
        return self.verbose_name

    # Unique Identifier
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    # Basic Info
    package_name = models.CharField(max_length=100, help_text="Must be snake_case.")
    verbose_name = models.CharField(max_length=100)
    description = models.CharField(max_length=255, blank=True, null=True)
    long_description = models.FileField(upload_to="app_store/readme/")
    long_description_type = models.CharField(
        max_length=20,
        choices=DescriptionTypes.choices,
        default=DescriptionTypes.MARKDOWN,
    )
    subcategories = models.ManyToManyField(Subcategory)
    development_stage = models.CharField(
        max_length=21, choices=DevelopmentStage.choices, blank=True, null=True
    )
    version = VersionField()
    banner_message = models.TextField(blank=True, null=True)

    # Ownership Info
    author = models.CharField(max_length=50)
    author_email = models.EmailField(blank=True, null=True)
    repository_url = models.URLField()
    homepage_url = models.URLField(blank=True, null=True)
    support_url = models.URLField(blank=True, null=True)
    donation_url = models.URLField(blank=True, null=True)
    pypi_url = models.URLField(blank=True, null=True)
    license_type = models.CharField(max_length=100, default="GPLv3")

    # Environment
    sys_platforms = MultiSelectField(choices=SysPlatforms.choices, max_length=10)

    # Compatibility
    touch_compatible = models.BooleanField()
    mobile_compatible = models.BooleanField()
    minimum_conreq_version = VersionField()
    tested_conreq_version = VersionField()
    max_conreq_version = VersionField(blank=True, null=True)
    asynchronous = models.CharField(max_length=20, choices=AsyncCompatibility.choices)

    # App Dependencies
    required_apps = models.ManyToManyField("self", blank=True)
    optional_apps = models.ManyToManyField("self", blank=True)
    incompatible_apps = models.ManyToManyField("self", blank=True)
    incompatible_categories = models.ManyToManyField(
        Category, related_name="incompatible_categories", blank=True
    )
    incompatible_subcategories = models.ManyToManyField(
        Subcategory, related_name="incompatible_subcategories", blank=True
    )

    # Tracker
    tracker = FieldTracker()


class EnvironmentVariable(models.Model):
    def __str__(self):
        return self.name + ' = "' + str(self.default) + '"'

    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=50)
    default = models.CharField(max_length=255, blank=True, null=True)
    example = models.CharField(max_length=255, blank=True, null=True)
    required = models.BooleanField(default=False, blank=True, null=True)
    app_package = models.ForeignKey(AppPackage, on_delete=models.CASCADE)


class Screenshot(models.Model):
    def __str__(self):
        return self.title

    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=255, blank=True, null=True)
    image = models.ImageField(upload_to="app_store/screenshot/")
    app_package = models.ForeignKey(AppPackage, on_delete=models.CASCADE)


class NoticeMessage(models.Model):
    def __str__(self):
        return self.title

    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    mark_read = models.BooleanField(default=False, blank=True, null=True)
    app_package = models.ForeignKey(AppPackage, on_delete=models.CASCADE)
