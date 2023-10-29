from collections import deque
import random

class Rede:
    def __init__(self, num_vertices, fonte, sumidouro):
        '''
        Estrutura de uma rede, contendo sua lista de adjacências,
        fonte, sumidouro, numero de vértices e um dicionario que
        terá como chave um par de vértices (aresta) e servirá para
        armazenar as capacidades entre esses vértices.
        '''
        self.G = [[] for _ in range(num_vertices)]
        self.s = fonte
        self.t = sumidouro
        self.num = num_vertices
        self.capacidade = {}

    def __repr__(self):
        '''
        Ao referenciar uma rede em uma função para imprimi-la,
        será mostrada a capacidade de cada aresta.
        '''
        print("\nCapacidades da Rede:")
        res = ''
        for (u, v), c in self.capacidade.items():
            res += f'({u}, {v}): {c}\n'
        return res



def calcula_fluxos(rede, fluxo):
    '''
    Função que calcula os fluxos de entrada e saída
    de cada vértice presente na rede. Essa função
    é criada para ser utilizada na verificação de
    validade do fluxo para uma rede, já que um dos
    requisitos para que a validade seja verdadeira é
    que o fluxo de entrada de um vértice deve ser o
    mesmo que o fluxo de saída dele mesmo.
    '''
    fxtotalentrada = [0] * rede.num
    fxtotalsaida = [0] * rede.num
    for (u, v) in fluxo:
        fxtotalentrada[v] += fluxo[(u, v)]
        fxtotalsaida[u] += fluxo[(u, v)]

    return fxtotalentrada, fxtotalsaida

def teste_calcula_fluxos():
    '''
    Método para testar a função calcula_fluxos,
    utilizando a rede da figura 26.1(a) do CLRS.
    '''
    s, v1, v2, v3, v4, t = list(range(6))

    rede = cria_rede(6, s, t)

    addAresta(rede, s, v1, 16)
    addAresta(rede, s, v2, 13)
    addAresta(rede, v1, v3, 12)
    addAresta(rede, v2, v1, 4)
    addAresta(rede, v3, v2, 9)
    addAresta(rede, v2, v4, 14)
    addAresta(rede, v3, t, 20)
    addAresta(rede, v4, v3, 7)
    addAresta(rede, v4, t, 4)

    fluxo = {}
    fluxo[(s, v1)] = 11
    fluxo[(s, v2)] = 3
    fluxo[(v1, v3)] = 12
    fluxo[(v2, v1)] = 1
    fluxo[(v2, v4)] = 2
    fluxo[(v3, t)] = 12
    fluxo[(v4, t)] = 2

    fluxo1 = {}
    fluxo1[(s, v1)] = 5
    fluxo1[(s, v2)] = 3
    fluxo1[(v1, v3)] = 5
    fluxo1[(v2, v4)] = 3
    fluxo1[(v3, t)] = 5
    fluxo1[(v4, t)] = 2

    assert calcula_fluxos(rede, fluxo) == ([0, 12, 3, 12, 2, 14], [14, 12, 3, 12, 2, 0])
    assert calcula_fluxos(rede, fluxo1) == ([0, 5, 3, 5, 3, 7], [8, 5, 3, 5, 2, 0])


def cria_rede(tam: int, fonte: int, sumid: int):
    '''
    Dados uma quantidade de vértices, uma fonte e
    um sumidouro, é criada uma rede com esses
    parâmetros.
    '''
    rede = Rede(tam, fonte, sumid)
    return rede


def addAresta(rede, u: int, v: int, w: int):
    '''
    Função para adicionar uma aresta à rede. O método
    adiciona o vértice em que a aresta entra à lista
    de adjacências do vértice em que sai a aresta e
    também adiciona ao dicionário de capacidades a
    capacidade da aresta adicionada.
    '''
    rede.G[u].append(v)
    rede.capacidade[(u, v)] = w


