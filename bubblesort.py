#!/usr/bin/env python3

class BubbleSort:
    def __init__(self, arr):
        self.arr = arr

    def sort(self):
        n = len(self.arr)
        for i in range(n):
            swapped = False

            for j in range(0, n - i - 1):
                if self.arr[j] > self.arr[j + 1]:
                    self.arr[j], self.arr[j + 1] = self.arr[j + 1], self.arr[j]
                    swapped = True

            if not swapped:
                break

    def display(self):
        for element in self.arr:
            print(element, end=" ")
        print()


if __name__ == "__main__":
    input_array = [64, 34, 25, 12, 22, 11, 90]
    bubble_sort = BubbleSort(input_array)
    print("Original Array:")
    bubble_sort.display()
    
    bubble_sort.sort()
    
    print("Sorted Array:")
    bubble_sort.display()


