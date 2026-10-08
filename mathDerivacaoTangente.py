"""
Reta tangente usando a derivada com h.

    f'(x0) ≈ (f(x0 + h) - f(x0)) / h
    Com h (intervalo) aproximadamente igual a 0 

- O declive m é calculado com o quociente acima (h = x0)
- Reta tangente: y = m * (x - x0) + f(x0)
- Desenha a função e a tangente no mesmo gráfico (opcional)
"""

import numpy as np
import matplotlib.pyplot as plt
import sympy as sp
from sympy.parsing.sympy_parser import (
    parse_expr,
    standard_transformations,
    implicit_multiplication_application,
    convert_xor,
)

x = sp.symbols("x")
TRANSFORMACOES = standard_transformations + (
    implicit_multiplication_application,
    convert_xor,
)

H = 1e-8


def ler_expressao(texto):
    return parse_expr(texto, local_dict={"x": x}, transformations=TRANSFORMACOES)


def declive_h(f, x0, h=H):
    """Quociente de diferenças: (f(x0 + h) - f(x0)) / h"""
    return (f(x0 + h) - f(x0)) / h


def y_or_n(pergunta):
    while True:
        resposta = input(pergunta).strip().lower()
        if resposta in ("y", "yes", "s", "sim"):
            return True
        if resposta in ("n", "no", "nao", "não"):
            return False
        print("Responde com y ou n.")


def derivada_existe(f, x0):
    """Verifica se o declive estabiliza quando h diminui"""
    m1 = declive_h(f, x0, H)
    m2 = declive_h(f, x0, H * 10)
    m_esq = (f(x0) - f(x0 - H)) / H
    tol = 1e-3 * (1 + abs(m1))
    if not np.isfinite(m1) or abs(m1 - m2) > tol:
        return False
    if np.isfinite(m_esq) and abs(m1 - m_esq) > tol:
        return False
    return True


def desenhar(f, expr, tangente, x0, y0, m):
    xs = np.linspace(x0 - 5, x0 + 5, 800)
    with np.errstate(all="ignore"):
        ys_f = np.asarray(f(xs), dtype=float) * np.ones_like(xs)
    ys_t = m * (xs - x0) + y0

    plt.figure(figsize=(8, 6))
    plt.plot(xs, ys_f, label=f"f(x) = {expr}", linewidth=2)
    plt.plot(xs, ys_t, "--", label=f"tangente: y = {tangente}", linewidth=2)
    plt.scatter([x0], [y0], color="red", zorder=5,
                label=f"ponto ({x0:g}, {y0:g}),  m = {m:g}")

    # Limita o eixo y para funções que "explodem" (ex.: 1/x, tan(x))
    validos = ys_f[np.isfinite(ys_f)]
    if validos.size:
        baixo, alto = np.percentile(validos, [2, 98])
        margem = (alto - baixo) * 0.2 or 1
        plt.ylim(baixo - margem, alto + margem)

    plt.axhline(0, color="black", linewidth=0.8)
    plt.axvline(0, color="black", linewidth=0.8)
    plt.grid(True, alpha=0.3)
    plt.xlabel("x")
    plt.ylabel("y")
    plt.title("Função e reta tangente")
    plt.legend()
    plt.show()


def main():
    print(" Derivada com h/intervalo !!!")

    expr = ler_expressao(input("f(x) = "))
    x0 = ler_expressao(input("Ponto x0 = "))
    mostrar_grafico = y_or_n("Mostrar gráfico? (y/n): ")

    f = sp.lambdify(x, expr, "numpy")
    x0_num = float(x0.evalf())

    # Valor da função e declive
    y0 = sp.simplify(expr.subs(x, x0))
    try:
        with np.errstate(all="ignore"):
            m_bruto = float(declive_h(f, x0_num))
    except (ZeroDivisionError, ValueError, TypeError):
        m_bruto = float("nan")

    try:
        with np.errstate(all="ignore"):
            existe = derivada_existe(f, x0_num)
    except (ZeroDivisionError, ValueError, TypeError):
        existe = False

    if not existe or not np.isfinite(m_bruto) or not y0.is_real or y0.has(sp.zoo, sp.oo, sp.nan):
        print("Erro: a função não é diferenciável ou não está definida neste ponto; não está presente no intervalo")
        return

    
    m_arred = round(m_bruto, 4) + 0.0
    m = sp.Integer(int(m_arred)) if m_arred == int(m_arred) else sp.Float(m_arred, 5)

    f_linha = sp.diff(expr, x)
    tangente = sp.simplify(m * (x - x0) + y0)

    print("\n--- Resultados ---")
    print(f"Função:              f(x)  = {expr}")
    print(f"Derivada:            f'(x) = {f_linha}")
    print(f"Valor da função:     f({x0}) = {y0}")
    print(f"Declive (derivada):  f'({x0}) = {m}")
    print(f"Reta tangente:       y = {m}*(x - {x0}) + {y0}")
    print(f"Simplificada:        y = {tangente}")

    if mostrar_grafico:
        desenhar(f, expr, tangente, x0_num, float(y0), float(m))


if __name__ == "__main__":
    main()