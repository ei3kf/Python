def bubblesort(a):
    for n in range(len(a)-1,0,-1):
        for i in range(n):
            if a[i]>a[i+1]:
                scratch = a[i]
                a[i] = a[i+1]
                a[i+1] = scratch

a = [3,1,5,2,9,6,8,4,7,10]
print(a)
bubblesort(a)
print(a)
