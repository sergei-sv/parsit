from unittest import TestCase
from ..parse import parse_dotnum, remove_rnt, parse_int, parse_comnum


class TestParse(TestCase):
    def test_parse_dotnum(self):
        test_data = [
            {'input': '42.33 usd', 'output': '42.33'},
            {'input': '42 usd', 'output': None},
            {'input': ' usd', 'output': None},
            {'input': '.2 usd', 'output': None},
            {'input': None, 'output': None},
            {'input': '', 'output': ''},
            {'input': '12.12.12', 'output': '12.12'},
            {'input': 12.4, 'output': 12.4},
            {'input': ['12.1'], 'output': ['12.1']},
        ]
        for data in test_data:
            result = parse_dotnum(data['input'])
            self.assertEqual(result, data['output'])


    def test_parse_comnum(self):
        test_data = [
            {'input': '42,33 usd', 'output': '42,33'},
            {'input': '42 usd', 'output': None},
            {'input': ' usd', 'output': None},
            {'input': ',2 usd', 'output': None},
            {'input': None, 'output': None},
            {'input': '', 'output': ''},
            {'input': '12,12,12', 'output': '12,12'},
            {'input': 124, 'output': 124},
            {'input': ['12,1'], 'output': ['12,1']},
        ]
        for data in test_data:
            result = parse_comnum(data['input'])
            self.assertEqual(result, data['output'])

    def test_remove_rnt(self):
        test_data = [
            {'input': '\tcar\nbike', 'output': 'car bike'},
            {'input': ' car   bike  ', 'output': 'car bike'},
            {'input': 'car bike', 'output': 'car bike'},
            {'input': '', 'output': ''},
            {'input': None, 'output': None},
            {'input': [], 'output': []},
            {'input': 123, 'output': 123},
        ]
        for data in test_data:
            result = remove_rnt(data['input'])
            self.assertEqual(result, data['output'])

    def test_parse_int(self):
        test_data = [
            {'input': 'today 23 hours', 'output': '23'},
            {'input': 'today 23.5', 'output': '23'},
            {'input': 'today', 'output': None},
            {'input': '', 'output': ''},
            {'input': None, 'output': None},
            {'input': 123, 'output': 123},
        ]
        for data in test_data:
            result = parse_int(data['input'])
            self.assertEqual(result, data['output'])
