from lab import helper


class Tabela:
    """TO-DO"""

    def __init__(self, dados=[], rotulos=[], separador="\\hline"):
        self._dados = []
        self._rotulos = rotulos
        self.separador = separador
        """TO-DO"""

        if not helper.iteravel(rotulos):
            raise Exception("Argumento incorreto: <rotulos> não é iterável")
        if helper.iteravel_vazio(dados):
            return

        self.dados = dados

    @property
    def dados(self):
        return self._dados

    @dados.setter
    def dados(self, dados):
        try:
            self._dados = [[i for i in l] for l in dados]

        except Exception:
            raise Exception(
                "Argumento incorreto: <dados> não é iterável de iteráveis")

    @property
    def rotulos(self):
        return self._rotulos

    @rotulos.setter
    def rotulos(self, r):
        if not helper.iteravel(r):
            raise Exception("RArgumento incorreto: <rotulos> não é iterável")
        else:
            self._rotulos = r

    def exibir(self):
        s = "\\begin{tabular}"
        s += "{|" + ("c|" * self._colunas) + "}"  # Número de colunas

        s += "\n\n" + self.separador + "\n"
        for r in self._rotulos:
            s += str(r) + " & "

        if not helper.iteravel_vazio(self._rotulos):
            s = s[:-2] + "\\\\\n\n" + self.separador + "\n"

        for l in self._dados:
            for obj in l:
                s += str(obj) + " & "

            # Remover "& " adicional, colocar \\ no final, pular uma linha
            s = s[:-2] + "\\\\\n\n" + self.separador + "\n"

        s += "\\end{tabular}"
        return s

    def __str__(self):
        return self.exibir()


class TabelaMatriz(Tabela):
    """TO-DO"""

    def __init__(self, matriz_dados=[], rotulos=[], separador="\\hline"):
        self._linhas = 0
        self._colunas = 0

        """TO-DO"""

        if not helper.matriz(matriz_dados):
            raise Exception("Argumento incorreto: <matriz_dados> não é matriz")

        super().__init__(matriz_dados, rotulos, separador)

    @property
    def linhas(self):
        return self._linhas

    @property
    def colunas(self):
        return self._colunas

    @property
    def dados(self):
        return self._dados

    @dados.setter  # override
    def dados(self, matriz_dados):
        if not helper.matriz(matriz_dados):
            raise Exception("Argumento incorreto: <matriz_dados> não é matriz")

        Tabela.dados.fset(self, matriz_dados)
        self._linhas = len(matriz_dados)
        self._colunas = len(matriz_dados[0] if self._linhas != 0 else 0)

    def adicionar_coluna(self, lista_objetos, n=None):

        if not helper.iteravel(lista_objetos):
            raise Exception(
                "Argumento inválido <lista_objetos>: <lista_objetos> não iterável")

        if not (isinstance(n, int) or n == None):
            raise Exception("Argumento inválido <n>: diferente de int ou None")

        elif helper.iteravel_vazio(lista_objetos):
            return self

        lista_objetos_ = list(lista_objetos)

        if self._dados == []:
            self._dados = [[i] for i in lista_objetos_]
            self._linhas = len(lista_objetos_)
            self._colunas = 1
            return self

        elif len(lista_objetos_) != self._linhas:
            raise Exception(
                "Argumento inválido <lista_objetos>: dimensão de <lista_objetos> diferente do número de linhas")

        # Chatices checando cada caso e o funcionamento meio burro de .insert
        if n == None:
            for i in range(self._linhas):
                self._dados[i].append(lista_objetos_[i])

        elif n >= 0:
            for i in range(self._linhas):
                self._dados[i].insert(n, lista_objetos_[i])

        elif n == -1:
            for i in range(self._linhas):
                self._dados[i].insert(self._colunas, lista_objetos_[i])

        else:
            for i in range(self._linhas):
                self._dados[i].insert(n + 1, lista_objetos_[i])

        self._colunas += 1
        return self

    def adicionar_linha(self, lista_objetos, n=None):

        if not helper.iteravel(lista_objetos):
            raise Exception(
                "Argumento inválido <lista_objetos>: <lista_objetos> não iterável")

        if not (isinstance(n, int) or n == None):
            raise Exception("Argumento inválido <n>: diferente de int ou None")

        elif helper.iteravel_vazio(lista_objetos):
            return self

        lista_objetos_ = list(lista_objetos)

        if self._dados == []:
            self._dados.append(lista_objetos_)
            self._linhas = 1
            self._colunas = len(lista_objetos_)
            return self

        elif len(lista_objetos_) != self._colunas:
            raise Exception(
                "Argumento inválido <lista_objetos>: dimensão de <lista_objetos> diferente do número de colunas")

        # Chatices checando cada caso e o funcionamento meio burro de .insert
        if n == None:
            self._dados.append(lista_objetos_)

        elif n >= 0:
            self._dados.insert(n, lista_objetos_)

        elif n == -1:
            self._dados.insert(self._linhas, lista_objetos_)

        else:
            self._dados.insert(n + 1, lista_objetos_)

        self._linhas += 1
        return self

    def remover_coluna(self, n):
        if self._dados == []:
            return

        else:
            for i in range(self._linhas):
                self._dados[i].pop(n)

    def remover_linha(self, n):
        if self._dados == []:
            return

        else:
            self.dados.pop(n)


class TabelaRegressao():
    """Classe que retorna tabelas LaTeX de uma instância de lab.stat.RegressaoLinear"""

    _rotulos_latex = {
        "a": "$\\overline{a} \\pm u_a$",
        "b": "$\\overline{b} \\pm u_b$",
        "n": "$N$",
        "sw": "$\\sum w$",
        "uy": "$u_y$",
        "sx": "$\\sum x$",
        "swx": "$\\sum wx$",
        "sx_sq": "$\\sum x^2$",
        "swx_sq": "$\\sum wx^2$",
        "sy": "$\\sum y$",
        "swy": "$\\sum wy$",
        "swxy": "$\\sum wxy$",
        "delta": "$\\Delta$"
    }

    @property
    def rotulos_latex(self):
        return self._rotulos_latex

    def __init__(self, r=None):
        import lab

        self._regressao = lab.stat.RegressaoLinear()

        if r is not None:
            self.regressao = r

    @property
    def regressao(self):
        return self._regressao

    @regressao.setter
    def regressao(self, other):
        import lab
        if not isinstance(other, lab.stat.RegressaoLinear):
            raise Exception(
                "Argumento inválido <r>: <r> não é instância de RegressaoLinear")

        else:
            self._regressao = other

    def tabela_assistentes(self):
        r = self._regressao.resultados
        labels = []
        if "sw" in r:
            labels = ["n", "sw", "swx", "swy", "swx_sq", "swxy", "delta"]

        else:
            labels = ["n", "uy", "sx", "sy", "sx_sq", "sxy", "delta"]

        return TabelaMatriz([["{}".format(r[l]).replace(".",",") for l in labels]], rotulos=[self.rotulos_latex[l] for l in labels])

    def tabela_coeficientes(self, invertido=False):

        r = self._regressao.resultados if not invertido else self._regressao.coeficientes_invertidos()

        return TabelaMatriz([[r["a"], r["b"]]], rotulos=[self.rotulos_latex["a"], self.rotulos_latex["b"]])
