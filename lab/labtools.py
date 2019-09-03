def printar_mmq(mmq):
    """Função que exibe uma descrição dos dados de certa regressão linear <mmq> no console.

    Parâmetros:
    mmq: RegressaoLinear"""

    import stat

    if not isinstance(mmq ,stat.RegressaoLinear):
        raise Exception("Argumento <mmq> do tipo incorreto")

    dados = mmq.resultados

    try:
        if "sx" in dados:
            print("")
            print("N = " + str(dados["n"]))
            print("Soma p/ variavel independente = " + str(dados["sx"]))
            print("Soma quadratica p/ variavel independente = " + str(dados["sx_sq"]))
            print("Soma p/ variavel dependente = " + str(dados["sy"]))
            print("Soma mista = " + str(dados["sxy"]))
            print("Delta = " + str(dados["delta"]))
            return

        if "swx" in dados:
            print("a = " + str(dados["a"].media) + " +- " + str(dados["a"].incerteza))
            print("b = " + str(dados["b"].media) + " +- " + str(dados["b"].incerteza))
            print("")
            print("N = " + str(dados["n"]))
            print("Soma de w = " + str(dados["sw"]))
            print("Soma p/ w vezes variavel independente = " + str(dados["swx"]))
            print("Soma p/ w vezes variavel independente quadrada = " + str(dados["swx_sq"]))
            print("Soma p/ w vezes variavel dependente = " + str(dados["swy"]))
            print("Soma de w vezes produto misto = " + str(dados["swxy"]))
            print("Delta = " + str(dados["delta"]))
            return
    except Exception:
        raise Exception("Dicionário de resultados corrompido")

    raise Exception("Dicionário de resultados fora do formato esperado")