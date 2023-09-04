import sys
import math 
import random 

from decimal import *

# Informações da cache
memory = []
n_bits_offset = 0
n_bits_tag = 0 
n_bits_index = 0
nsets = 0 
bsize = 0
assoc = 0
subst = 'R' 
flag_out = 1
input_file = ' '

# Informações do BenchMark
n_hits = 0
n_acess = 0
n_misses = 0
n_misses_conflict = 0
n_misses_capacity = 0
n_misses_cold_start = 0

def main():
    global nsets, bsize, assoc, subst, flag_out, input_file

    if (len(sys.argv) != 7):
        print("Número de argumentos incorreto! Utilize:")
        print("python cache_simulator.py <nsets> <bsize> <assoc> <substituição> <flag_saida> arquivo_de_entrada")
        exit(1)

    nsets = int(sys.argv[1])
    bsize = int(sys.argv[2])
    assoc = int(sys.argv[3])
    subst = sys.argv[4]
    flag_out = int(sys.argv[5])
    input_file = sys.argv[6]

    build_cache()
    run()
    if flag_out == 0:
        print_no_pattern()
    else:
        print_pattern()

def build_cache(): 
    global memory, nsets, assoc

    for ns in range(nsets):
        sets = []
        for ass in range(assoc):
            block = [0 ,False]
            sets.append(block)
        memory.append(sets)
    

def calc_bits(): 
    global nsets, bsize, n_bits_offset, n_bits_tag, n_bits_index

    n_bits_offset = int(math.log2(bsize))
    n_bits_index = int(math.log2(nsets))
    n_bits_tag = int(32 - n_bits_offset - n_bits_tag)


def run():
    global input_file, nsets, assoc, memory, n_bits_offset, n_bits_tag, n_bits_index, n_hits, n_misses, n_misses_cold_start, n_acess
    arquivo = open(input_file,'rb') 
    #lemos de 4 em 4 pois é endereçaca a byte
    entrada = arquivo.read(4)
    while entrada: 
        n_acess += 1
        entrada_int = int.from_bytes(entrada, byteorder='big', signed=False)
        #transforma o número em um binario de 32 bits 
        endereco = format(entrada_int,'032b')
        
        # Calcula offset, index e tag.
        calc_bits()
        
        #Obter o indice em decimal
        reference = int("".join(list(endereco[(32-n_bits_offset-n_bits_index):32-n_bits_offset])),2) 
        #Obter a tag em decimal 
        tag = int("".join(list(endereco[:(32-n_bits_offset-n_bits_index)])),2) 
        index = reference % nsets
        #bloco[set][block][tag, validade]
        set = memory[index]
        teste = teste_hit(tag, set, assoc)
        #Se tem uma posicao livre adicionamos a tag nessa posicao 
        if teste != -1 and teste != -2: 
            memory[index][teste][0] = 1 
            memory[index][teste][1] = tag 
        elif teste == -1: 
            posicao_retirada = random.randint(0, assoc-1)
            memory[index][posicao_retirada][1] = tag    
        #Lê mais 4 posições
        entrada = arquivo.read(4)
      
def teste_hit(tag,bloco,assoc):
    global memory , n_hits, n_misses, n_misses_cold_start , n_misses_conflict, n_misses_capacity
    #contador para miss
    count_info = 0 
    #guarda a posicao livre
    posicao_livre = 0
    
    for ass in range(assoc):
        # se o bit validade for 1 e a tag for igual a buscada
        if bloco[ass][0] == 1 and bloco[ass][1] == tag:
            n_hits += 1
            return -2
        if bloco[ass][0] == 1 :
            count_info = count_info + 1 
        else:
            posicao_livre = ass 

    if count_info == assoc:
        n_misses +=1      
        if full_cache():
            n_misses_capacity += 1 
        else:  
            n_misses_conflict += 1 
        return -1
    else: 
        n_misses += 1 ; 
        n_misses_cold_start += 1
        return posicao_livre 


def full_cache(): 
    global memory, nsets, assoc 

    for ns in range(nsets) :
        for ass in range(assoc):
            if memory[ns][ass][0] == 0:
                return False
    return True

def print_no_pattern(): 
    global n_acess, n_hits, n_misses, n_misses_cold_start, n_misses_capacity, n_misses_conflict
    
    print('[NÚMEROS]')
    print(f'Acessos: {n_acess}')
    print(f'Acertos: {n_hits}')
    print(f'Faltas: {n_misses}')
    print(f'Faltas compulsórias: {n_misses_cold_start}')
    print(f'Faltas por capacidade: {n_misses_capacity}')
    print(f'Faltas por conflito: {n_misses_conflict}')

    print('[TAXAS]')
    print(f'Acertos : {(n_hits/n_acess):.4f}')
    print(f'Faltas: {(n_misses/n_acess):.4f}')
    print(f'Faltas compulsórias : {(n_misses_cold_start/n_misses):.2f}')
    print(f'Faltas por capacidade : {(n_misses_capacity/n_misses):.2f}')
    print(f'Faltas por conflito : {(n_misses_conflict/n_misses):.2f}')

def print_pattern(): 
    global n_acess, n_hits, n_misses, n_misses_cold_start, n_misses_capacity, n_misses_conflict
    
    hit_rate = n_hits/n_acess
    miss_rate = n_misses/n_acess
    cold_start_rate = n_misses_cold_start/n_misses
    capacity_rate = n_misses_capacity/n_misses
    conflict_rate = n_misses_conflict/n_misses

    print('{}, {:.4f}, {:.4f}, {:.2f}, {:.2f}, {:.2f}'
          .format(n_acess, hit_rate, miss_rate, cold_start_rate, capacity_rate, conflict_rate))

if __name__ == '__main__':
	main()	