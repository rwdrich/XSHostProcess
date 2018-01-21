#!/usr/bin/env python

import configparser
import HostProcess
import requests
import time

sleep_time = 10



def get_pending_hosts(read_url, read_key):
    print(read_url, read_key)
    return requests.get(read_url, params={'code': read_key, 'subset': 'pending'}).json()


def can_process_host(host):
    return 'host_version' in host and 'installed_updates' in host


def process_pending_hosts(read_url, read_key, write_url, write_key):
    hosts = [host for host in get_pending_hosts(read_url, read_key) if can_process_host(host)]
    print(hosts)
    for host in hosts:
        host = HostProcess.populate_available_updates(host)
        print(host)
        requests.post(write_url, params={'code': write_key}, json=host)

def main():

    urls_config = configparser.SafeConfigParser()
    urls_config.read('urls.cfg')
    read_url = urls_config.get('urls', 'read_url')
    write_url = urls_config.get('urls', 'write_url')

    credentials_config = configparser.SafeConfigParser()
    credentials_config.read('credentials.cfg')
    read_key = credentials_config.get('apis', 'read_key')
    write_key = credentials_config.get('apis', 'write_key')

    while(True):
        process_pending_hosts(read_url, read_key, write_url, write_key)
        time.sleep(sleep_time)

if __name__ == '__main__':
    main()