#!/usr/bin/env python

import os
import random
import requests
import string
import sys
import time


DEFAULT_HOST = 'localhost'
DEFAULT_PORT = 8000


RAINBOW = (
    'ff4534',  # red
    'ff8d1f',  # orange
    'ffcd33',  # yellow
    'ebff43',  # green
    'b6b2ff',  # cyan
    '5f16ff',  # blue
    '7f54ff',  # purple
)


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

    def rainbow(self, delay):
        body = {
            'hex': None,
            'client_id': self.client_id
        }
        for c in RAINBOW:
            body['hex'] = c
            requests.put(self.url, data=body)
            time.sleep(delay)

    def random(self, count, delay):
        body = {
            'hex': None,
            'client_id': self.client_id
        }
        for _ in range(count):
            body['hex'] = random.choice(RAINBOW)
            requests.put(self.url, data=body)
            time.sleep(delay)

    def state(self):
        response = requests.get(self.url)
        s = response.json()
        print('On: %s' % s['on'])
        print('Hex: %s' % s['hex'])
        print('Hue: %s' % s['hue'])
        print('Brightness: %s' % s['brightness'])
        print('Saturation: %s' % s['saturation'])

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
    elif args[0] == 'state':
        c.state()
    elif args[0] == 'rainbow':
        if len(args) > 1:
            delay = int(args[1])
        else:
            delay = 1
        c.rainbow(delay)
    elif args[0] == 'random':
        if len(args) > 1:
            count = int(args[1])
        else:
            count = 5
        if len(args) > 2:
            delay = int(args[2])
        else:
            delay = 1

        c.random(count, delay)


def print_usage():
    print('Please specify one of: on, off, color <hex>, rainbow <delay>, random <count> <delay>')


if __name__ == '__main__':
    run(sys.argv[1:])
