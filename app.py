import time
import math
import json
import redis
from flask import Flask



app = Flask(__name__)
cache = redis.Redis(host='redis', port=6379)

cache.flushall()
def get_hit_count():
    retries = 5
    while True:
        try:
            return cache.incr('hits')
        except redis.exceptions.ConnectionError as exc:
            if retries == 0:
                raise exc
            retries -= 1
            time.sleep(0.5)

def calculateFactorial(number):
    if(number<1):
        return 0
    i=1
    product = 1
    while(i<=number):
        product = product * i
        i=i+1
    return(product)

@app.route('/calculationsStored')
def calculationsStored():
    String1=""   
    for key in cache.keys():
        String1+= key.decode() + "! is " + cache.get(key).decode() +" "
    return String1

@app.route('/factorial/<int(signed=True):number>')
def factorial(number):
    result = calculateFactorial(number)
    if(result==0):
        return '{}'.format(number) + " is not larger than 0\n"
    else:
        cache.set(number, '{}'.format(number) + '{}'.format(result))
        return '{}!'.format(number) + " is {}\n".format(result)

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
