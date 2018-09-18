#!/usr/bin/env python

import os
import random
import requests
import string
import sys


DEFAULT_HOST = 'localhost'
DEFAULT_PORT = 8000


class Client(object):

    def __init__(self, host, port, client_id=None) -> None:
        self.host = host
        self.port = port
        self.client_id = client_id or random_id()

    def turn_on(self):
        requests.post(self.url)

    def turn_off(self):
        requests.delete(self.url)

    def change_color_hex(self, hex):
        body = {
            'hex': hex,
            'client_id': self.client_id
        }
        requests.put(self.url, data=body)

    @property
    def url(self):
        return 'http://%s:%s/light/' % (self.host, self.port)


def random_id():
    return ''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(6))


def run(args):

    if len(args) == 0:
        print_usage()

    host = os.environ.get('RAYNER_HOST', DEFAULT_HOST)
    port = os.environ.get('RAYNER_PORT', DEFAULT_PORT)
    client_id = 'cli-%s' % random_id()

    c = Client(host, port, client_id=client_id)

    if args[0] == 'on':
        c.turn_on()
    elif args[0] == 'off':
        c.turn_off()
    elif args[0] == 'color':
        c.change_color_hex(args[1])


def print_usage():
    print('Please specify one of: on, off, color <hex>')


if __name__ == '__main__':
    run(sys.argv[1:])
