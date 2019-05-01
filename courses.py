from canvas_dump_lib import headers, read_folder, CANVAS
from canvas_dump_utils import mk_and_cd
import requests
import os
import json

COURSE_FOLDERS_URL = CANVAS + 'courses/{course}/folders/root'

def main():
    courses = requests.get(CANVAS + 'users/self/courses', headers=headers, params={
        'per_page': 200,
    })
    courses = courses.json()

    mk_and_cd('output');

    for course in courses:
        logging.info('Processing class "{}"'.format(course['name']))

        root = mk_and_cd(course['name'])

        # Dump course metadata
        with open('course_meta.json', 'w') as outf:
            outf.write(json.dumps(course, indent=2))

        # Dump all course files
        read_folder(COURSE_FOLDERS_URL.format(course=course['id']))

        os.chdir(root)

if __name__ == '__main__':
    main()
