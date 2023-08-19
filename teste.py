'''
with open('bin_100.bin', 'rb') as file:
    n_bits_ofsset = 2
    entrada = file.read(4)
    number = int.from_bytes(entrada, byteorder='big', signed=False)
    endereco = format(number, '032b')
    offest = endereco[32-n_bits_ofsset:32]
    print(offest)
'''

mem = []

assoc = []
aux = [0, 1]
aux2 = [1,2]
assoc.append(aux)
assoc.append(aux2)
mem.append(assoc)
print(mem[0][1][0])
