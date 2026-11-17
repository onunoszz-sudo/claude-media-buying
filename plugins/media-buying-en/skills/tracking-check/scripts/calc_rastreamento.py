"""Conferencia de rastreamento: compras do pixel x vendas reais, dia a dia.
Tracking check: pixel purchases vs real sales, day by day.

Entrada: um CSV com uma linha por dia. Colunas (cabecalho em PT ou EN):
Input: a CSV with one row per day. Columns (PT or EN header):
  data | date                         AAAA-MM-DD
  reais | real                        vendas reais na fonte de verdade / real sales in the source of truth
  atribuidas | attributed             compras do pixel no Gerenciador / pixel purchases in Ads Manager
  valor_atribuido | attributed_value  (opcional) valor dessas compras / (optional) their value
  valor_real | real_value             (opcional) valor que as vendas reais deveriam mandar ao pixel (ex.: liquido da Hotmart)
                                      (optional) value the real sales should send to the pixel (e.g. Hotmart net)
  recebidos_navegador | raw_web       (opcional) eventos Purchase recebidos pelo navegador / (optional) browser events received
  recebidos_servidor | raw_server     (opcional) eventos Purchase recebidos pelo servidor / (optional) server events received

Uso / usage:
  python calc_rastreamento.py dias.csv --menor-valor 3.47 --moeda US$
  python calc_rastreamento.py days.csv --lowest-value 3.47 --currency $ --lang en
  --menor-valor / --lowest-value: menor valor que uma venda real manda ao pixel (ex.: o bump liquido).
  Com valor_atribuido e valor_real, as compras a mais de um dia que nao trazem pelo menos metade desse
  valor contam como "sem valor". / Lowest value a real sale sends to the pixel. With attributed_value and
  real_value, a day's extra purchases that don't bring at least half of it count as "no value".
"""
import argparse
import csv
import sys

ALIASES = {
    "data": "data", "date": "data",
    "reais": "reais", "real": "reais",
    "atribuidas": "atrib", "attributed": "atrib",
    "valor_atribuido": "valor", "attributed_value": "valor",
    "valor_real": "vreal", "real_value": "vreal",
    "recebidos_navegador": "web", "raw_web": "web",
    "recebidos_servidor": "srv", "raw_server": "srv",
}

T = {
    "pt": {
        "tit": "### Conferencia de rastreamento",
        "cab": "| Dia | Reais | Atribuidas | Casamento | Valor atribuido | A mais sem valor | Recebidos nav. | Recebidos serv. |",
        "tot": "**Total {a} a {b}:** {r} vendas reais, {p} compras atribuidas, casamento **{m}**.",
        "sv": "Compras a mais sem valor: **{n}** ({pct} das atribuidas). Valor medio por compra atribuida: {vm}.",
        "vr": "Valor atribuido {va} contra valor real {vr} (diferenca de {d}).",
        "raw": "Eventos recebidos: {w} pelo navegador e {s} pelo servidor, {t} no total = {x} por venda real "
               "(com navegador e servidor ligados e deduplicando, o esperado fica perto de 2).",
        "cob": "Cobertura do servidor: {c} dos eventos do navegador (a Meta recomenda 75% ou mais).",
        "sem": "Ultimos 7 dias: casamento {u}; 7 dias antes: {a}.",
        "queda": "ALERTA: o casamento caiu {d} pontos de uma semana para a outra.",
        "acima": "LEITURA: acima de 100% o pixel conta venda que nao existe (ou conta a mesma venda duas vezes).",
        "abaixo": "LEITURA: abaixo de 80% o pixel esta perdendo vendas.",
        "faixa": "LEITURA: casamento dentro da faixa normal (80% a 105%).",
        "ver": "**Seguro para julgar anuncio: {v}.**",
        "sim": "SIM", "ress": "COM RESSALVA", "nao": "NAO",
        "e_col": "ERRO: faltam colunas obrigatorias (data, reais, atribuidas). Achei: {c}",
        "e_vazio": "ERRO: nenhuma linha com dados.",
        "nd": "n/d",
    },
    "en": {
        "tit": "### Tracking check",
        "cab": "| Day | Real | Attributed | Match | Attributed value | Extra, no value | Received web | Received server |",
        "tot": "**Total {a} to {b}:** {r} real sales, {p} attributed purchases, match **{m}**.",
        "sv": "Extra purchases with no value: **{n}** ({pct} of attributed). Average value per attributed purchase: {vm}.",
        "vr": "Attributed value {va} vs real value {vr} (a {d} difference).",
        "raw": "Events received: {w} from the browser and {s} from the server, {t} in total = {x} per real sale "
               "(with browser and server both on and deduplicating, expect about 2).",
        "cob": "Server coverage: {c} of browser events (Meta recommends 75% or more).",
        "sem": "Last 7 days: match {u}; the 7 days before: {a}.",
        "queda": "ALERT: match fell {d} points from one week to the next.",
        "acima": "READ: above 100% the pixel counts sales that don't exist (or counts the same sale twice).",
        "abaixo": "READ: below 80% the pixel is missing sales.",
        "faixa": "READ: match within the normal range (80% to 105%).",
        "ver": "**Safe to judge ads: {v}.**",
        "sim": "YES", "ress": "WITH A CAVEAT", "nao": "NO",
        "e_col": "ERROR: missing required columns (date, real, attributed). Found: {c}",
        "e_vazio": "ERROR: no data rows.",
        "nd": "n/a",
    },
}