def verifica_fluxo(rede, fluxo):
    '''
    Método que verifica se um fluxo é válido para
    uma dada rede. Para realizar essa verificação,
    3 etapas são seguidas. Se o fluxo entre dois
    vértices foi maior que a capacidade suportada
    pelos vértices, o fluxo não é válido. Se o fluxo
    de saída da fonte for diferente do fluxo de
    entrada do sumidouro, o fluxo também não é válido.
    Por fim, se para todos os vértices, exceto fonte
    e sumidouro, o fluxo de entrada for diferente do
    fluxo de saída, o fluxo também será inválido.
    '''
    for u in fluxo:
        if fluxo[u] > rede.capacidade[u] or fluxo[u] < 0:
            return False

    fluxoentrada, fluxosaida = calcula_fluxos(rede, fluxo)

    '''
    A etapa de calcular se o fluxo de saída da fonte
    é o mesmo que o fluxo de entrada do sumidouro é
    descartável, porém pode auxiliar no tempo de
    execução do algoritmo, já que é uma verificação
    feita em tempo O(1).
    '''
    if fluxosaida[rede.s] != fluxoentrada[rede.t]:
        return False

    for i in range(rede.num):
        if i != rede.s and i != rede.t:
            if fluxoentrada[i] != fluxosaida[i]:
                return False

    return True

def Etapa1():
    s, v1, v2, v3, v4, t = list(range(6))

    rede = cria_rede(6, s, t)

    addAresta(rede, s, v1, 16)
    addAresta(rede, s, v2, 13)
    addAresta(rede, v1, v3, 12)
    addAresta(rede, v2, v1, 4)
    addAresta(rede, v3, v2, 9)
    addAresta(rede, v2, v4, 14)
    addAresta(rede, v3, t, 20)
    addAresta(rede, v4, v3, 7)
    addAresta(rede, v4, t, 4)

    fluxo = {}
    fluxo[(s, v1)] = 11
    fluxo[(v1, v3)] = 11
    fluxo[(v3, t)] = 11

    '''
    Fluxo válido, pois respeita todas as regras
    de validade citadas.
    '''

    assert verifica_fluxo(rede, fluxo) == True

    fluxo1 = {}
    fluxo1[(s, v2)] = 14

    '''
    Fluxo inválido, pois a capacidade entre s e v2
    é menor do que o fluxo.
    '''

    assert verifica_fluxo(rede, fluxo1) == False

    fluxo2 = {}
    fluxo2[(s, v1)] = 5
    fluxo2[(s, v2)] = 3
    fluxo2[(v1, v3)] = 5
    fluxo2[(v2, v4)] = 3
    fluxo2[(v3, t)] = 5
    fluxo2[(v4, t)] = 2

    '''
    Fluxo inválido, pois o fluxo de saída da fonte
    é diferente do fluxo de entrada do sumidouro.
    '''

    assert verifica_fluxo(rede, fluxo2) == False

    fluxo3 = {}
    fluxo3[(s, v1)] = 5
    fluxo3[(v1, v3)] = 5
    fluxo3[(v3, t)] = 3
    fluxo3[(v4, t)] = 2

    '''
    Fluxo inválido, pois o fluxo de entrada e de saída
    de alguns dos vértices (v3 e v4) é diferente.
    '''

    assert verifica_fluxo(rede, fluxo3) == False

def cria_rede_residual(rede, fluxo):
    '''
    Este método cria uma rede residual baseando se
    em uma rede inicial e um fluxo. Uma rede residual
    é uma rede com mesmo numero de vértices que a rede
    a qual se baseia, assim como mesma fonte e mesmo
    sumidouro. A diferença está nas arestas. A rede
    residual utiliza o fluxo passado como parâmetro
    para calcular a capacidade entre suas arestas.
    Para cada aresta na rede original, caso o fluxo
    passado por uma aresta (u, v) não exista, o valor
    da capacidade entre (u, v) na rede residual seria
    igual ao da rede original. Caso contrário, o valor
    da capacidade na rede residual será a capacidade
    original menos o fluxo passado por essa aresta, e
    uma aresta com valor desse fluxo será adicionado no
    sentido contrário, ou seja, em (v, u).
    '''

    if verifica_fluxo(rede, fluxo) == False:
        #print("Fluxo Inválido")
        return False

    rede_residual = Rede(rede.num, rede.s, rede.t)

    for aresta, capacidade in rede.capacidade.items():
        u, v = aresta
        if (u, v) in fluxo:
            fluxo_uv = fluxo[(u, v)]
        else:
            fluxo_uv = 0
        if capacidade - fluxo_uv > 0:
            addAresta(rede_residual, u, v, capacidade - fluxo_uv)
        if fluxo_uv > 0:
            addAresta(rede_residual, v, u, fluxo_uv)
        if capacidade - fluxo_uv == capacidade:
            addAresta(rede_residual, v, u, 0)
    return rede_residual


