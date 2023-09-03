import sys
import math 
import random 

memory = []
n_bits_offset = 0
n_bits_tag = 0 
n_bits_indice = 0
n_hits = 0
n_misses = 0
n_misses_compulsorio = 0
n_acess = 0
n_misses_conflito = 0
n_misses_capacidade = 0
nsets = 0 
assoc = 0 
def main():
    global nsets, assoc
    '''
    if (len(sys.argv) != 7):
        print("Numero de argumentos incorreto. Utilize:")
        print("python cache_simulator.py <nsets> <bsize> <assoc> <substituição> <flag_saida> arquivo_de_entrada")
        exit(1)

    nsets = int(sys.argv[1])
    bsize = int(sys.argv[2])
    assoc = int(sys.argv[3])
    subst = sys.argv[4]
    flagOut = int(sys.argv[5])
    arquivoEntrada = sys.argv[6]
    
    print(type(nsets))

    print("nsets =", nsets)
    print("bsize =", bsize)
    print("assoc =", assoc)
    print("subst =", subst)
    print("flagOut =", flagOut)
    print("arquivo =", arquivoEntrada)
  
    '''
    #define a cache
    nsets = 16
    bsize = 2
    assoc = 8
    subst = "R"
    flagOut = 1
    arquivoEntrada = "bin_1000.bin"

    cache(nsets,assoc)
    #calcula o numero de bits
    calc_bits(nsets, bsize)
    run(arquivoEntrada, nsets,assoc)
    print_results() 

def cache(nsets, assoc): 
    global memory

    for ns in range(nsets):
        sets = []
        for ass in range(assoc):
            block = [0 ,False]
            sets.append(block)
        memory.append(sets)
    

def calc_bits(nsets,bsize): 
    global n_bits_offset ,n_bits_tag ,n_bits_indice  

    n_bits_offset =int (math.log2(bsize))
    n_bits_tag = int (math.log2(nsets))
    n_bits_indice =int (32 - n_bits_offset - n_bits_tag)
    #print(n_bits_indice)


def run(arquivoEntrada, nsets,assoc):
    global memory, n_bits_offset,n_bits_tag ,n_bits_indice ,n_hits ,n_misses ,n_misses_compulsorio, n_acess
    arquivo = open(arquivoEntrada,'rb') 
    #lemos de 4 em 4 pois o endereço é de 32 bits
    entrada = arquivo.read(4)
    while entrada: 
        n_acess += 1
        entrada_int = int.from_bytes(entrada, byteorder='big', signed=False)
        #transforma o número em um binario de 32 bits 
        endereco = format(entrada_int,'032b')
        #Obter o indice em decimal
        indice = int("".join(list(endereco[(32-n_bits_offset-n_bits_indice):32-n_bits_offset])),2) 
        #Obter a tag em decimal 
        tag = int("".join(list(endereco[:(32-n_bits_offset-n_bits_indice)])),2) 
        indice_bloco = indice % nsets
        #bloco[set][block][tag, validade]
        bloco = memory[indice_bloco]
        teste = teste_hit(tag, bloco,assoc)
        #Se tem uma posicao livre adicionamos a tag nessa posicao 
        if teste != -1 and teste != -2: 
            memory[indice_bloco][teste][0] = 1 
            memory[indice_bloco][teste][1] = tag 
        elif teste == -1: 
            posicao_retirada = random.randint(0, assoc-1)
            memory[indice_bloco][posicao_retirada][1] = tag    
        #Lê mais 4 posições
        entrada = arquivo.read(4)
      
def teste_hit(tag,bloco,assoc):
    global memory , n_hits, n_misses, n_misses_compulsorio , n_misses_conflito, n_misses_capacidade
    #contador para miss
    count_info = 0 
    #guarda a posicao livre
    posicao_livre = 0
    
    for ass in range(assoc):
        # se o bit validade for 1 e a tag for igual a buscada
        if bloco[ass][0] == 1 and bloco[ass][1] == tag:
            n_hits += 1
            return -2
        
        print(bloco[ass][0])

        if bloco[ass][0] == 1 :
            count_info = count_info + 1 
        else:
            posicao_livre = ass 

    if count_info == assoc:
        n_misses +=1      
        if full_cache():
            n_misses_capacidade += 1 
        else:  
            n_misses_conflito += 1 
        return -1
    
    else: 
        n_misses += 1 ; 
        n_misses_compulsorio += 1
        return posicao_livre 


def full_cache(): 
    global memory, nsets, assoc 

    for ns in nsets :
        for ass in assoc:
            if memory[ns][ass][0]  == 0:
                return False
    return True

def print_results(): 
    global n_acess, n_hits, n_misses,n_misses_compulsorio
    print(f'Numero de acessos {n_acess}')
    print(f'Numero de hits : {n_hits}')
    print(f'Numero de mises: {n_misses}')
    print(f'Numero de misses compulosrios : {n_misses_compulsorio}')
    print(f'Taxa de hit: {n_hits/n_acess}')


if __name__ == '__main__':
	main()	