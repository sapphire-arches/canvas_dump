from canvas_dump_lib import headers, read_folder, CANVAS
from canvas_dump_utils import mk_and_cd
import requests
import os
import json

def main():
    mk_and_cd('output');

    read_folder(CANVAS + 'users/self/folders/root')

if __name__ == '__main__':
    main()
