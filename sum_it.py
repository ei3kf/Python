#!/usr/bin/env python3

'''
Quick dirty script that takes 3 numbers, and prints the highest two and the value of the two added.
'''

def sum_it(a,b,c):
  i = [a,b,c]
  print(i)
  i.sort()
  print(i)
  high1 = i[-1]
  high2 = i[-2]
  high_sum = high1 + high2
  print(high1, high2, high_sum)

sum_it(3,18,1946)
