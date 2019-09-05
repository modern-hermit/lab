import math
from lab import helper


class Medida():
    """Classe que implementa uma medida e seus principais métodos.

    Membros:
    media, incerteza: float

    Métodos:
    ucomb, normalizar
    """

    @staticmethod
    def ucomb(incertezas):
        """Método estático que combina a incerteza de uma lista de medidas. Devolve, por padrão, '0.0' para uma lista vazia.

        Parâmetros:
        incertezas: list(float)

        Retorno: float
        """

        uc = 0.0
        for u in incertezas:
            uc += math.pow(u, 2)

        return math.pow(u, 1 / 2)

    def normalizar(self, n_alg=1):
        """Método que devolve uma classe como a atual, mas normalizada na incerteza com <n_alg> algarismos significativos.

        Parâmetros:
        n_alg: int (>0)

        Retorno: Medida
        """

        norm = helper.normalizar(self.media, self.incerteza, n_alg)

        return Medida(norm[0], norm[1])

    def __init__(self, medida, incerteza=None, algarismos=0, formatacao=(lambda m: helper.formatar_com_erro(m.media, m.incerteza))):

        self.media = 0.0
        self.incerteza = 0.0
        self.formatacao = formatacao

        """Construtor de Medida.
		Quando construído com uma lista não nula, é assumido que foi construída com medidas repetidas de um experimento e o cálculo é feito sobre estes valores, sem incerteza.
		Quando construído com medida sendo float e a incerteza sendo uma lista, as incertezas são combinadas e o valor é atribuído à incerteza.
		Quando ambos são construídos como float, os valores são simplesmente atribuídos às variáveis respectivas.
		Se algarismos for não nulo, faz a normalização da medida com <algarismos> algarismos significativos na incerteza.
		Caso contrário, levanta uma exceção.

		Parâmetros:
		medida: float ou list(float) ou list(int)
		incerteza: float ou int ou list ou None"""

        if not (isinstance(incerteza, float) or isinstance(incerteza, int) or helper.iteravel(incerteza)):
            raise Exception("Argumento incorreto: <incerteza>")

        # Se é número, checar possíveis casos
        if isinstance(medida, float) or isinstance(medida, int):

            # Processar a incerteza
            if isinstance(incerteza, float) or isinstance(incerteza, int):
                self.incerteza = float(incerteza)

            # Se é lista, calcular a incerteza combinada
            elif isinstance(incerteza, iterable):
                # Assumimos que é desnecessário checar se a lista é composta de números, de fato
                self.incerteza = ucomb(incerteza)

            # Tratada a incerteza, atribuir o valor da média

            self.media = float(medida)

        # Se é lista, calcular incerteza do desvio-padrão populacional
        elif helper.iteravel(medida):
            if incerteza != None or helper.iteravel_vazio(medida):
                raise Exception("Inicialização incorreta da classe Medida")

            n = len(medida)
            m_ph = 0.0  # Placeholder da média

            for md in medida:
                m_ph += md  # Soma dos valores que eventualmente serão dividos por n; maior precisão

            self.media = m_ph / n

            # Com a média, faremos o cálculo da incerteza padrão
            u_ph = 0.0

            for md in medida:
                # Somar diferença entre média e medida ao quadrado
                u_ph += math.pow(self.media - md, 2)

            self.incerteza = math.pow(u_ph / (n * (n - 1)), 1 / 2)

        else:
            raise Exception(
                "Inicialização incorreta da classe Medida em <medida>")

        # Checar se o argumento "algarismos" foi bem definido (se não for inteiro)
        if not isinstance(algarismos, int):
            raise Exception(
                "Inicialização incorreta da classe Medida em <algarismos> (<algarismos> não inteiro)")

        # Checar se o argumento "algarismos" foi bem definido (se for inteiro)
        if algarismos < 0:
            raise Exception(
                "Inicialização incorreta da classe Medida em <algarismos> (<algarismos> < 0)")

        if algarismos > 0:
            norm = self.normalizar(algarismos)
            self.media = norm.media
            self.incerteza = norm.incerteza

    def __str__(self):
        return self.formatacao(self)

    def __getitem__(self, key):
    	if key == 0:
    		return self.media

    	if key == 1:
    		return self.incerteza

    	else:
    		raise Exception(
    			"Acesso de chave incorreto na classe Medida")


