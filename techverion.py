import tkinter as tk
import json
import random
import threading
import time
import os

def gungan_city():
    print(1+1)
def royal_palace():
    print(1+2)
def naboo():
    print("\nWhenyou get to Naboo you are welcomed by two members of the Naboo Royal Security Force ... ")
    print("\nYou have two choices")
    print("-"*20)
    print("'City' -to go to the Gungan city")
    print("'Palace' -to go to the Royal Palace")
    command = input('\nPlease enter your choice.')
    if command == 'city':
        gungan_city()
    elif command == 'palace':
        royal_palace()
    else:
        print('Hmmm that choice doesnt exist, try again.')
naboo()