from typing import List
from collections import deque
from time import time
from math import inf
from random import choice
from random import random
from operator import itemgetter

class Vertice:
    def __init__(self, num: int) -> None:
        """
        inicialização dos vértices:
        num representa o número do vértice
        adj representa a lista de adjacência do vértice
        """
        self.num = num
        self.adj: List[Vertice] = []
        self.pai = None
        self.rank = 0

    def __str__(self) -> str:
        return "%d" % (self.num)

class Grafo:
    """
    Representação de um grafo não-orientado
    """
    def __init__(self, n: int) -> None:
        """
        Atributos do grafo
        """
        self.vertices = [Vertice(i) for i in range(n)]
        self.quantidadearestas = 0
        self.arestas = []
        """
        Neste grafo temos uma matriz de adjacências para armazenar
        os pesos das arestas adicionadas ao grafo.
        """
    def addArestas(self, u: int, v: int, w):
        self.vertices[u].adj.append(self.vertices[v])
        self.vertices[v].adj.append(self.vertices[u])
        self.arestas.append([u, v, w])
        self.quantidadearestas += 1

    """
    O BFS foi implementado para que possa ser chamado na função Diametro().
    Em Diametro(), o BFS aqui é utilizado para encontrar o vértice que está 
    mais longe da raíz do grafo e também calcula esta distância.
    """

    def BFS(self, s):
        fila = deque()
        for v in self.vertices:
            v.d = inf
            v.visitado = False
        self.vertices[s].d = 0
        self.vertices[s].visitado = True
        fila.appendleft(self.vertices[s])
        while fila:
            u = fila.popleft()
            res = u.num
            for v in u.adj:
                if v.visitado == False:
                    v.d = u.d + 1
                    fila.append(v)
                    v.visitado = True
        for v in self.vertices:
            if v.num == res:
                return v.num, v.d  # Retorna o Vértice mais distante e sua distância


    """
    O DFS foi implementado para ser utilizado na função is_arvore().
    Uma maneira de descobrir se um grafo é ou não uma árvore, é preenchendo
    esses dois requisitos:
    1- A quantidade de arestas deve ser menor que a quantidade de vértices menos 1.
    Isso porque se a quantidade de arestas for maior do que isso, é impossível fazer
    um grafo sem ciclo (um ciclo descaracterizaria a árvore).
    2- Um vértice qualquer u pode ser acessado por qualquer outro vértice do grafo.
    Isso quer dizer, todos os vértices são alcançáveis através de todos os vértices.

    Primeiramente, saber se o primeiro requisito foi preenchido é fácil, pois pode-se
    incrementar 1 no atributo grafo.quantidadearestas cada vez que uma aresta é
    adicionada.
    Entretanto, para satisfazer o segundo requisito é necessário realizar uma operação
    de busca, como o DFS, no grafo e, adicionando cada vértice que foi visitado
    no set "visitados", conseguimos distinguir os vértices alcançáveis dos
    não-alcançáveis em um grafo. Assim, por fim, basta verificar se o set visitados possui
    o mesmo número de elementos da lista de vértices do grafo. Caso algum vértice não 
    tenha sido visitado, este grafo não é uma árvore, já que um vértice não pôde ser acessado.
    """

    def DFS(self, s, visitados):
        visitados.add(s)
        for u in self.vertices[s].adj:
            if u.num not in visitados:
                self.DFS(u.num, visitados)

    def is_arvore(self):
        if self.quantidadearestas != (len(self.vertices)-1):
            #print("\nO grafo não é uma árvore, portanto não pode ter o diâmetro medido")
            return False
        visitados = set()
        s = choice(self.vertices)
        self.DFS(s.num, visitados)
        return len(visitados) == len(self.vertices)

    def Diametro(self):
        if not self.is_arvore():
            return
        s = choice(self.vertices)
        a, d1 = self.BFS(s.num)
        b, d2 = self.BFS(a)
        #print("\nO diâmetro da árvore é %d" % d2)
        return d2

    """
    Em MSTKruskal, o primeiro passo dado é criar um set (conjunto disjunto) para cada vértice do grafo. 
    Após isso, as arestas do grafo são ordenadas em ordem não decrescente de acordo com seus pesos.
    Então, as arestas ordenadas são percorridas enquanto a árvore não se completa e, se o vértice
    de saída da aresta estiver em um set diferente do set do vértice de entrada, essa aresta é
    adicionada no conjunto que é retornado e é feita a união dos sets dos vértices. 
    """

    def MSTKruskal(self):
        A = []
        for v in self.vertices:
            MakeSet(v)
        self.arestas.sort(key=itemgetter(2))
        qarestas = 0
        while qarestas < len(self.vertices)-1:
            for aresta in self.arestas:
                    if FindSet(self.vertices[aresta[0]]) != FindSet(self.vertices[aresta[1]]):
                        A.append([aresta[0], aresta[1], aresta[2]])
                        Union(self.vertices[aresta[0]], self.vertices[aresta[1]])
                        qarestas += 1
        return A

