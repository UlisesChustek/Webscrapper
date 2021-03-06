import logging
logging .basicConfig(level =logging.INFO)
import subprocess
import datetime
import os
import shutil
import sys

logger = logging.getLogger(__name__)
news_sites_uids = ['nytimes','TWP','padaily']
now = datetime.datetime.now().strftime('%Y_%m_%d')

def main():
    _extract()
    _transform()
    _load()


def _extract():
    logger.info('Starting extract process')
    for news_site_uid in news_sites_uids:
        subprocess.run(['python', 'newspaper_created.py', news_site_uid], cwd='./extract')
        path = './extract'
        file = _search_file(path, news_site_uid)
        _move_file(path + '/' + file, './transform/' + file)

def _transform():
    logger.info('Starting transform process')
    for news_site_uid in news_sites_uids:
        dirty_data_filename = _search_file('.\\transform', news_site_uid)
        clean_data_filename = f'clean_{dirty_data_filename}'
        subprocess.run(['python', 'newspaper_receipe.py', dirty_data_filename], cwd='./transform')
        _remove_file('.\\transform', dirty_data_filename)
        _move_file('.\\transform\\' + clean_data_filename, '.\\load\\' + clean_data_filename)

def _load():
    logger.info('Starting load process')
    for news_site_uid in news_sites_uids:
        clean_data_filename = _search_file('.\\load', news_site_uid)
        subprocess.run(['python', 'charger_db.py', clean_data_filename], cwd='./load')
        _remove_file('.\\load', clean_data_filename)


def _remove_file(path, file):
    logger.info(f'Removing file {file}')
    os.remove(f'{path}/{file}')


def _search_file(path, file_match):
    logger.info('Searching file')
    for root in list(os.walk(path))[0]:
        if len(root) > 1:
            for file in root:
                if file_match in file:
                    return file
    return None


def _move_file(origin, destiny):
    logger.info('Moving file')
    shutil.move(origin, destiny)


def main():
    try:
        logger.info('Starting ETL process')
        _extract()
        _transform()
        _load()
        logger.info('ETL process finished')
    except FileNotFoundError as err:
        logger.warning(str(err))
    except Exception as e:
        logger.warning('Process Error')
        logger.warning(str(e))
        # e.with_traceback()


if __name__ == '__main__':
    main()