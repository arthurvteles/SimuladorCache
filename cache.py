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

def main():
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

    cache(nsets,assoc)
    calc_bits(nsets, bsize)
    run(arquivoEntrada, nsets,assoc)


if __name__ == '__main__':
	main()


def cache(nsets, assoc):
    global memory 

    for ns in nsets:
        sets = []
        for ass in assoc:
            block = []
            #bit validade, tag
            block.append([0, None])
	    
        sets.append(block)
        memory.append(sets)
    
def calc_bits(nsets, bsize): 
    global n_bits_offset ,n_bits_tag ,n_bits_indice  

    n_bits_offset =int (math.log2(bsize))
    n_bits_tag = int (math.log2(nsets))
    n_bits_indice =int (32 - n_bits_offset - n_bits_tag)

def run(arquivoEntrada, n_sets,assoc):
     
    global memory, n_bits_offset,n_bits_tag ,n_bits_indice ,n_hits ,n_misses ,n_misses_compulsorio, n_acess

    arquivo = open(arquivoEntrada,'rb') 
    #lemos de 4 em 4 pois o endereço é de 32 bits
    entrada = arquivo.read(4)
    while entrada: 
        n_acess += 1 
        #converte cada linha em um inteiro 
        entrada_int = int.from_bytes(entrada, byteorder='big', signed=False)
        #transforma o número em um binario de 32 bits 
        endereco = format(entrada_int,'032b')
        #Obter o offset 
        offset = endereco[32-n_bits_offset:32]
        #Obter o indice
        index = endereco[32-n_bits_offset-n_bits_indice:32-offset]
        #Obter a tag 
        tag = endereco[:32-offset-index]
        #Seleciona o index na memoria
        index_mem = int(index) % n_sets
        #pega 
        bloco = memory[index_mem]
        #testa se é hit:
        teste = test_hit(tag,bloco,assoc)
        #Se tem uma posicao livre adicionamos a tag nessa posicao 
        if teste != -1 and teste != -2: 
            memory[index_mem][teste][0] = 1 
            memory[index_mem][teste][1] = tag 
        elif teste == -1: 
            posicao_retirada = random.randint(0, assoc)
            memory[index][posicao_retirada] = tag     
        #Lê mais 4 posições 
        entrada = arquivo.read(4)

        
#testa hit (retorna -2 se hit, -1 miss compulsorio e retorna posicao vazias miss normal)
def test_hit(tag,bloco,assoc ):
    global memory , n_hits, n_misses, n_misses_compulsorio 
    count_info = 0 
    posicao_livre = 0
    for ass in range(assoc):
        # se o bit validade for 1 e a tag for igual a buscada
        if bloco[ass][0] == 1 and bloco[ass][1] == tag:
            n_hit += 1 
            return -2
        elif bloco[ass][0] == 1: 
            count_info += 1 
        else: 
            posicao_livre = ass 
    
    if count_info == assoc:
        n_misses_compulsorio +=1 
        return -1
    else: 
        n_misses +=1 
        return posicao_livre 
    
    
            
    

	