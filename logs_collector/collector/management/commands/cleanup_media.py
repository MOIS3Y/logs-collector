import os
import logging
from django.core.management.base import BaseCommand
from django.apps import apps
from django.db.models import Q
from django.conf import settings
from django.db.models import FileField


logger = logging.getLogger(__name__)

logging.config.dictConfig({
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'console': {
            'format': '%(asctime)s %(name)-12s %(levelname)-8s %(message)s'
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'console'
        },
    },
    'loggers': {
        '': {
            'level': 'INFO',
            'handlers': ['console']
        }
    }
})


class Command(BaseCommand):
    # HELP MESSAGE:
    help_part1 = 'This command deletes all media files from'
    help_part2 = 'the MEDIA_ROOT directory which are no longer referenced'
    help_part3 = 'by any of the models from installed_apps'
    help = f'{help_part1} {help_part2} {help_part3}'

    def handle(self, *args, **options):
        logger.info('Start cleanup storage....')
        all_models = apps.get_models()
        physical_files = set()
        db_files = set()
        # Get all files from the database
        logger.info('Get all files from the database....')
        for model in all_models:
            file_fields = []
            filters = Q()
            for f_ in model._meta.fields:
                if isinstance(f_, FileField):
                    file_fields.append(f_.name)
                    is_null = {'{}__isnull'.format(f_.name): True}
                    is_empty = {'{}__exact'.format(f_.name): ''}
                    filters &= Q(**is_null) | Q(**is_empty)
            # only retrieve the models which have non-empty,
            # non-null file fields
            if file_fields:
                files = model.objects.exclude(filters).values_list(
                    *file_fields,
                    flat=True
                ).distinct()
                db_files.update(files)
        logger.info(f'Find: {len(db_files)} files from the database')
        # Get all files from the MEDIA_ROOT, recursively
        logger.info('Get all files from the MEDIA_ROOT, recursively....')
        media_root = getattr(settings, 'MEDIA_ROOT', None)
        if media_root is not None:
            for relative_root, dirs, files in os.walk(media_root):
                for file_ in files:
                    # Compute the relative file path to the media directory,
                    # so it can be compared to the values from the db
                    relative_file = os.path.join(
                        os.path.relpath(relative_root, media_root), file_
                    )
                    physical_files.add(relative_file)
        logger.info(f'Find: {len(physical_files)} files from the MEDIA_ROOT')
        # Compute the difference and delete those files
        logger.info('Compute the difference and delete those files....')
        deletables = physical_files - db_files
        logger.info(f'Find: {len(deletables)} orphan files')
        if deletables:
            for file_ in deletables:
                logger.info(f"Delete orphan file: {file_}")
                os.remove(os.path.join(media_root, file_))
            # Bottom-up - delete all empty folders
            logger.info('Bottom-up - delete all empty folders....')
            for relative_root, dirs, files in os.walk(
                    media_root, topdown=False):
                for dir_ in dirs:
                    if not os.listdir(os.path.join(relative_root, dir_)):
                        os.rmdir(os.path.join(relative_root, dir_))
            logger.info('Done! Storage has been cleaned up')
        logger.info('Done! Nothing to delete')
