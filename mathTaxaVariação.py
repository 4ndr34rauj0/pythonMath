def ler_numero(msg):
    
    while True:
        txt = input(msg).strip().replace(",", ".")
        try:
            if "/" in txt:
                num, den = txt.split("/")
                return float(num) / float(den)
            return float(txt)
        except (ValueError, ZeroDivisionError):
            print("  Valor inválido. Tenta de novo.")


def fmt(valor):

    return "{valor:.10g}".format(valor)


def taxa_media(x1, y1, x2, y2):
    if x2 == x1:
        raise ValueError("x2 = x1: a taxa de variação não está definida (divisão por zero).")
    return (y2 - y1) / (x2 - x1)


def modo_dois_pontos():
    print("\nIntroduz os dois pontos A(x1, y1) e B(x2, y2):")
    x1 = ler_numero("  x1 = ")
    y1 = ler_numero("  y1 = ")
    x2 = ler_numero("  x2 = ")
    y2 = ler_numero("  y2 = ")
    try:
        m = taxa_media(x1, y1, x2, y2)
    except ValueError as e:
        print("Erro:", e)
        return
    print("\nTaxa de variação média = (y2 - y1)/(x2 - x1)")
    print("              =({})-({})/({}-{})".format(fmt(y2), fmt(y1), fmt(x2), fmt(x1)))
    print("                       = {}".format(fmt(m)))


def modo_incognita():
    print("\nIntroduz a taxa de variação e o ponto A(x1, y1):")
    m = ler_numero("  taxa m = ")
    x1 = ler_numero("  x1 = ")
    y1 = ler_numero("  y1 = ")

    print("\nQual é a coordenada conhecida do ponto B?")
    escolha = ""
    while escolha not in ("x", "y"):
        escolha = input("  Escreve 'x' ou 'y': ").strip().lower()

    if escolha == "x":
        x2 = ler_numero("  x2 = ")
        y2 = y1 + m * (x2 - x1)
        print("\ny2 = y1 + m·(x2 - x1) = {} + {}·({} - {})".format(fmt(y1), fmt(m), fmt(x2), fmt(x1)))
        print("y2 = {}".format(fmt(y2)))
        print("Ponto B({}, {})".format(fmt(x2), fmt(y2)))
    else:
        y2 = ler_numero("  y2 = ")
        if m == 0:
            if y2 == y1:
                print("\nCom m = 0 e y2 = y1, qualquer valor de x2 serve (reta horizontal).")
            else:
                print("\nImpossível: com m = 0, y2 tem de ser igual a y1.")
            return
        x2 = x1 + (y2 - y1) / m
        print("\nx2 = x1 + (y2 - y1)/m = {} + ({} - {})/{}".format(fmt(x1), fmt(y2), fmt(y1), fmt(m)))
        print("x2 = {}".format(fmt(x2)))
        print("Ponto B({}, {})".format(fmt(x2), fmt(y2)))



def main():
    while True:
        print("\n!!! Taxa de variação !!!")
        print("1) Tenho dois pontos -> calcular a taxa")
        print("2) Tenho a taxa, um ponto e uma coordenada do outro -> achar a incógnita")
        print("0) Sair")
        op = input("Opção: ").strip()
        if op == "1":
            modo_dois_pontos()
        elif op == "2":
            modo_incognita()
        elif op == "0":
            break
        else:
            print("Opção inválida.")


main()
