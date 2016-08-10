import sys
import re
import requests

nginx_log_pattern = re.compile(
    '\s*(?P<ip>\d+.\d+.\d+.\d+)\s-\s-\s\[(?P<date>.+)\]\s"(?P<method>\w+)\s(?P<path>\S+)')


def input_stream():
    for line in sys.stdin:
        yield line


class Parser(object):

    def __init__(self, text):
        self.text = text

    def parse(self):
        m = nginx_log_pattern.match(self.text)
        if m:
            return m.groups()
        return None


class RequestData(object):
    """docstring for RequestData"""

    def __init__(self, ip, datetime, method, path):
        self.ip = ip
        self.datetime = self.datetime
        self.method = method
        self.path = path

    def as_dict(self, use_grafana=True):
        if use_grafana:
            return {}


class GrafanaClient(requests.Session):
    pass


def main():
    for line in input_stream():
        data_tuple = Parser(line).parse()
        if data_tuple:
            data = RequestData(*data_tuple)


if __name__ == '__main__':
    main()