class RegressaoLinear():
    """Classe que gera uma regressão linear de várias possíveis representações de medidas e seus erros."""

    @staticmethod
    def _mmq(dados_x, dados_y, u):
        """Método estático de baixo nível que calcula a regressão linear de certos dados (X,Y+-u_i) para uma incerteza u_i fixa ou uma lista de incertezas, podendo o tipo de <u> variar.
        Se <u> for float, a regressão é calculada com erros em Y todos iguais. Se <u> for list, a regressão é calculada com erros em Y possivelmente distintos (perda de precisão).

        Parâmetros:
        dados_x: list(float)
        dados_y: list(float)
        u_fixo: float ou list

        Retorno: dict(a:Medida,
        b:Medida,
        n:int,
        uy:float,
        sx:float,
        sx_sq:float,
        sy:float,
        sxy:float,
        delta:float,uy:float) ou 

        dict(a:Medida,
        b:Medida,
        n:int,
        sw:float,
        swx:float,
        swx_sq:float,
        swy:float,
        swxy:float,
        delta:float)"""

        if isinstance(u, float) or isinstance(u, int):

            n = len(dados_x)

            if n != len(dados_y):
                raise Exception("Listas de dados de tamanhos distintos")

            sx = 0.0
            sx_sq = 0.0
            sy = 0.0
            sxy = 0.0

            for i in range(n):
                sx += dados_x[i]
                sx_sq += math.pow(dados_x[i], 2)
                sy += dados_y[i]
                sxy += dados_x[i] * dados_y[i]

            delta = n * sx_sq - math.pow(sx, 2)
            a = (n * sxy - sx * sy) / delta
            b = (sy * sx_sq - sxy * sx) / delta
            ua = math.pow(n / delta, 1 / 2) * u
            ub = math.pow(sx_sq / delta, 1 / 2) * u

            return ({"a": Medida(a, ua), "b": Medida(b, ub), "n": n, "sx": sx, "sx_sq": sx_sq, "sy": sy, "sxy": sxy, "delta": delta, "uy": u})

        elif helper.iteravel(u):
            n = len(dados_x)

            if n != len(dados_y) or n != len(u):
                raise Exception("Listas de dados de tamanhos distintos")

            swx = 0.0
            swx_sq = 0.0
            swy = 0.0
            swxy = 0.0
            sw = 0.0
            w = []

            for ui in u:
                w.append(math.pow(1 / ui, 2))

            for i in range(n):
                sw += w[i]
                swx += w[i] * dados_x[i]
                swy += w[i] * dados_y[i]
                swxy += w[i] * dados_x[i] * dados_y[i]
                swx_sq += w[i] * math.pow(dados_x[i], 2)

            delta = sw * swx_sq - math.pow(swx, 2)
            a = (sw * swxy - swx * swy) / delta
            b = (swy * swx_sq - swxy * swx) / delta
            ua = math.pow(sw / delta, 1 / 2)
            ub = math.pow(swx_sq / delta, 1 / 2)

            return ({"a": Medida(a, ua), "b": Medida(b, ub), "n": n, "sw": sw, "swx": swx, "swx_sq": swx_sq, "swy": swy, "swxy": swxy, "delta": delta})

        else:
            raise Exception("Argumento <u> incorreto")

    # Aqui acabam as implementações de baixo nível

    def __init__(self, dados=[], invertido=False):

        self._resultados = {}
        self._invertido = invertido

        """Construtor de RegressaoLinear.
		Deve ser construído com uma lista de dados em que cada elemento é uma tupla de instâncias de Medida.

		Parâmetros:
		dados: list(tuple(Medida,Medida)) """

        if not helper.iteravel(dados):
            raise Exception(
                "Inicialização incorreta da classe RegressaoLinear")

        elif helper.iteravel_vazio(dados):
            return

        else:
            self.dados = list(dados)
            self.calcular(inverter_eixos=invertido)

    @property
    def resultados(self):
        return self._resultados

    def calcular(self, inverter_eixos=False):
        """Método que calcula efetivamente a regressão linear dos dados e retorna """
        if not isinstance(inverter_eixos, bool):
            raise Exception("Argumento <inverter_eixos> incorreto")

        if inverter_eixos:

            # Placeholder de incerteza para checagem de caso de incertezas iguais
            u_ph = self.dados[0].incerteza

            u_iguais = True
            dados_x = []
            dados_y = []

            for par in self.dados:  # Checagem de caso de incertezas iguais e instanciamento de dados_x e dados_y

                if not par[0].incerteza == u_ph:
                    u_iguais = False

                # for aproveitado para criar dados_x, dados_y e otimizar número de loops
                dados_x.append(par[0].media)
                dados_y.append(par[1].media)

            # Instanciar lista de u's apenas se <u_iguais> for falso
            self._resultados = self._mmq(dados_y, dados_x, (self.dados[0][0].incerteza if u_iguais else [
                                         d[0].incerteza for d in self.dados]))

        else:
            # Placeholder de incerteza para checagem de caso de incertezas iguais
            u_ph = self.dados[0][1].incerteza

            u_iguais = True
            dados_x = []
            dados_y = []

            for par in self.dados:  # Checagem de caso de incertezas iguais e instanciamento de dados_x e dados_y

                if not par[1].incerteza == u_ph:
                    u_iguais = False

                # for aproveitado para criar dados_x, dados_y e otimizar número de loops
                dados_x.append(par[0].media)
                dados_y.append(par[1].media)

            # Instanciar lista de u's apenas se <u_iguais> for falso
            self._resultados = self._mmq(dados_x, dados_y, (self.dados[0][1].incerteza if u_iguais else [
                                         d[1].incerteza for d in self.dados]))

        self._invertido = inverter_eixos
        return self

    @property
    def invertido(self):
        return self._invertido


    def proporcao_incertezas(self):
    	uy_maior_ux = [m[1].incerteza/m[1].media > m[0].incerteza/m[0].media for m in self.dados]
    	prop_y = helper.arredondar(len(list(filter(lambda i: i, uy_maior_ux)))/len(uy_maior_ux),2)
    	return (helper.arredondar(1-prop_y,2), prop_y)


    def coeficientes_invertidos(self):
        """Método que inverte os valores de resultados['a'] e resultados['b'] a partir de um modelo de regressão invertido e propaga seus erros.

        Retorno: dict(a:Medida,
        b:Medida)"""

        if not self._resultados:
            raise Exception(
                "A regressão linear não tem resultados para que sejam calculados seus coeficientes invertidos")

        a_invertido = 1 / self._resultados['a'].media
        ua_invertido = self._resultados['a'].incerteza / \
            math.pow(self._resultados['a'].media, 2)

        b_invertido = -self._resultados['b'].media / \
            self._resultados['a'].media

        # Cálculo otimizado de ub_invertido
        ub_invertido = math.pow(math.pow(self._resultados['b'].incerteza, 2) + math.pow(
            self._resultados['a'].incerteza * self._resultados['b'].media / self._resultados['a'].media, 2), 1 / 2) / abs(self._resultados['a'].media)

        return {'a': Medida(a_invertido, ua_invertido), 'b': Medida(b_invertido, ub_invertido)}

    def __getitem__(self, key):
    	return self._resultados[key]
