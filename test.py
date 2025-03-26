import math
import random

def calculate_radius(c):
    radius = math.sqrt(c[0]**2 + c[1]**2)
    print(radius)

cr=random.randint(1,100)
fc=calculate_radius(cr)
print(f'{fc}')