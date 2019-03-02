from mapReduce.map import Mapper
from mapReduce.reduce import Reducer

import functools as ft

class Map(Mapper): 
    
    @staticmethod
    def map(key, value):
        return (key, value)

class Reduce(Reducer):
    
    @staticmethod
    def reduce(key, values):
        return key, sum(values)
