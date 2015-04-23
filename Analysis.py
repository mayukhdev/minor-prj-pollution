#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pymongo import MongoClient
from Database import find_data
from datetime import datetime
import pprint


def main():
	q = {"date":datetime(2015,04,23,15,10)}
	find_data(q)[0]


if __name__ == '__main__':
	main()