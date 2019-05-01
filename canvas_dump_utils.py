import os
import logging

logging.basicConfig(level=logging.INFO)

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