"""
As 4 funções abaixo são os procedimentos utilizados para criar sets
(conjuntos disjuntos) para os vértices do grafo. Os sets são utilizados
em MSTKruskal, para verificar se uma aresta é ou não segura para ser
adicionada à árvore.
"""

def MakeSet(v):
    v.pai = v
    v.rank = 0

def FindSet(v):
    if v != v.pai:
        v.pai = FindSet(v.pai)
    return v.pai

def Link(u, v):
    if u.rank > v.rank:
        v.pai = u
    else:
        u.pai = v
        if u.rank == v.rank:
            v.rank += 1

def Union(vertice1, vertice2):
    Link(FindSet(vertice1), FindSet(vertice2))

"""
O procedimento RandomTreeKruskal constrói uma árvore percorrendo um grafo completo
com arestas de pesos inteiros aleatórios entre 0 e 1. Então, calcula a minimum
spanning tree deste grafo com o procedimento MSTKruskal e por fim
retorna um grafo contendo apenas as arestas encontradas no MSTKruskal.
"""

def RandomTreeKruskal(n):
    g = Grafo(n)
    g.arestas = [[u, v, random()] for u in range(n) for v in range(u+1, n)]
    #print(g.arestas)
    A = g.MSTKruskal()
    #print(A)
    g.arestas = []
    for aresta in A:
        g.addArestas(aresta[0], aresta[1], aresta[2])
    return g

"""
O procedimento RandomTreeRandomWalk constrói uma árvore aleatória
percorrendo o grafo também aleatoriamente. Para isso, inicalmente é criado um set
para armazenar todos os vértices do grafo que forem visitados. Então, um vértice u
aleatório é escolhido no grafo e colocado no set "visitado". Assim, para construir
a árvore, um vértice novo é escolhido e verifica-se se ele já foi visitado. Caso sim,
o procedimento continua a buscar por um vértice que ainda não tenha sido visitado.
Caso não, ele é marcado como visitado e adiciona-se uma aresta entre o último vértice
verificado e ele. O procedimento é repetido enquanto a quantidade de arestas no grafo
seja menor que o número de vértices que o grafo tem menos 1 (pré-requisito para que
um grafo seja considerado uma árvore). 
"""

def RandomTreeRandomWalk(n):
    G = Grafo(n)
    for v in G.vertices:
        v.visitado = False
    u = choice(G.vertices)
    u.visitado = True
    while G.quantidadearestas < n - 1:
        v = choice(G.vertices)
        if not v.visitado:
            G.addArestas(u.num, v.num, 0)
            v.visitado = True
        u = v
    return G

"""
Como pedido na especificação do trabalho, são calculados os resultados
dos diâmetros de árvores geradas pelo RandomTreeRandomWalk e uma média
de todas as 500 iterações para cada quantidade de vértices (250, 500, 750,
1000, 1250, 1500, 1750 e 2000) é feita para que os resultados sejam plottados
e testados pelo programa plot.py passado via Classroom.
"""

def testeRTRW():
    with open("randomwalk.txt", "w") as file:
        soma = [0] * 9
        for i in range(500):
            for j in range(250, 2001, 250):
                T = RandomTreeRandomWalk(j)
                ind = j // 250
                soma[ind] += T.Diametro()
            print(i + 1)
        for i in range(1, 9):
            soma[i] /= 500
            file.write(f"{i * 250} {soma[i]}\n")

"""
Como pedido na especificação do trabalho, são calculados os resultados
dos diâmetros de árvores geradas pelo RandomTreeKruskal e uma média
de todas as 500 iterações para cada quantidade de vértices (250, 500, 750,
1000, 1250, 1500, 1750 e 2000) é feita para que os resultados sejam plottados
e testados pelo programa plot.py passado via Classroom.
"""

