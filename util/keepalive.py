# (c) adarsh-goel

import logging
import requests
from info  import *
def ping_server():
    k = requests.get(f'https://ping-pong-sn.herokuapp.com/pingback?link={URL}').json()
    if not k.get('error'):
        logging.info('KeepAliveService: Pinged {} with status {}'.format(FQDN, k.get('Status')))
    else:
        logging.error('Couldn\'t Ping the Server!')
