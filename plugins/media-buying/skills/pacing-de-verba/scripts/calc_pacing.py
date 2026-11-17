"""Pacing de verba de um portfolio de contas: ritmo do gasto contra o orcamento do periodo.
Budget pacing for a portfolio of ad accounts: spend pace against the period budget.

Uso / usage:
  python calc_pacing.py portfolio.csv --hoje 2026-10-28
  python calc_pacing.py portfolio.csv --as-of 2026-10-28 --lang en --currency $

CSV (cabecalho em PT ou EN / header in PT or EN; uma linha por conta e plataforma):
  conta|account, plataforma|platform, orcamento|budget, gasto|spend_to_date,
  inicio|start, fim|end  (AAAA-MM-DD, periodo inclusivo / inclusive flight dates)
  opcionais / optional:
  diario_atual|current_daily       orcamento diario configurado hoje (senao usa o ritmo medio)
  planejado_ate_hoje|planned_to_date  gasto planejado ate ontem (curva sazonal); senao linear

"gasto" e o gasto ate ONTEM (dias completos). "hoje" conta como dia restante.
"""
import argparse
import csv
import math
import sys
from datetime import date, timedelta

COLS = {
    "conta": ["conta", "account"], "plataforma": ["plataforma", "platform"],
    "orcamento": ["orcamento", "budget"], "gasto": ["gasto", "spend_to_date", "spend"],
    "inicio": ["inicio", "start"], "fim": ["fim", "end"],
    "diario": ["diario_atual", "current_daily"], "planejado": ["planejado_ate_hoje", "planned_to_date"],
}
TOL = 0.10      # NO RITMO / ON PACE: projecao a +-10% do orcamento / projection within +-10% of budget
PASSO = 0.20    # passo maximo de verba / max budget step
CLIENTE = 0.50  # acima disso a correcao e decisao do cliente / above this, client decision

T = {
    "pt": {
        "titulo": "### Pacing do portfolio em {d} ({n} contas)",
        "cab": "| Conta | Plataforma | Orcamento | Gasto ate ontem | Esperado ate ontem | Pace | Projecao do fim | Desvio | Diario atual | Diario recomendado | Status |",
        "st": {"ok": "NO RITMO", "abaixo": "ABAIXO", "acima": "ACIMA", "estoura": "ESTOURA"},
        "acoes": "### Acoes para aprovar (maior desvio em dinheiro primeiro)",
        "a_ok": "{c} ({p}): manter (projecao dentro de 10% do orcamento). Pace {pace}; diario exato para fechar no orcamento: {para}.",
        "a_mudar": "{c} ({p}): diario de {de} para {para} ({var}){passos}.",
        "a_passos": "; acima de 20%: em {n} passos de ate 20%, a cada 48 h",
        "a_cliente": " **Decisao do cliente/gestor: correcao maior que 50%.**",
        "a_tarde": " Nao da tempo de chegar so com passos de 20% ate o fim do periodo: subir o que der e avisar do subgasto.",
        "a_esgotou": "{c} ({p}): **orcamento do periodo ja gasto** ({g} de {o}). Pausar ou pedir aumento ao cliente.",
        "a_esgota": "{c} ({p}): no ritmo atual o orcamento acaba em {d}, antes do fim ({f}). Baixar o diario para {para}.",
        "notas": "Lembretes de plataforma: o Google pode gastar ate 2x o diario num dia, mas cobra no maximo 30,4x o "
                 "diario medio no mes; a Meta pode passar ate 75% do diario num dia, sem passar de 7x o diario na semana. "
                 "Por isso o diario configurado nao e teto exato.",
        "e_col": "ERRO: coluna obrigatoria ausente no CSV: {c}",
        "e_lin": "ERRO na linha {i}: {e}",
        "linear": "linear", "plan": "planejado",
    },
    "en": {
        "titulo": "### Portfolio pacing as of {d} ({n} accounts)",
        "cab": "| Account | Platform | Budget | Spend to date | Expected to date | Pace | Projected EOP | Variance | Current daily | Recommended daily | Status |",
        "st": {"ok": "ON PACE", "abaixo": "UNDER", "acima": "OVER", "estoura": "OVERSPEND"},
        "acoes": "### Actions to approve (largest dollar variance first)",
        "a_ok": "{c} ({p}): hold (projection within 10% of budget). Pace {pace}; exact daily to land on budget: {para}.",
        "a_mudar": "{c} ({p}): daily from {de} to {para} ({var}){passos}.",
        "a_passos": "; over 20%: in {n} steps of up to 20%, 48 h apart",
        "a_cliente": " **Client/lead decision: correction above 50%.**",
        "a_tarde": " 20% steps cannot get there before the flight ends: raise what you can and flag the underspend.",
        "a_esgotou": "{c} ({p}): **flight budget already spent** ({g} of {o}). Pause or ask the client for more budget.",
        "a_esgota": "{c} ({p}): at the current rate the budget runs out on {d}, before the end ({f}). Lower the daily to {para}.",
        "notas": "Platform reminders: Google can spend up to 2x the daily budget on a given day but bills at most 30.4x "
                 "the average daily budget per month; Meta can spend up to 75% over the daily budget on a given day but "
                 "not more than 7x the daily budget in a week. The daily setting is not an exact cap.",
        "e_col": "ERROR: required CSV column missing: {c}",
        "e_lin": "ERROR on row {i}: {e}",
        "linear": "linear", "plan": "planned",
    },
}

LANG, MOEDA = "pt", "R$"


