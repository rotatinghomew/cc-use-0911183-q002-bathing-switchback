from pathlib import Path
import json

from .allocation import *
from .services import *
from .planning import *


class Application:
    def __init__(self, store):
        self.store = store

    def seed(self):
        directory = Path(__file__).resolve().parent.parent / 'fixtures'
        for path in sorted(directory.glob('*.json')):
            if not self.store.all(path.stem):
                self.store.put_many(path.stem, json.loads(path.read_text(encoding='utf-8')))

    def demo(self):
        return {'descriptive': descriptive_periods(self.store), 'costs': course_costs(self.store), 'candidate': quote_expansion(self.store, ['north'])}

    def check(self):
        value = self.demo()
        return {'status': 'ok', 'summary': value}

    def call(self, method, route, payload):
        if method == 'GET' and route == 'summary':
            return self.demo()
        if method == 'POST' and route == 'service':
            return {'revision': save_service(self.store, payload)}
        if method == 'POST' and route == 'assignment':
            return {'revision': save_assignment(self.store, payload)}
        if method == 'POST' and route == 'quote':
            return quote_expansion(self.store, payload['teams'])
        raise KeyError('接口不存在')
