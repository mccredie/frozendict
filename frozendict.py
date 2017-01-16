#!/usr/bin/env python3

from enum import Enum
from collections import namedtuple, Mapping

class RBColor(Enum):
    black = False
    red = True

class RBNode(namedtuple("RBNode", "key value left right color")):
    __slots__ = ()
    def __new__(cls, key, value, left=None, right=None, color=RBColor.black):
        return super(RBNode, cls).__new__(cls, key, value, left, right, color)

    def rotate_left(self):
        new = self._replace(right=self.right.left, color=RBColor.red)
        return self.right._replace(left=new, color=self.color)

    def rotate_right(self):
        new = self._replace(color=RBColor.red, left=self.left.right)
        return self.left._replace(right=new, color=self.color)

    def flip_colors(self):
        return self._replace(
            color=not self.color,
            left=self.left._replace(color=not self.left.color),
            right=self.right._replace(color=not self.right.color))

    def insert(self, key, value):
        return insert(self, key, value)

    def search(self, key):
        x = self
        while x is not None:
            if key == x.key:
                return x.value
            elif key < x.key:
                x = x.left
            elif key > x.key:
                x = x.right
        raise KeyError(key)

def iter_keys(h):
    if h is None:
        return
    yield from iter_keys(h.left)
    yield h.key
    yield from iter_keys(h.right)

def insert(h, key, value):
    if h is None:
        h = RBNode(key, value)

    if is_red(h.left) and is_red(h.right):
        h = h.flip_colors()

    if key == h.key:
        h = h._replace(value=value)
    elif key < h.key:
        h = h._replace(left=insert(h.left, key, value))
    else:
        h = h._replace(right=insert(h.right, key, value))

    if is_red(h.right) and not is_red(h.left):
        h = h.rotate_left()
    if is_red(h.left) and is_red(h.left.left):
        h = h.rotate_right()

    return h

def node_len(node):
    if node is None:
        return 0
    return 1 + node_len(node.left) + node_len(node.right)

def is_red(node):
    return node and node.color

def node_to_str(node, prefix=""):
    if node is None:
        return prefix + '-\n'

    return "".join([
        prefix, "key: ", str(node.key), "\n",
        prefix, "value: ", str(node.value), "\n",
        prefix, "left:", "\n",
        node_to_str(node.left, prefix + "  "),
        prefix, "right:", "\n",
        node_to_str(node.right, prefix + "  "),
    ])

class FrozenDict(Mapping, tuple):
    """ A frozen dictionary implementation that is based on an immutable left
    leaning red black tree implementation.
    """
    __slots__ = ()
    def __new__(cls, *args, **kwds):
        if len(args) > 1:
            raise TypeError('update expected at most 1 arguments, got %d' %
                            len(args))
        root = None
        if args:
            other = args[0]
            if isinstance(other, FrozenDict):
                root = other._root
            elif isinstance(other, Mapping):
                for key in other:
                    root = insert(root, key, other[key])
            elif hasattr(other, "keys"):
                for key in other.keys():
                    root = insert(root, key, other[key])
            else:
                for key, value in other:
                    root = insert(root, key, value)
        for key, value in kwds.items():
            root = insert(root, key, value)

        return tuple.__new__(cls, (root,))

    @property
    def _root(self):
        return tuple.__getitem__(self, 0)

    def __getitem__(self, key):
        return self._root.search(key)

    def __iter__(self):
        return iter_keys(self._root)

    def __len__(self):
        return node_len(self._root)

    def __repr__(self):
        return ", ".join(
                "{0!r}: {1!r}".format(k, v) for k, v in self.items()).join((
                    "FrozenDict({", "})"))


# TODO
#  - add something like update to FrozenDict
#  - add some sort of delete method for removing keys
#  - check performance and make insert more performant
#  - add more efficent __eq__ method


if __name__ == "__main__":
    entries = [
        (0, "root"),
        (1, "words"),
        (4, "blah"),
        (2, "goop"),
        (-1, "ham"),
        (100, "eggs")
    ]

    d = FrozenDict(entries)

    for k, v in d.items():
        print(k, ":", v)

    print("keys: ", ", ".join(str(k) for k in d.keys()))