def din(v):
    sinal = "-" if v < 0 else ""
    s = f"{abs(v):,.2f}"
    if LANG == "pt":
        return f"{sinal}{MOEDA} " + s.replace(",", "X").replace(".", ",").replace("X", ".")
    return f"{sinal}{MOEDA}{s}"


def pct(v, sinal=False):
    s = f"{v * 100:+.0f}%" if sinal else f"{v * 100:.0f}%"
    return s


def col(row, chave):
    for nome in COLS[chave]:
        if nome in row and str(row[nome]).strip() != "":
            return row[nome].strip()
    return None


def fnum(v):
    return float(str(v).replace(",", ".")) if v is not None else None


def analisar(row, hoje):
    o, g = fnum(col(row, "orcamento")), fnum(col(row, "gasto"))
    ini, fim = date.fromisoformat(col(row, "inicio")), date.fromisoformat(col(row, "fim"))
    total = (fim - ini).days + 1
    passados = max(0, min(total, (hoje - ini).days))
    restantes = total - passados
    plan = fnum(col(row, "planejado"))
    esperado = plan if plan is not None else o * passados / total
    ritmo = g / passados if passados else 0.0
    diario = fnum(col(row, "diario")) or ritmo
    projecao = g + diario * restantes
    rec = (o - g) / restantes if restantes else 0.0
    pace = g / esperado if esperado else (1.0 if g == 0 else float("inf"))
    esgota = None
    if diario > 0 and g < o:
        dias_ate_acabar = (o - g) / diario
        if dias_ate_acabar < restantes:
            esgota = hoje + timedelta(days=math.floor(dias_ate_acabar))
    razao = projecao / o if o else 0.0
    if g >= o:
        st = "estoura"
    elif razao > 1 + TOL:
        st = "acima"
    elif razao < 1 - TOL:
        st = "abaixo"
    else:
        st = "ok"
    return dict(conta=col(row, "conta"), plat=col(row, "plataforma"), o=o, g=g, esperado=esperado, pace=pace,
                projecao=projecao, desvio=projecao - o, diario=diario, rec=max(rec, 0.0), st=st,
                restantes=restantes, fim=fim, hoje=hoje, esgota=esgota)


def acao(r):
    tr = T[LANG]
    c, p = r["conta"], r["plat"]
    if r["g"] >= r["o"]:
        return tr["a_esgotou"].format(c=c, p=p, g=din(r["g"]), o=din(r["o"]))
    if r["st"] == "ok":
        return tr["a_ok"].format(c=c, p=p, pace=pct(r["pace"]), para=din(r["rec"]))
    if r["st"] == "acima" and r["esgota"] is not None:
        return tr["a_esgota"].format(c=c, p=p, d=r["esgota"].isoformat(), f=r["fim"].isoformat(), para=din(r["rec"]))
    var = r["rec"] / r["diario"] - 1 if r["diario"] else float("inf")
    passos, extra = "", ""
    if abs(var) > PASSO and r["diario"]:
        n = math.ceil(abs(math.log(r["rec"] / r["diario"]) / math.log(1 + PASSO))) if r["rec"] > 0 else 1
        passos = tr["a_passos"].format(n=n)
        if var > 0 and (n - 1) * 2 >= r["restantes"]:
            extra += tr["a_tarde"]
    if abs(var) > CLIENTE:
        extra += tr["a_cliente"]
    var_txt = pct(var, sinal=True) if math.isfinite(var) else "n/a"
    return tr["a_mudar"].format(c=c, p=p, de=din(r["diario"]), para=din(r["rec"]), var=var_txt, passos=passos) + extra


def main():
    global LANG, MOEDA
    ap = argparse.ArgumentParser()
    ap.add_argument("csv")
    ap.add_argument("--hoje", "--as-of", dest="hoje", default=date.today().isoformat())
    ap.add_argument("--lang", choices=["pt", "en"], default="pt")
    ap.add_argument("--moeda", "--currency", dest="moeda")
    a = ap.parse_args()
    LANG = a.lang
    MOEDA = a.moeda or ("R$" if LANG == "pt" else "$")
    tr = T[LANG]
    hoje = date.fromisoformat(a.hoje)

    with open(a.csv, encoding="utf-8-sig", newline="") as f:
        linhas = list(csv.DictReader(f))
    if not linhas:
        sys.exit(tr["e_lin"].format(i=0, e="CSV vazio / empty"))
    for chave in ("conta", "plataforma", "orcamento", "gasto", "inicio", "fim"):
        if not any(n in linhas[0] for n in COLS[chave]):
            sys.exit(tr["e_col"].format(c="|".join(COLS[chave])))
    res = []
    for i, row in enumerate(linhas, start=2):
        try:
            res.append(analisar(row, hoje))
        except (ValueError, TypeError) as e:
            sys.exit(tr["e_lin"].format(i=i, e=e))
    res.sort(key=lambda r: -abs(r["desvio"]))

    out = [tr["titulo"].format(d=hoje.isoformat(), n=len(res)), "", tr["cab"], "|" + "---|" * 11]
    for r in res:
        out.append(f"| {r['conta']} | {r['plat']} | {din(r['o'])} | {din(r['g'])} | {din(r['esperado'])} | "
                   f"{pct(r['pace']) if math.isfinite(r['pace']) else 'n/a'} | {din(r['projecao'])} | "
                   f"{din(r['desvio'])} | {din(r['diario'])} | {din(r['rec'])} | {tr['st'][r['st']]} |")
    out += ["", tr["acoes"], ""]
    out += [f"{i}. {acao(r)}" for i, r in enumerate(res, start=1)]
    out += ["", tr["notas"]]
    print("\n".join(out))


if __name__ == "__main__":
    main()
