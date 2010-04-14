#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys

from kargoxml import add_column


if __name__ == '__main__':
    args = sys.argv

    if len(args) != 2:
        print("Usage: python %s [limit]") % __file__
        sys.exit()

    add_column(args[-1])
