import json


def get_start_urls(path_to_json: str) -> list:  # TODO: make tests
    with open(path_to_json) as file:  # TODO: if not json?
        data = json.load(file)
        return [i.get('url') for i in data]


if __name__ == '__main__':
    print(get_start_urls(
        '../../spiders/shops/ostrovshop_by/output/cats.json')[:3])
