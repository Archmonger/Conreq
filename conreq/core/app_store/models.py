import uuid

from django.db import models
from jsonfield import JSONField
from model_utils import FieldTracker
from multiselectfield import MultiSelectField
from versionfield import VersionField


# Create your models here.
class DevelopmentStage(models.TextChoices):
    PREALPHA = "PREALPHA", "Pre-Alpha"
    ALPHA = "ALPHA", "Alpha"
    BETA = "BETA", "Beta"
    STABLE = "STABLE", "Stable"
    DEPRECATED = "DEPRECATED", "Deprecated"
    OBSOLETE = "OBSOLETE", "Obsolete"


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


class Category(models.Model):
    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Category"
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
        return self.name

    # Unique Identifier
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    # Basic Info
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    subcategories = models.ManyToManyField(Subcategory)
    development_stage = models.CharField(
        max_length=20, choices=DevelopmentStage.choices, blank=True, null=True
    )
    version = VersionField()
    screenshots = JSONField(default=[], blank=True)
    notice_message = models.TextField(blank=True, null=True)

    # Ownership Info
    author = models.CharField(max_length=50)
    repository_url = models.URLField(blank=True, null=True)
    homepage_url = models.URLField(blank=True, null=True)
    support_url = models.URLField(blank=True, null=True)
    donation_url = models.URLField(blank=True, null=True)

    # Environment
    environment_variables = JSONField(default=[], blank=True)
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
