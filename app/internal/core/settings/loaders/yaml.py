import yaml


def notimplemented_constructor(loader, node):
    """
    :param loader:  yaml.Loader
    :param node:  yaml.nodes.Node
    :return: NotImplemented
    """
    if node.tag == '!secret':
        return NotImplemented


def __load_yaml(path: str) -> dict:
    with open(path, encoding='utf-8') as f:
        yaml.add_constructor('!secret', notimplemented_constructor)
        d = yaml.load(f, Loader=yaml.FullLoader)
    return d
