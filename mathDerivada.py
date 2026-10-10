def mdc(a, b):
    while b:
        a, b = b, a % b
    return a


def reduz(p, q):
    if q < 0:
        p = -p
        q = -q
    g = mdc(abs(p), q)
    return p // g, q // g


def parse_num(s):
    if s == "":
        raise ValueError("numero em falta")
    if "." in s:
        a, b = s.split(".", 1)
        return reduz(int(a + b), 10 ** len(b))
    return int(s), 1


def parse_frac(s):
    s = s.replace("(", "").replace(")", "")
    if "/" in s:
        a, b = s.split("/", 1)
        p1, q1 = parse_num(a)
        p2, q2 = parse_num(b)
        if p2 == 0:
            raise ValueError("divisao por zero")
        return reduz(p1 * q2, q1 * p2)
    return parse_num(s)


def separar(s):
    out = []
    atual = ""
    for c in s:
        if (c == "+" or c == "-") and atual != "" and atual[-1] != "^":
            out.append(atual)
            if c == "-":
                atual = "-"
            else:
                atual = ""
        else:
            atual += c
    if atual != "":
        out.append(atual)
    return out


def termo(t):

    sinal = 1
    while t != "" and (t[0] == "+" or t[0] == "-"):
        if t[0] == "-":
            sinal = -sinal
        t = t[1:]
    i = t.find("x")
    if i < 0:
        p, q = parse_frac(t)
        return sinal * p, q, 0
    coef = t[:i]
    resto = t[i + 1:]
    if coef.endswith("*"):
        coef = coef[:-1]
    if coef == "":
        p, q = 1, 1
    else:
        p, q = parse_frac(coef)
    den = ""
    if "/" in resto:
        resto, den = resto.split("/", 1)
    e = 1
    if resto != "":
        if resto[0] != "^":
            raise ValueError("x so com ^n")
        e = int(resto[1:])
        if e < 0:
            raise ValueError("expoente negativo")
    if den != "":
        dp, dq = parse_frac(den)
        if dp == 0:
            raise ValueError("divisao por zero")
        p, q = reduz(p * dq, q * dp)
    return sinal * p, q, e


def ler(txt):
    s = txt.replace(" ", "").lower()
    s = s.replace("\u00b2", "^2").replace("\u00b3", "^3").replace("**", "^")
    if "=" in s:
        s = s.split("=")[-1]
    if s == "":
        raise ValueError("vazio")
    poly = {}
    for t in separar(s):
        p, q, e = termo(t)
        if e in poly:
            p0, q0 = poly[e]
            poly[e] = reduz(p0 * q + p * q0, q0 * q)
        else:
            poly[e] = reduz(p, q)
    return poly


def derivar(poly):
    r = {}
    for e in poly:
        if e > 0:
            p, q = poly[e]
            r[e - 1] = reduz(p * e, q)
    return r


def txt_termo(p, q, e):
    if e == 0:
        if q == 1:
            return str(p)
        return str(p) + "/" + str(q)
    s = ""
    if p == -1:
        s = "-"
    elif p != 1:
        s = str(p)
    s += "x"
    if e > 1:
        s += "^" + str(e)
    if q != 1:
        s += "/" + str(q)
    return s


def mostrar(poly):
    ks = sorted(poly.keys())
    ks.reverse()
    s = ""
    for e in ks:
        p, q = poly[e]
        if p == 0:
            continue
        t = txt_termo(p, q, e)
        if s == "":
            s = t
        elif t[0] == "-":
            s += " - " + t[1:]
        else:
            s += " + " + t
    if s == "":
        return "0"
    return s


def main():
    print("Derivada")
    while True:
        txt = input("f(x) = ")
        if txt.strip() == "":
            break
        try:
            f = ler(txt)
        except Exception:
            print("Erro: usa termos como 2x^2, 3x, 5, 2/7x")
            continue
        print("f(x)  = " + mostrar(f))
        print("f'(x) = " + mostrar(derivar(f)))


main()