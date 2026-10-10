from math import *
import ti_plotlib as plt

x = 0
H = 1e-6
ln = log


def criar_f(txt):
    txt = txt.replace("^", "**")

    def f(v):
        global x
        x = v
        return eval(txt)

    return f


def finito(v):
    return v == v and abs(v) != float("inf")


def declive_h(f, x0, h=H):
    return (f(x0 + h) - f(x0)) / h


def y_or_n(pergunta):
    while True:
        r = input(pergunta).strip().lower()
        if r in ("y", "yes", "s", "sim"):
            return True
        if r in ("n", "no", "nao"):
            return False
        print("Responde com y ou n.")


def derivada_existe(f, x0):
    m1 = declive_h(f, x0, H)
    m2 = declive_h(f, x0, H * 10)
    m_esq = (f(x0) - f(x0 - H)) / H
    tol = 1e-3 * (1 + abs(m1))
    if not finito(m1) or abs(m1 - m2) > tol:
        return False
    if finito(m_esq) and abs(m1 - m_esq) > tol:
        return False
    return True


def desenhar(f, x0, y0, m):
    n = 60
    xmin = x0 - 5
    xmax = x0 + 5
    passo = (xmax - xmin) / n

    pts = []
    for i in range(n + 1):
        xi = xmin + i * passo
        try:
            yi = f(xi)
            if finito(yi):
                pts.append((xi, yi))
            else:
                pts.append(None)
        except Exception:
            pts.append(None)

    ys = sorted([p[1] for p in pts if p])
    if ys:
        lo = ys[int(len(ys) * 0.02)]
        hi = ys[min(len(ys) - 1, int(len(ys) * 0.98))]
    else:
        lo = y0 - 5
        hi = y0 + 5
    margem = (hi - lo) * 0.2
    if margem == 0:
        margem = 1

    plt.cls()
    plt.window(xmin, xmax, lo - margem, hi + margem)
    plt.axes("on")


    plt.color(0, 0, 255)
    ant = None
    for p in pts:
        if p and ant and abs(p[1] - ant[1]) <= (hi - lo) * 2 + 1:
            plt.line(ant[0], ant[1], p[0], p[1])
        ant = p

    
    plt.color(255, 0, 0)
    plt.line(xmin, m * (xmin - x0) + y0, xmax, m * (xmax - x0) + y0)

    
    plt.color(0, 0, 0)
    plt.plot(x0, y0, "o")
    plt.title("Funcao e reta tangente")
    plt.show_plot()


def main():
    print("Derivada com h/intervalo")

    txt = input("f(x) = ")
    f = criar_f(txt)
    x0 = float(criar_f(input("Ponto x0 = "))(0))
    mostrar = y_or_n("Mostrar grafico? (y/n): ")

    try:
        y0 = f(x0)
        m_bruto = declive_h(f, x0)
        existe = derivada_existe(f, x0)
        if not (existe and finito(y0) and finito(m_bruto)):
            raise ValueError
    except Exception:
        print("Erro: a funcao nao e diferenciavel ou nao esta definida neste ponto")
        return

    m = round(m_bruto, 4)
    if m == int(m):
        m = int(m)
    b = y0 - m * x0

    sinal = "+" if b >= 0 else "-"

    print("--- Resultados ---")
    print("f(x0)  = %g" % y0)
    print("f'(x0) = %g" % m)
    print("y = %g*(x - %g) + %g" % (m, x0, y0))
    print("y = %g*x %s %g" % (m, sinal, abs(b)))

    if mostrar:
        desenhar(f, x0, y0, m)


main()