from nanoleaf import Aurora
import sys
from time import sleep

my_aurora = Aurora("192.168.0.10", "SYNhmvk39Qbcx1ZqGqBvS7mEq4fvx6Zv")
while my_aurora.on:
        print('Waiting until effects are over')
        sleep(1)
my_aurora.on = True
my_aurora.brightness = 70
my_aurora.effect = sys.argv[1]
sleep(5)
my_aurora.on = False
