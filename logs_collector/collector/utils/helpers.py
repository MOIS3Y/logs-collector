import shutil
import pathlib


def logs_dir_path(instance, filename: str) -> str:
    """
        file will be uploaded to
        MEDIA_ROOT/view/<filename>
    """
    return f'{instance.ticket.number}/{filename}'


def sizify(value: int) -> str:
    """Simple kb/mb/gb size snippet for admin panel custom field:

    Args:
        value (int): size of file from Filefield

    Returns:
        str: format human readable size like 4.2 Gb
    """
    if value < 512000:
        value = value / 1024.0
        ext = 'KB'
    elif value < 4194304000:
        value = value / 1048576.0
        ext = 'MB'
    else:
        value = value / 1073741824.0
        ext = 'GB'
    return f'{round(value, 1)} {ext}'


def get_mount_fs_info(path: type[pathlib.PosixPath]) -> dict:
    """
        Get directory information for storing uploaded files.
        Includes information total/used/free space on mount device

    Args:
        path (pathlib.PosixPath): path to storage dir

    Returns:
        dict: storage mount info
    """
    mount_info: dict = {}
    try:
        mount_info = shutil.disk_usage(path)._asdict()
        mount_info['used_percent'] = round(
            mount_info['used'] / mount_info['total'] * 100,
        )
        mount_info['status'] = 'mount'
    except Exception as error:  # expected FileNotFoundError
        mount_info = {
            'total': 0,
            'used': 0,
            'free': 0,
            'used_percent': 0,
            'status': 'error',
            'traceback': f'{error}'
        }
    return mount_info
