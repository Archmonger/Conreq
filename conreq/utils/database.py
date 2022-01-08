from datetime import datetime, timedelta
from glob import glob
from pathlib import Path

from django.core.management import call_command


def add_unique(model, **kwargs):
    """Adds a row to the database only if all parameters are unique."""
    if not model.objects.filter(**kwargs):
        new_request = model(**kwargs)
        new_request.clean_fields()
        new_request.save()
        return new_request
    return None


def backup_needed() -> bool:
    """Returns True if a database backup is needed."""
    # pylint: disable=import-outside-toplevel
    from django.conf import settings

    backup_dir = getattr(settings, "BACKUP_DIR")
    dbbackup_date_format = getattr(settings, "DBBACKUP_DATE_FORMAT")
    backup_files = sorted(glob(str(backup_dir / "*.*")), reverse=True)

    for file_path in backup_files:
        try:
            file_name = Path(file_path).stem.rstrip(".dump")
            file_date = datetime.strptime(file_name, dbbackup_date_format)
            return datetime.now() - timedelta(weeks=1) > file_date
        except Exception:
            pass

    # No backup files were found, or backup has expired
    return True


def backup():
    """Creates a database backup."""
    call_command(
        "dbbackup",
        "--clean",
        "--compress",
    )
