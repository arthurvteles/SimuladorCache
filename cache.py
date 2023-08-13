import sys
from math import log2

memory = []
n_bits_offset = 0
n_bits_tag = 0 
n_bits_indice = 0


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



    print("nsets =", nsets)
    print("bsize =", bsize)
    print("assoc =", assoc)
    print("subst =", subst)
    print("flagOut =", flagOut)
    print("arquivo =", arquivoEntrada)

    cache(nsets,assoc)
    calc_bits(nsets, bsize)

	



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

    n_bits_offset = math.log2(bsize)
    n_bits_tag = math.log2(nsets)
    n_bits_indice = 32 - n_bits_offset - n_bits_tag



    
	    


	