import math



digitos = lambda x: int(math.floor(math.log10(abs(x))))


arredondar = lambda x, n=1: round(x, -digitos(x)+n-1)


def normalizar(media, incerteza, n_alg=1):
    """Método que devolve uma classe como a atual, mas normalizada na incerteza com <n_alg> algarismos significativos.

    Parâmetros:
    n_alg: int (>0)

    Retorno: Medida
    """


    incerteza_norm = arredondar(incerteza, n_alg)
    media_norm = round(media, -digitos(incerteza_norm)+n_alg-1)

    return (media_norm, incerteza_norm)

def formatar_com_erro(media, incerteza, algsig=1):
    """Função que formata uma medida em LaTeX"""

    if incerteza > 1:
        d = digitos(incerteza)
        return "$(" + formatar_com_erro(media/pow(10,d-algsig+2), incerteza/pow(10,d-algsig+2), algsig)[1:-1] + ")\\cdot 10^" + ("{{ {} }}" if d > 9 else "{}").format(d+1) + "$"
    
    else:
        norm = normalizar(media, incerteza, algsig)
        return ("${} \\pm {}$".format(norm[0],norm[1])).replace(".", ",")

def iteravel(v):
    try:
        i = iter(v)
        return True
    except Exception:
        return False


iteravel_vazio = lambda v: not any(True for _ in v)


def matriz(m):
    if not iteravel(m):
        return False

    elif iteravel_vazio(m):
        return True

    else:

        try:
            n_ = len(list(list(m)[0]))
            for l in m:
                if len(list(l)) != n_:
                    return False

            return True

        except Exception:
            return False


def matriz_iteravel_lista(m):
    if not matriz(m):
        raise Exception("Argumento inválido <v>: <v> não é uma matriz iterável")

    saolistas = True and any([isinstance(l, list) for l in m])

    if isinstance(m, list) and saolistas:
        return m

    elif saolistas:
        return [l for l in m]

    else:
        mat = []
        for l in m:
            mat.append([i for i in l])