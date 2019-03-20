#!/usr/bin/env python

import os
import GeoIP
import urllib2
from flask import request
import utils

def info(ip):
    thisf = os.path.abspath(__file__)
    cdir  = os.path.dirname(thisf)
    dataf = os.path.join(cdir.replace('exec', 'static/data/'),'GeoIP.dat')

    ogeo    = GeoIP.open(dataf, GeoIP.GEOIP_STANDARD)
    country = ogeo.country_name_by_addr(ip)
    retval = ' '.join([str(ip),'[',str(country),']'])
    return retval


# from http://commandline.org.uk/python/how-to-find-out-ip-address-in-python/
def public_ip():
    op = urllib2.urlopen('http://ploskon.com/georaw')
    return op.readlines()[0].strip('\n')


def response():
    remoteip = request.remote_addr
    iptext = '`' + info(remoteip) + '`'
    if remoteip == '127.0.0.1':
        remoteip = public_ip()
        iptext += ' but your public ip is: `' + info(remoteip) + '`'
    # response = '##Here is what we found...\n```\nYour ip shows: {}\n```'.format(iptext)
    retval = '### Your ip shows: __{}__'.format(iptext)
    return retval

def response_ip():
    remoteip = request.remote_addr
    iptext = info(remoteip)
    if remoteip == '127.0.0.1':
        remoteip = public_ip()
    # response = '##Here is what we found...\n```\nYour ip shows: {}\n```'.format(iptext)
    return remoteip

def ping():
    sip = response_ip()
    ping_result = utils.call_exec('ping -t 1 -c 1 -i 0.2 {}'.format(sip), ' ')
    if not ping_result:
        ping_result = 'Single ping failed.'
    return ping_result

if __name__ == "__main__":
    ip = public_ip()
    print info(ip)
    print ping()
