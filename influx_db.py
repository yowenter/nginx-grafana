#!/bin/env python
#coding=utf-8
__author__ = 'kebe'

from influxdb import InfluxDBClient

CONFIG = {
    'host': '192.168.1.131',
    'port': 8086,
    'username': 'root',
    'password': 'root',
    'database': 'daovoice'
}

def get_db_client():
    return InfluxDBClient(CONFIG['host'],
                          CONFIG['port'],
                          CONFIG['username'],
                          CONFIG['password'],
                          CONFIG['database'])
