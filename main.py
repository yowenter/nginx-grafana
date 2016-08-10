import sys
import re
import influx_db
import time

nginx_log_pattern = re.compile('\s*(?P<ip>\d+.\d+.\d+.\d+)\s-\s-\s\[(?P<date>.+)\]\s"(?P<method>\w+)\s(?P<path>\S+)')

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
        self.datetime = datetime
        self.method = method
        self.path = path

class InfluxDBClient:

    def __init__(self):
        self._db_client = influx_db.get_db_client()

    def save_request_info(self, req_dict):
        data = []
        for method in req_dict.keys():
            for path in req_dict[method].keys():
                data.append({
                    'measurement': 'api_requests_info',
                    'tags': {
                        'method': method,
                        'path': path
                    },
                    'fields': {
                        'count': req_dict[method][path]
                    }
                })
        self._db_client.write_points(data)


def replace_uuid(path):
    path_without_uuid = re.sub(r'([0-9a-f]{8}-([0-9a-f]{4}-){3}[0-9a-f]{12})', 'uuid', path)
    path_without_params = re.sub(r'(\?.+)', '', path_without_uuid)
    return re.sub(r'apps/(.{8})', 'apps/app_uuid', path_without_params)

def get_init_req_dict():
    return {
        'POST': {},
        'GET': {},
        # 'OPTIONS': {},
        'DELETE': {},
        'PATCH': {},
        'PUT': {},
    }

def main():
    req_dict = get_init_req_dict()
    last_save_time = time.time()
    for line in input_stream():
        data_tuple = Parser(line).parse()
        if data_tuple:
            data = RequestData(*data_tuple)
            path = replace_uuid(data.path)
            if not data or \
                    data.method not in req_dict.keys() or \
                    '.' in data.path:
                continue
            if req_dict[data.method].get(path) is None:
                req_dict[data.method][path] = 1
            else:
                req_dict[data.method][path] += 1
        now_time = time.time()
        if now_time - last_save_time > 60:
            # Save
            client = InfluxDBClient()
            client.save_request_info(req_dict)
            last_save_time = now_time
            req_dict = get_init_req_dict()

if __name__ == '__main__':
    main()
