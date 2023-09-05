# SimuladorCache

### Repositório desenvolvido pro segundo trabalho prático de AOC II.

### Objetivos 🎯

-   Deverá ser implementado um simulador funcional de caches em uma linguagem de programação (livre escolha), este simulador deverá ser parametrizável (configurações da cache), quanto ao número de
    conjuntos, tamanho do bloco, nível de associatividade e política de substituição. Considere que a cache é endereçada à bytes e o endereço possui 32 bits.
-   A configuração de cache deverá ser repassada por linha de comando e formatada com os seguintes
    parâmetros (o arquivo de entrada poderá ter extensão):

-    cache_simulator 'nsets' 'bsize' 'assoc' 'substituição' 'flag_saida' 'arquivo_de_entrada'

-   Onde cada um destes campos possui o seguinte significado:
    -   cache_simulator - nome do arquivo de execução principal do simulador (todos devem usar este
        nome, independente da linguagem escolhida);
    -   nsets - número de conjuntos na cache (número total de “linhas” ou “entradas” da cache);
    -   bsize - tamanho do bloco em bytes;
    -   assoc - grau de associatividade (número de vias ou blocos que cada conjunto possui);
    -   substituição - política de substituição, que pode ser Random (R), FIFO (F) ou L (LRU);
    -   flag_saida - flag que ativa o modo padrão de saída de dados;
    -   arquivo_de_entrada - arquivo com os endereços para acesso à cache.

### Tecnologias Utilizadas 💻

| Python |
| ------ |
| 3.11.4 |

### Rodando o projeto ▶️

-   Deve-se abrir o terminal na pasta do projeto e utilizar o seguinte comando:

    python3 cache_simulator.py 'nsets' 'bsize' 'assoc' 'substituição' 'flag_saida' 'arquivo_de_entrada'

-   Substituindo <'nsets' 'bsize' 'assoc' 'substituição' 'flag_saida' 'arquivo_de_entrada'> pelos valores desejados.

### Observações 🚩

-   Integrantes: Arthur Teles e Mauricio Mucci 🤝
-   Foram implementados dois algoritmos de substituição: Random e FIFO