def Etapa2():
    # Grafo da figura 26.1(a) do livro do Cormen.

    s, v1, v2, v3, v4, t = list(range(6))

    rede = cria_rede(6, s, t)

    addAresta(rede, s, v1, 16)
    addAresta(rede, s, v2, 13)
    addAresta(rede, v1, v3, 12)
    addAresta(rede, v2, v1, 4)
    addAresta(rede, v3, v2, 9)
    addAresta(rede, v2, v4, 14)
    addAresta(rede, v3, t, 20)
    addAresta(rede, v4, v3, 7)
    addAresta(rede, v4, t, 4)

    fluxo = {}
    fluxo[(s, v1)] = 11
    fluxo[(s, v2)] = 3
    fluxo[(v1, v3)] = 12
    fluxo[(v2, v1)] = 1
    fluxo[(v2, v4)] = 2
    fluxo[(v3, t)] = 12
    fluxo[(v4, t)] = 2

    '''
    Criando uma rede residual partindo da figura
    26.1(a) do CLRS e um fluxo qualquer dado acima.
    '''

    rede_res = cria_rede_residual(rede, fluxo)
    caminho = encontrar_caminho(rede_res, pai=[-1] * rede_res.num)
    print('O caminho encontrado foi', caminho)
    print(rede_res)

    assert rede_res.capacidade[(s, v1)] == 5
    assert rede_res.capacidade[(v1, s)] == 11
    assert rede_res.capacidade[(s, v2)] == 10
    assert rede_res.capacidade[(v2, s)] == 3
    '''
    COMO O FLUXO CONSUMIU A CAPACIDADE TOTAL DE V1
    ATE V3, NÃO HÁ ARESTA (V1, V3) NA REDE RESIDUAL,
    APENAS (V3, V1) QUE POSSUI A CAPACIDADE TOTAL.
    '''
    assert rede_res.capacidade[(v3, v1)] == 12
    assert rede_res.capacidade[(v2, v1)] == 3
    assert rede_res.capacidade[(v1, v2)] == 1
    assert rede_res.capacidade[(v3, v2)] == 9
    assert rede_res.capacidade[(v2, v4)] == 12
    assert rede_res.capacidade[(v4, v2)] == 2
    assert rede_res.capacidade[(v3, t)] == 8
    assert rede_res.capacidade[(t, v3)] == 12
    assert rede_res.capacidade[(v4, v3)] == 7
    assert rede_res.capacidade[(v4, t)] == 2
    assert rede_res.capacidade[(t, v4)] == 2

def encontrar_caminho(rede_residual, pai):
    '''
    Função que encontra um caminho qualquer (comecando
    em s e terminando em tem uma rede residual. A ideia
    é utilizar o BFS para encontrar este caminho visitando
    todos os nós em ordem crescente de distância da fonte,
    garantindo que o caminho encontrado seja o mais curto
    possível.
    '''

    visitados = [False] * rede_residual.num
    visitados[rede_residual.s] = True
    Q = deque()
    Q.append(rede_residual.s)

    while Q:
        u = Q.popleft()
        for v in rede_residual.G[u]:
            if not visitados[v] and rede_residual.capacidade[(u, v)] > 0:
                pai[v] = u
                visitados[v] = True
                Q.append(v)

                if v == rede_residual.t:
                    caminho = []
                    while v != rede_residual.s:
                        caminho.append(v)
                        v = pai[v]

                    caminho.append(rede_residual.s)
                    caminho.reverse()
                    return caminho

    return None