def testeRTK():
    with open("kruskal.txt", "w") as file:
        soma = [0] * 9
        for i in range(500):
            for j in range(250, 2001, 250):
                T = RandomTreeKruskal(j)
                ind = j // 250
                soma[ind] += T.Diametro()
                #print(j)
            print(i + 1)
        for i in range(1, 9):
            soma[i] /= 500
            file.write(f"{i * 250} {soma[i]}\n")

"""
As funções abaixo foram feitas pra calcular o tempo puro dos procedimentos,
sem influência do tempo levado para abrir e escrever nos arquivos e calcular
os diâmetros e as médias
"""

def RTK():
    for i in range(1):
        for j in range(250, 2001, 250):
            T = RandomTreeKruskal(j)
            print(T.Diametro())

def RTRW():
    for i in range(1):
        for j in range(250, 2001, 250):
            T = RandomTreeRandomWalk(j)
            #print(T.Diametro())

def Parte1():
    """
    Parte 1 do trabalho. Apenas criação de 3 grafos e verificação se
    são ou não árvores e cálculo dos diâmetros dos grafos que são árvore
    """
    g = Grafo(6)
    g.addArestas(0, 1, 0)
    g.addArestas(0, 2, 0)
    g.addArestas(0, 3, 0)
    g.addArestas(0, 4, 0)
    g.addArestas(0, 5, 0)
    assert g.Diametro() == 2
    h = Grafo(7)
    h.addArestas(0, 1, 0)
    h.addArestas(0, 5, 0)
    h.addArestas(1, 3, 0)
    h.addArestas(5, 2, 0)
    h.addArestas(5, 6, 0)
    h.addArestas(1, 4, 0)
    h.addArestas(6, 4, 0)
    assert h.Diametro() == None
    i = Grafo(7)
    i.addArestas(0, 1, 0)
    i.addArestas(0, 5, 0)
    i.addArestas(1, 3, 0)
    i.addArestas(5, 2, 0)
    i.addArestas(5, 6, 0)
    i.addArestas(1, 4, 0)
    assert i.Diametro() == 4

"""
Abaixo segue dois testes de verificação do MST-Kruskal implementado. 
São criados dois grafos que formam ciclos e com arestas que tem pesos diferentes.
Após implementar o MST-Kruskal nos grafos, são feitos três testes: 1- Se o conjunto
de arestas da árvore encontrada é realmente o esperado; 2- Se o grafo formado realmente
é uma árvore; 3- Se o peso total da árvore encontrada é o esperado.
"""

def testeMSTKruskal():
    G = Grafo(5)
    G.arestas = [[0, 1, 0.5], [1, 2, 1], [0, 2, 0.1], [3, 1, 0.4], [4, 2, 1], [4, 3, 1]]
    A = G.MSTKruskal()
    G.arestas = []
    pesototaldografo = 0
    for aresta in A:
        pesototaldografo += aresta[2]
        G.addArestas(aresta[0], aresta[1], aresta[2])
    assert G.arestas == [[0, 2, 0.1], [3, 1, 0.4], [0, 1, 0.5], [4, 2, 1]]
    assert G.is_arvore() == True
    assert pesototaldografo == 2
    F = Grafo(6)
    F.arestas = [[0, 1, 1], [1, 2, 0.3], [0, 2, 0.1], [3, 1, 1], [4, 2, 0.7], [4, 3, 0.5], [5, 0, 1], [5, 2, 0.4]]
    A = F.MSTKruskal()
    F.arestas = []
    pesototaldografo = 0
    for aresta in A:
        pesototaldografo += aresta[2]
        F.addArestas(aresta[0], aresta[1], aresta[2])
    assert F.arestas == [[0, 2, 0.1], [1, 2, 0.3], [5, 2, 0.4], [4, 3, 0.5], [4, 2, 0.7]]
    assert F.is_arvore() == True
    assert pesototaldografo == 2


def main():
    t1 = time()
    Parte1()
    RTRW() #Parte 2
    RTK() #Parte 3
    testeMSTKruskal()
    #testeRTRW()
    #testeRTK()
    t2 = time()
    ttotal = t2 - t1
    print("O tempo total de execução foi %f" % ttotal)

if __name__ == '__main__':
    main()
