from mapReduce.map import Mapper
from mapReduce.reduce import Reducer

class Map(Mapper): 
    
    @staticmethod
    def map(key, value):
        return (key*2, value*2)

class Reduce(Reducer):
    
    @staticmethod
    def reduce(key, values):
        return key, reduce(lambda x,y: x + y, values)

print("*"*200)