def teste_encontrar_caminho():
    '''
    Função para testar o algoritmo que utiliza
    o BFS para encontrar o caminho mais curto
    possível indo da fonte até o sumidouro.
    '''
    s, v1, v2, v3, v4, t = list(range(6))

    rede = cria_rede(6, s, t)

    addAresta(rede, s, v1, 16)
    addAresta(rede, s, v2, 13)
    addAresta(rede, v1, v3, 12)
    addAresta(rede, v2, v1, 4)
    addAresta(rede, v3, v2, 9)
    addAresta(rede, v2, v4, 14)
    addAresta(rede, v3, t, 20)
    addAresta(rede, v4, v3, 7)
    addAresta(rede, v4, t, 4)

    res = cria_rede_residual(rede, fluxo={})

    assert encontrar_caminho(res, pai=[-1] * res.num) == [s, v1, v3, t]

def EdmondsKarp(rede):
    '''
    O algoritmo de Edmonds Karp é nada mais que uma
    variação do algoritmo Ford-Fulkerson e usa a ideia
    de caminhos aumentantes (encontrados via BFS) para
    encontrar o fluxo máximo em tempo polinomial. Nesta
    implementação foi feito um loop infinito, que será
    quebrado apenas quando não houver caminho restante
    da fonte até o sumidouro. Inicialmente, o fluxo em
    todas as arestas é definido como zero. Isso significa
    que nenhum fluxo está passando pelas arestas do grafo.
    O objetivo do algoritmo é encontrar o fluxo máximo que
    pode ser enviado da fonte ao sumidouro. O algoritmo
    encontra o caminho aumentante usando o algoritmo da
    busca em largura. Enquanto houver um caminho aumentante,
    o algoritmo vai percorrer este caminho, que é um
    caminho da fonte ao sumidouro. Se não houver mais
    caminhos aumentantes, o algoritmo termina. Começando
    pela fonte, ele visita todos os vértices que podem ser
    alcançados a partir da fonte até chegar ao sumidouro.
    Durante a busca em largura, o algoritmo marca cada
    vértice que é visitado e armazena o caminho que leva
    ao vértice. Uma vez que o caminho aumentante é encontrado,
    é preciso determinar a quantidade de fluxo que pode ser
    enviada ao longo dele. Essa quantidade é igual à menor
    capacidade das arestas ao longo do caminho aumentante,
    que representa a restrição mais limitante para o envio
    de fluxo. Depois que o fluxo máximo é determinado, ele
    é adicionado ao fluxo atual ao longo do caminho aumentante,
    o que significa que o fluxo é enviado do vértice de origem
    ao vértice de destino ao longo do caminho aumentante.
    Isso também significa que a capacidade da aresta diminui
    à medida que o fluxo é enviado ao longo dela. O algoritmo
    continua a encontrar caminhos aumentantes e adicionar fluxo
    até que não haja mais caminhos aumentantes. Nesse ponto,
    o fluxo máximo é encontrado e o algoritmo termina.
    '''
    fluxo_total = 0
    residual = cria_rede_residual(rede, fluxo={})
    fluxoEK = {}

    while True:
        pai = [-1] * residual.num

        caminho = encontrar_caminho(residual, pai)
        if caminho == None:
            #print("Nenhum caminho encontrado")
            break
        print("Caminho encontrado:", caminho)
        caminho_min = float("Inf")
        s = residual.t
        while s != residual.s:
            caminho_min = min(caminho_min, residual.capacidade[(pai[s], s)])
            s = pai[s]

        fluxo_total += caminho_min

        v = residual.t
        while v != residual.s:
            u = pai[v]
            fluxo_aresta = caminho_min
            if (u, v) in fluxoEK:
                fluxo_aresta += fluxoEK[(u, v)]
            fluxoEK[(u, v)] = fluxo_aresta
            residual.capacidade[(u, v)] -= caminho_min
            residual.capacidade[(v, u)] += caminho_min
            v = pai[v]

    assert verifica_fluxo(rede, fluxoEK) == True

    print("\nO maior fluxo possível nesta rede é", fluxo_total)

    return fluxo_total

def DFS(rede, u, visitados):
    '''
    Este método implementa a busca em profundidade,
    que será utilizada na geração de uma rede
    aleatória válida da seguinte maneira:
    Após fazer o DFS começando pela fonte, se algum
    vértice não foi visitado, é adicionada uma aresta
    entre a fonte e este vértice.
    '''
    for v in rede.G[u]:
        if (u, v) in rede.capacidade and not visitados[v]:
            visitados[v] = True
            DFS(rede, v, visitados)

