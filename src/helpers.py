import json
import gzip

def write_gzip_json(filename, data):
    """Write a gzipped JSON file"""
    # https://stackoverflow.com/questions/39450065/python-3-read-write-compressed-json-objects-from-to-gzip-file
    with gzip.GzipFile(filename, 'w') as fout:
        fout.write(json.dumps(data).encode('utf-8'))

def read_gzip_json(filename):
    with gzip.GzipFile(filename, 'r') as fin:
        data = json.loads(fin.read().decode('utf-8'))
    return data
