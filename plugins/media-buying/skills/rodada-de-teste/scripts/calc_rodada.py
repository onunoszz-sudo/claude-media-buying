"""Tamanho de uma rodada de teste de criativos pela verba.
Test round size from the budget.

Cada anuncio precisa gastar pelo menos a linha de MATAR da conta para ser julgado. Entao:
  anuncios na janela = verba diaria x dias da janela / linha de MATAR (arredondado para baixo).
Each ad must spend at least the account's KILL line to be judged, so:
  ads per window = daily budget x window days / KILL line (rounded down).

Uso / usage:
  python calc_rodada.py --verba-diaria 5 --dias 7 --linha-matar 13.87 --moeda US$
  python calc_rodada.py --daily-budget 500 --days 7 --kill-line 120 --lang en --currency $
  opcional / optional:
    --hooks-por-angulo 3   anuncios por angulo (padrao 3) / ads per angle (default 3)
    --conjuntos 2          conjuntos ABO: a verba e dividida por igual / ABO ad sets, budget split evenly
"""
import argparse
import math
import sys

T = {
    "pt": {
        "titulo": "### Tamanho da rodada de teste",
        "conta": "Verba da janela: {v} por dia x {d} dias = {tot}. Linha de MATAR: {k} por anuncio.",
        "res": "**Anuncios que cabem na janela: {n}** ({tot} / {k} = {raz}, arredondado para baixo).",
        "angulos": "Com {h} hooks por angulo: {a} angulo(s) completo(s).",
        "um_hook": "Nao cabe um angulo completo: teste 1 hook por angulo ({n} angulo(s)) e deixe as variacoes de hook "
                   "para o vencedor.",
        "conj": "Em {c} conjuntos ABO: {vc} por dia em cada; cada conjunto comporta {nc} anuncio(s) na janela.",
        "zero": "**Nenhum anuncio cabe na janela.** Aumente a janela para {dmin} dias ou a verba para {vmin} por dia "
                "para testar 1 anuncio.",
        "dias_um": "Um anuncio sozinho leva {d1} dia(s) para chegar a linha de MATAR com toda a verba.",
        "e_pos": "ERRO: verba, dias e linha de MATAR precisam ser maiores que zero.",
    },
    "en": {
        "titulo": "### Test round size",
        "conta": "Window budget: {v} a day x {d} days = {tot}. KILL line: {k} per ad.",
        "res": "**Ads that fit in the window: {n}** ({tot} / {k} = {raz}, rounded down).",
        "angulos": "With {h} hooks per angle: {a} full angle(s).",
        "um_hook": "No full angle fits: test 1 hook per angle ({n} angle(s)) and keep hook variations for the winner.",
        "conj": "Across {c} ABO ad sets: {vc} a day each; each ad set fits {nc} ad(s) in the window.",
        "zero": "**No ad fits in the window.** Extend the window to {dmin} days or the budget to {vmin} a day to "
                "test 1 ad.",
        "dias_um": "A single ad needs {d1} day(s) to reach the KILL line with the full budget.",
        "e_pos": "ERROR: budget, days and KILL line must be greater than zero.",
    },
}

LANG, MOEDA = "pt", "R$"


def din(v):
    s = f"{abs(v):,.2f}"
    sinal = "-" if v < 0 else ""
    if LANG == "pt":
        return f"{sinal}{MOEDA} " + s.replace(",", "X").replace(".", ",").replace("X", ".")
    return f"{sinal}{MOEDA}{s}"


def main():
    global LANG, MOEDA
    ap = argparse.ArgumentParser()
    ap.add_argument("--verba-diaria", "--daily-budget", dest="verba", type=float, required=True)
    ap.add_argument("--dias", "--days", dest="dias", type=int, required=True)
    ap.add_argument("--linha-matar", "--kill-line", dest="matar", type=float, required=True)
    ap.add_argument("--hooks-por-angulo", "--hooks-per-angle", dest="hooks", type=int, default=3)
    ap.add_argument("--conjuntos", "--ad-sets", dest="conjuntos", type=int, default=1)
    ap.add_argument("--lang", choices=["pt", "en"], default="pt")
    ap.add_argument("--moeda", "--currency", dest="moeda")
    a = ap.parse_args()
    LANG = a.lang
    MOEDA = a.moeda or ("R$" if LANG == "pt" else "$")
    tr = T[LANG]
    if a.verba <= 0 or a.dias <= 0 or a.matar <= 0 or a.hooks <= 0 or a.conjuntos <= 0:
        sys.exit(tr["e_pos"])

    total = a.verba * a.dias
    razao = total / a.matar
    n = math.floor(razao)
    out = [tr["titulo"], "", tr["conta"].format(v=din(a.verba), d=a.dias, tot=din(total), k=din(a.matar)), ""]
    if n == 0:
        out.append(tr["zero"].format(dmin=math.ceil(a.matar / a.verba), vmin=din(a.matar / a.dias)))
    else:
        raz = f"{razao:.2f}".replace(".", ",") if LANG == "pt" else f"{razao:.2f}"
        out.append(tr["res"].format(n=n, tot=din(total), k=din(a.matar), raz=raz))
        out.append(tr["angulos"].format(h=a.hooks, a=n // a.hooks))
        if n // a.hooks == 0:
            out.append(tr["um_hook"].format(n=n))
        if a.conjuntos > 1:
            vc = a.verba / a.conjuntos
            out.append(tr["conj"].format(c=a.conjuntos, vc=din(vc), nc=math.floor(vc * a.dias / a.matar)))
    out.append(tr["dias_um"].format(d1=math.ceil(a.matar / a.verba)))
    print("\n".join(out))


if __name__ == "__main__":
    main()
