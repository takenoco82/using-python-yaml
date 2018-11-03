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


def where_dict(value):
    if type(value) == OrderedDict:
        delete_targets = []

        keys = value.keys()
        for key in keys:
            print(key)
            # example の削除
            if key == "example":
                delete_targets.append(key)
            # 「x-○○」の削除
            elif type(key) == str and key.startswith("x-"):
                delete_targets.append(key)
            where_dict(value[key])

        for target in delete_targets:
            value.pop(target)
    elif type(value) == list:
        for item in value:
            where_dict(item)
    else:
        pass


def main():
    path = "./swagger.yaml"
    spec = read(path)
    where_dict(spec)
    write(path, spec)


if __name__ == '__main__':
    main()
