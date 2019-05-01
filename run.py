import requests
import json
import urllib
import logging
import os
import sys

logging.basicConfig(level=logging.INFO)


with open('token.txt') as inf:
    token = inf.read().strip()

headers = {
    'Authorization': 'Bearer ' + token
}

CANVAS = 'https://canvas.vt.edu/api/v1/'
COURSE_FOLDERS_URL = CANVAS + 'courses/{course}/folders/root'

def mkdir(p):
    try:
        os.mkdir(p)
    except FileExistsError:
        logging.debug('Path %s already exists' % p)
    except PermissionError:
        logging.debug('Permission not granted to create %s' % p)

def mk_and_cd(p):
    cwd = os.getcwd()
    mkdir(p)
    os.chdir(p)
    return cwd

def download_file(f):
    logging.info('Downloading file "{display_name}" ({filename})'.format(**f))
    with open(f['display_name'], 'wb') as outf:
        resp = requests.get(f['url'], headers=headers)
        for chunk in resp.iter_content():
            outf.write(chunk)
    with open(f['display_name'] + '.meta.json', 'w') as outf:
        outf.write(json.dumps(f, indent=2))

def read_folder(url_or_object):
    root = None
    if type(url_or_object) is dict:
        root = url_or_object
    elif type(url_or_object) is str:
        root = requests.get(url_or_object, headers=headers)
        root = root.json()
    else:
        assert "This is not OK"
    logging.debug(str(root))
    logging.info('Processing folder "{}"'.format(root['full_name']))

    old_dir = mk_and_cd(root['name'])

    if 'status' in root and root['status'] == 'unauthorized':
        logging.warning('Failed to list folder {}'.format(root))

    with open('folder_meta.json', 'w') as outf:
        outf.write(json.dumps(root, indent=2))

    if 'files_url' in root and root['files_count'] > 0:
        logging.info('Processing %d files' % root['files_count'])
        files = requests.get(root['files_url'], headers=headers)
        files = files.json()
        for f in files:
            download_file(f)

    if 'folders_url' in root and root['folders_count'] > 0:
        logging.info('Processing %d sub-folders' % root['folders_count'])
        folders = requests.get(root['folders_url'], headers=headers)
        folders = folders.json()
        for folder in folders:
            read_folder(folder)
        # logging.info('Sub-folders: %s' % folders)

    os.chdir(old_dir)

def main():
    courses = requests.get(CANVAS + 'users/self/courses', headers=headers, params={
        'per_page': 200,
    })
    courses = courses.json()

    mk_and_cd('output');

    for course in courses:
        logging.info(course['name'] + ' :')

        root = mk_and_cd(course['name'])

        # Dump course metadata
        with open('course_meta.json', 'w') as outf:
            outf.write(json.dumps(course, indent=2))

        # Dump all course files
        read_folder(COURSE_FOLDERS_URL.format(course=course['id']))

        os.chdir(root)

if __name__ == '__main__':
    main()
