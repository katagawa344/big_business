import timeit
start = timeit.default_timer()
myfile = open('test.txt','w')
with open("HIV3 week3.txt","r") as splitfile:
    for columns in [line.split("\t") for line in splitfile]:
       myfile.write(' '.join(columns))




myfile.close()


stop = timeit.default_timer()
print(stop - start) 