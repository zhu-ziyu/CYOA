import tkinter as tk
import json
import random
import threading
import time
import os

getaway_vehicle = True
getaway_fly = True
def Enter():
    print("Enter from the side door")

def walk():
    Enter()

def vehicle():
    if getaway_vehicle:
        Enter()
    else:
        print("you can not do this you did not buy the vehicle")

vehicle()

def fly():
    if getaway_fly:
        Enter()
    else:
        print("you can not do this you did not buy the fly")

vehicle()

def naboo():

        print("\nThe action begins")
        print("\nYou have two choices")
        print("-" * 20)
        print("'walk' - Approached by walking (---VP)")
        print("'vehicle' - Approach via land vehicle (--VP)")
        print("'fly' - Approach via flying vehicle(-VP)")
        command = input('\nPlease enter your choice: ')
        if command == 'walk':
            walk()

        elif command == 'vehicle':
            vehicle()

        elif command == 'fly':
            fly()

        else:
            print("Hmmm that choice doesn't exist, try again.")
            naboo()

