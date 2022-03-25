import contextlib
import os
import shutil
from datetime import datetime, timedelta
from glob import glob
from pathlib import Path

from django.core.management import call_command


def backup_now():
    """Performs the backup process at the current timestamp."""
    # TODO: Create an API for developers to add on their own backup steps during this function call
    # pylint: disable=import-outside-toplevel
    from django.conf import settings

    backup_date = datetime.now().strftime(settings.BACKUP_DATE_FORMAT)
    backup_path = Path(settings.BACKUP_DIR / backup_date)
    db_backup_path = backup_path / "database"
    os.makedirs(db_backup_path)
    for db_name in settings.DATABASES:
        call_command(
            "dumpdata",
            "--database",
            db_name,
            "--output",
            f"{backup_path / 'database' / db_name}.json.{settings.BACKUP_COMPRESSION}",
            "--verbosity",
            "0",
        )

    delete_old_backups()


def backup_folders() -> list[Path]:
    """Returns a sorted list of backup folders."""
    # pylint: disable=import-outside-toplevel
    from django.conf import settings

    backup_dir_contents = sorted(glob(str(settings.BACKUP_DIR / "*")), reverse=True)
    folders = []
    for item in backup_dir_contents:
        with contextlib.suppress(ValueError):
            path = Path(item)
            name = path.name if path.is_dir() else ""
            # Only append folders that follow our format
            datetime.strptime(name, settings.BACKUP_DATE_FORMAT)
            folders.append(path)
    return folders


def backup_needed() -> bool:
    """Returns True if a database backup is needed."""
    # pylint: disable=import-outside-toplevel
    from django.conf import settings

    latest_backup = backup_folders()[0]
    folder_name = latest_backup.name
    backup_date = datetime.strptime(folder_name, settings.BACKUP_DATE_FORMAT)
    return datetime.now() - timedelta(weeks=1) > backup_date


def delete_old_backups():
    """Deletes old backups beyond the maximum number of backups allowed."""
    # pylint: disable=import-outside-toplevel
    from django.conf import settings

    backups = backup_folders()
    if len(backups) <= settings.BACKUP_KEEP_MAX:
        return

    for folder in backups[settings.BACKUP_KEEP_MAX :]:
        shutil.rmtree(folder)
