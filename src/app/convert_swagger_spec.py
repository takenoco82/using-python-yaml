from collections import OrderedDict

import yaml


def read(path: str) -> dict:
    # OrderedDictとして読み込む
    # https://qiita.com/tkyaji/items/842840fa090fb7c6a095
    def construct_odict(loader, node):
        return OrderedDict(loader.construct_pairs(node))

    yaml.add_constructor('tag:yaml.org,2002:map', construct_odict)

    print("read")
    with open(path, "r") as f:
        spec = yaml.load(f)

    return spec


def write(path: str, spec: dict):
    # https://qiita.com/podhmo/items/aa954ee1dc1747252436
    def represent_odict(dumper, instance):
        return dumper.represent_mapping('tag:yaml.org,2002:map', instance.items())

    yaml.add_representer(OrderedDict, represent_odict)

    print("write")
    with open(path, "w") as f:
        yaml.dump(spec, f, default_flow_style=False)


def where_dict(value, filter_func=lambda: True):
    if type(value) == OrderedDict:
        filtered_keys = []

        keys = value.keys()
        for key in keys:
            print(key)
            if filter_func(key):
                where_dict(value[key], filter_func)
            else:
                # OrderedDictはイテレート中に削除できないため
                # いったんキーを保存しておき、後で削除する
                filtered_keys.append(key)

        for key in filtered_keys:
            value.pop(key)
    elif type(value) == list:
        for item in value:
            where_dict(item, filter_func)
    else:
        pass


def main():
    def delete_func(key):
        if key == "example":
            return False
        elif type(key) == str and key.startswith("x-"):
            return False
        else:
            return True

    path = "./swagger.yaml"
    spec = read(path)
    where_dict(spec, delete_func)
    write(path, spec)


if __name__ == '__main__':
    main()
