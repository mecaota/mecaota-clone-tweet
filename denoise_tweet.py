# -*- coding: utf-8 -*-
import pandas
import numpy
import sys

args = sys.argv
tweets = pandas.read_csv(args[1],encoding="utf-8")
print(tweets)