def DFS_invertido(rede, u, visitados):
    '''
    Este método implementa a busca em profundidade,
    mas no sentido contrário, ou seja, começando do
    sumidouro e considerando como caminho válido
    (v, u) ao invés de (u, v). Será utilizada
    na geração de uma rede aleatória válida da
    seguinte maneira: Após fazer o DFS começando
    pelo sumidouro, se algum vértice não foi visitado,
    é adicionada uma aresta entre o sumidouro e este
    vértice.
    '''
    for v in (rede.G[u]):
        if (v, u) in rede.capacidade and not visitados[u]:
            visitados[u] = True
            DFS_invertido(rede, u, visitados)

def rede_aleatoria_valida():
    '''
    Este método cria uma rede aleatória que preencha
    os requisitos para ser válida, ou seja, a rede não pode
    ter arestas antiparalelas e, para todos os vértices
    v, deve existir um caminho de s para t que passe por v.
    Para isso, é feita uma iteração sobre cada par de vértices,
    adicionando ou não uma aresta entre eles. Após isso,
    as funções de DFS são utilizadas para verificar se
    para todos os vértices v existe um caminho de s para t
    que passe por v. Note que ao fazer qualquer inserção de
    aresta, caso (u, v) exista, (v, u) nunca será adicionada,
    preservando o paralelismo do grafo.
    '''
    quantvert = random.randint(2, 10)
    fonte = random.randint(0, quantvert-1)
    sumidouro = random.choice([i for i in range(quantvert) if i != fonte])

    rede = Rede(quantvert, fonte, sumidouro)

    if rede.num == 2:
        addAresta(rede, fonte, sumidouro, random.randint(1, 10))

    for u in range(rede.num):
        for v in range(u + 1, rede.num):
            if (v, u) not in rede.capacidade and v!=fonte and u!=sumidouro:
                if random.choice([0, 1]):
                    addAresta(rede, u, v, random.randint(1, 10))

    visitados = [False] * rede.num
    visitados[rede.s] = True
    DFS(rede, rede.s, visitados)
    for v in range(rede.num):
        if v!=fonte and v!=sumidouro:
            if not visitados[v]:
                addAresta(rede, fonte, v, random.randint(1, 10))

    visitados = [False] * rede.num
    visitados[rede.s] = True
    DFS_invertido(rede, rede.t, visitados)
    for v in range(rede.num):
        if v!=fonte and v!=sumidouro:
            if not visitados[v]:
                addAresta(rede, v, sumidouro, random.randint(1, 10))

    print(rede)

    return rede

def Etapa3():
    s, v1, v2, v3, v4, t = list(range(6))

    rede = cria_rede(6, s, t)

    addAresta(rede, s, v1, 16)
    addAresta(rede, s, v2, 13)
    addAresta(rede, v1, v3, 12)
    addAresta(rede, v2, v1, 4)
    addAresta(rede, v3, v2, 9)
    addAresta(rede, v2, v4, 14)
    addAresta(rede, v3, t, 20)
    addAresta(rede, v4, v3, 7)
    addAresta(rede, v4, t, 4)

    '''
    Sabemos que o fluxo máximo na figura 26.1(a)
    do CLRS é 23, portanto, é possível rodar o 
    algoritmo de Edmonds-Karp nesta rede e verificar
    a saída já conhecida.
    '''
    assert EdmondsKarp(rede) == 23

    '''
    É possível testar o algoritmo de Edmonds-Karp
    para entradas aleatórias também. Dentro da
    própria função EdmondsKarp, após encontrar o
    fluxo máximo já é feita a verificação que o
    valida.
    '''

    R = rede_aleatoria_valida()
    S = rede_aleatoria_valida()
    T = rede_aleatoria_valida()
    EdmondsKarp(R)
    EdmondsKarp(S)
    EdmondsKarp(T)

def main():
    teste_calcula_fluxos()
    teste_encontrar_caminho()
    Etapa1()
    Etapa2()
    Etapa3()

if __name__ == "__main__":
    main()
