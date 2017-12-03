#!/usr/bin/env python

import configparser
import HostProcess
import requests
import time

sleep_time = 10

def get_pending_hosts(read_url):
    return requests.get(read_url).json()


def process_pending_hosts(read_url, write_url):

    hosts = get_pending_hosts(read_url)
    print(hosts)
    for host in hosts:
        host = HostProcess.populate_available_updates(host)
        print(host)
        requests.post(write_url, json=host)

def main():

    config = configparser.ConfigParser()
    config.read('urls.cfg')

    read_url = config.get('urls', 'read_url')
    write_url = config.get('urls', 'write_url')

    while(True):
        process_pending_hosts(read_url, write_url)
        time.sleep(sleep_time)

if __name__ == '__main__':
    main()