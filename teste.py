with open('bin_100.bin', 'rb') as file:
    data = file.read()
    print(data) 

for i in range(len(data)):
    print(data[i])