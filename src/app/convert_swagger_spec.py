from collections import OrderedDict
from logging import DEBUG, basicConfig, getLogger

import yaml

# ログ出力設定
formatter = "%(asctime)s [%(levelname)s] %(message)s"
basicConfig(level=DEBUG, format=formatter)
logger = getLogger(__name__)


def read(path: str) -> dict:
    # OrderedDictとして読み込む
    # https://qiita.com/tkyaji/items/842840fa090fb7c6a095
    def construct_odict(loader, node):
        return OrderedDict(loader.construct_pairs(node))

    yaml.add_constructor('tag:yaml.org,2002:map', construct_odict)

    with open(path, "r") as f:
        spec = yaml.load(f)

    return spec


def write(path: str, spec: dict):
    # https://qiita.com/podhmo/items/aa954ee1dc1747252436
    def represent_odict(dumper, instance):
        return dumper.represent_mapping('tag:yaml.org,2002:map', instance.items())

    yaml.add_representer(OrderedDict, represent_odict)

    with open(path, "w") as f:
        yaml.dump(spec, f, default_flow_style=False)


def filter_dict(value, where_func=lambda: True):
    if type(value) == OrderedDict:
        excluded_keys = []

        keys = value.keys()
        for key in keys:
            logger.debug("key={}".format(key))
            if where_func(key):
                filter_dict(value[key], where_func)
            else:
                # OrderedDictはイテレート中に削除できないため
                # いったんキーを保存しておき、後で削除する
                excluded_keys.append(key)

        for key in excluded_keys:
            value.pop(key)
    elif type(value) == list:
        for item in value:
            filter_dict(item, where_func)


def main():
    def where_func(key):
        if key == "example":
            return False
        elif type(key) == str and key.startswith("x-"):
            return False
        else:
            return True

    path = "./swagger.yaml"
    spec = read(path)
    filter_dict(spec, where_func)
    write(path, spec)


if __name__ == '__main__':
    main()