def num(x):
    x = (x or "").strip().replace(",", ".")
    return float(x) if x else None


def pct(a, b, t):
    return f"{a / b * 100:.0f}%" if b else t["nd"]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("csv")
    ap.add_argument("--menor-valor", "--lowest-value", dest="menor", type=float, default=None)
    ap.add_argument("--moeda", "--currency", dest="moeda", default="")
    ap.add_argument("--lang", default="pt", choices=["pt", "en"])
    a = ap.parse_args()
    t = T[a.lang]
    m = lambda v: f"{a.moeda} {v:.2f}".strip()

    with open(a.csv, encoding="utf-8-sig", newline="") as f:
        rd = csv.DictReader(f)
        cols = {h: ALIASES.get(h.strip().lower()) for h in rd.fieldnames or []}
        if not {"data", "reais", "atrib"} <= set(cols.values()):
            sys.exit(t["e_col"].format(c=", ".join(rd.fieldnames or [])))
        rows = []
        for r in rd:
            d = {cols[k]: v for k, v in r.items() if cols.get(k)}
            if not (d.get("data") or "").strip():
                continue
            rows.append({"data": d["data"].strip(), "reais": num(d.get("reais")) or 0,
                         "atrib": num(d.get("atrib")) or 0, "valor": num(d.get("valor")), "vreal": num(d.get("vreal")),
                         "web": num(d.get("web")), "srv": num(d.get("srv"))})
    if not rows:
        sys.exit(t["e_vazio"])
    rows.sort(key=lambda r: r["data"])

    print(t["tit"]), print(), print(t["cab"]), print("|---|---|---|---|---|---|---|---|")
    sv_total = 0
    for r in rows:
        sv = None
        if a.menor and r["valor"] is not None and r["vreal"] is not None:
            extra = int(r["atrib"] - r["reais"])
            sv = extra if extra > 0 and (r["valor"] - r["vreal"]) < 0.5 * a.menor * extra else 0
            sv_total += sv
        cel = lambda v: t["nd"] if v is None else f"{v:g}"
        print(f"| {r['data']} | {r['reais']:g} | {r['atrib']:g} | {pct(r['atrib'], r['reais'], t)} | "
              f"{t['nd'] if r['valor'] is None else m(r['valor'])} | {cel(sv)} | {cel(r['web'])} | {cel(r['srv'])} |")
    print()

    R = sum(r["reais"] for r in rows)
    P = sum(r["atrib"] for r in rows)
    match = P / R if R else None
    print(t["tot"].format(a=rows[0]["data"], b=rows[-1]["data"], r=f"{R:g}", p=f"{P:g}", m=pct(P, R, t)))

    tem_valor = all(r["valor"] is not None and r["vreal"] is not None for r in rows)
    if a.menor and tem_valor:
        V = sum(r["valor"] for r in rows)
        VR = sum(r["vreal"] for r in rows)
        print(t["sv"].format(n=sv_total, pct=pct(sv_total, P, t), vm=m(V / P) if P else t["nd"]))
        print(t["vr"].format(va=m(V), vr=m(VR), d=pct(V - VR, VR, t)))

    if all(r["web"] is not None and r["srv"] is not None for r in rows):
        W = sum(r["web"] for r in rows)
        S = sum(r["srv"] for r in rows)
        print(t["raw"].format(w=f"{W:g}", s=f"{S:g}", t=f"{W + S:g}", x=f"{(W + S) / R:.1f}" if R else t["nd"]))
        print(t["cob"].format(c=pct(S, W, t)))

    queda = 0
    if len(rows) >= 14:
        u, ant = rows[-7:], rows[-14:-7]
        mu = sum(r["atrib"] for r in u) / max(1, sum(r["reais"] for r in u))
        ma = sum(r["atrib"] for r in ant) / max(1, sum(r["reais"] for r in ant))
        print(t["sem"].format(u=f"{mu * 100:.0f}%", a=f"{ma * 100:.0f}%"))
        queda = (ma - mu) * 100
        if queda > 20:
            print(t["queda"].format(d=f"{queda:.0f}"))

    print()
    if match is None:
        ver = t["nao"]
    else:
        if match > 1.05:
            print(t["acima"])
        elif match < 0.8:
            print(t["abaixo"])
        else:
            print(t["faixa"])
        sv_frac = sv_total / P if (P and a.menor and tem_valor) else 0
        if 0.9 <= match <= 1.05 and sv_frac == 0 and queda <= 20:
            ver = t["sim"]
        elif 0.8 <= match <= 1.2 and sv_frac < 0.2 and queda <= 20:
            ver = t["ress"]
        else:
            ver = t["nao"]
    print(t["ver"].format(v=ver))


if __name__ == "__main__":
    main()
