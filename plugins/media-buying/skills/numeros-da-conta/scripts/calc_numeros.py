"""Calcula os numeros de decisao de uma conta de anuncios e imprime a conta aberta.
Computes an ad account's decision numbers and prints the math.

Uso / usage (taxas e margens como fracao / rates and margins as fractions, 0.40 = 40%):
  python calc_numeros.py venda-direta --ticket 150 --margem 0.40 --lucro 0.10
  python calc_numeros.py low-ticket --front 14.90 --item 7.90:0.10 --item 19.90:0.03 \
      --liquido-sobre-bruto 0.85 --reembolso 0.05 --lucro 0.20 --moeda US$
  python calc_numeros.py lead-crm --ticket 9000 --margem 0.45 --lucro 0.15 \
      --lead-venda 0.0125 --lead-mql 0.25 --lead-orcamento 0.075
  python calc_numeros.py hotel --lang en --currency $ --adr 220 --nights 2.6 \
      --cancellation 0.18 --ota-commission 0.18 --target-cos 0.12 --margin 0.70 --profit 0.25

Tipos / types: venda-direta | direct-sale, low-ticket, lead-crm, hotel
"""
import argparse
import sys

TIPOS = {"venda-direta": "venda-direta", "direct-sale": "venda-direta", "low-ticket": "low-ticket",
         "lead-crm": "lead-crm", "hotel": "hotel"}

T = {
    "pt": {
        "titulo": "### Numeros calculados ({tipo})",
        "be": "- ROAS de breakeven = 1 / {m} = **{v}**",
        "alvo": "- ROAS alvo = 1 / ({m} - {l}) = **{v}**",
        "mer": "- MER alvo (receita total / verba total) = **{v}**",
        "cpa_be": "- CPA maximo (breakeven) = {t} x {m} = **{v}**",
        "cpa_alvo": "- CPA alvo = {t} x ({m} - {l}) = **{v}**",
        "matar": "- MATAR sem venda depois de gastar 2x CPA alvo = **{v}**",
        "ticket_ef": "- Ticket efetivo = {f}{partes} = **{v}**",
        "margem_lt": "- Margem = {lb} liquido x (1 - {r} reembolso) - {o} outros = **{v}**",
        "base_lt": "- Base de receita: valor BRUTO das vendas (front + bump + upsell), antes de reembolso.",
        "cpl_max": "- CPL maximo = CPA maximo x taxa lead->venda {lv} = **{v}**",
        "cpl_alvo": "- CPL alvo = {c} x {lv} = **{v}**",
        "matar_lead": "- MATAR sem lead depois de gastar 2x CPL alvo = **{v}**",
        "custo_etapa": "- Custo alvo por {n} = {c} x ({lv} / {tx}) = **{v}**",
        "ciclo": "- Atencao: o ciclo de venda e longo; julgar CPL/MQL em 30 dias e receita/midia em 90.",
        "mql": "MQL", "orc": "orcamento",
        "h_reserva": "- Valor da reserva = diaria media {adr} x {n} noites = **{v}**",
        "h_real": "- Receita realizada por reserva = {b} x (1 - {c} cancelamento) = **{v}**",
        "h_ota": "**Lente OTA** (reserva direta contra a mesma reserva vinda pela OTA, comissao {c}):",
        "h_cos_max": "- Custo de venda maximo = comissao da OTA = **{v}** da receita realizada",
        "h_roas_min": "- ROAS minimo sobre receita realizada = 1 / {c} = **{v}**",
        "h_roas_min_plat": "- ROAS minimo na plataforma (receita reservada, antes do cancelamento) = 1 / ({c} x (1 - {k})) = **{v}**",
        "h_cpa_max": "- CPA maximo por reserva = {r} x {c} = **{v}**",
        "h_alvo": "**Alvo** (custo de venda alvo {t}):",
        "h_roas_alvo": "- ROAS alvo sobre receita realizada = 1 / {t} = **{v}**",
        "h_roas_alvo_plat": "- ROAS alvo na plataforma = 1 / ({t} x (1 - {k})) = **{v}**",
        "h_cpa_alvo": "- CPA alvo por reserva = {r} x {t} = **{v}**",
        "h_sem_alvo": "- Custo de venda alvo: FALTANDO (combinar com o hotel; abaixo da comissao da OTA)",
        "h_margem": "**Lente margem** (margem de contribuicao {m}, lucro desejado {l}):",
        "h_be_m": "- ROAS de breakeven sobre receita realizada = 1 / {m} = **{v}**",
        "h_cpa_max_m": "- CPA maximo por reserva = {r} x {m} = **{v}**",
        "h_cpa_alvo_m": "- CPA alvo por reserva = {r} x ({m} - {l}) = **{v}**",
        "h_aperta": "- Limite mais apertado: **{qual}** (CPA maximo {v})",
        "h_ota_nome": "OTA", "h_margem_nome": "margem",
        "h_matar": "- MATAR sem reserva depois de gastar 2x CPA alvo = **{v}**",
        "h_aviso": "- Atencao: a lente OTA so vale para reserva que viria pela OTA. Busca pela marca pode ser "
                   "deslocamento (viria direto de qualquer jeito), nao incremento: julgue marca e nao-marca separadas.",
        "h_cos_erro": "ERRO: custo de venda alvo ({t}) >= comissao da OTA ({c}); a reserva direta sairia mais cara que a OTA.",
        "e_margem": "ERRO: margem {m} fora de (0, 1]. Use fracao, ex.: 0.40",
        "e_lucro": "ERRO: lucro desejado ({l}) >= margem ({m}). Nao existe ROAS que entregue esse lucro; reduza o lucro desejado.",
        "e_lt": "ERRO: low-ticket precisa de --front e --liquido-sobre-bruto",
        "e_ticket": "ERRO: informe --ticket, --margem e --lucro",
        "e_lead": "ERRO: lead-crm precisa de --lead-venda",
        "e_hotel": "ERRO: hotel precisa de --adr, --noites e --comissao-ota",
    },
    "en": {
        "titulo": "### Decision numbers ({tipo})",
        "be": "- Break-even ROAS = 1 / {m} = **{v}**",
        "alvo": "- Target ROAS = 1 / ({m} - {l}) = **{v}**",
        "mer": "- Target MER (total revenue / total ad spend) = **{v}**",
        "cpa_be": "- Max CPA (break-even) = {t} x {m} = **{v}**",
        "cpa_alvo": "- Target CPA = {t} x ({m} - {l}) = **{v}**",
        "matar": "- KILL with no sale after spending 2x target CPA = **{v}**",
        "ticket_ef": "- Effective order value = {f}{partes} = **{v}**",
        "margem_lt": "- Margin = {lb} net x (1 - {r} refunds) - {o} other = **{v}**",
        "base_lt": "- Revenue basis: GROSS sales value (front + bump + upsell), before refunds.",
        "cpl_max": "- Max CPL = max CPA x lead-to-sale rate {lv} = **{v}**",
        "cpl_alvo": "- Target CPL = {c} x {lv} = **{v}**",
        "matar_lead": "- KILL with no lead after spending 2x target CPL = **{v}**",
        "custo_etapa": "- Target cost per {n} = {c} x ({lv} / {tx}) = **{v}**",
        "ciclo": "- Note: long sales cycle; judge CPL/MQL on 30 days and revenue/spend on 90.",
        "mql": "MQL", "orc": "quote",
        "h_reserva": "- Booking value = ADR {adr} x {n} nights = **{v}**",
        "h_real": "- Realized revenue per booking = {b} x (1 - {c} cancellations) = **{v}**",
        "h_ota": "**OTA lens** (direct booking vs. the same booking through an OTA at {c} commission):",
        "h_cos_max": "- Max cost of sale = OTA commission = **{v}** of realized revenue",
        "h_roas_min": "- Min ROAS on realized revenue = 1 / {c} = **{v}**",
        "h_roas_min_plat": "- Min in-platform ROAS (booked revenue, before cancellations) = 1 / ({c} x (1 - {k})) = **{v}**",
        "h_cpa_max": "- Max CPA per booking = {r} x {c} = **{v}**",
        "h_alvo": "**Target** (target cost of sale {t}):",
        "h_roas_alvo": "- Target ROAS on realized revenue = 1 / {t} = **{v}**",
        "h_roas_alvo_plat": "- Target in-platform ROAS = 1 / ({t} x (1 - {k})) = **{v}**",
        "h_cpa_alvo": "- Target CPA per booking = {r} x {t} = **{v}**",
        "h_sem_alvo": "- Target cost of sale: MISSING (agree with the hotel; it must sit below the OTA commission)",
        "h_margem": "**Margin lens** (contribution margin {m}, target profit {l}):",
        "h_be_m": "- Break-even ROAS on realized revenue = 1 / {m} = **{v}**",
        "h_cpa_max_m": "- Max CPA per booking = {r} x {m} = **{v}**",
        "h_cpa_alvo_m": "- Target CPA per booking = {r} x ({m} - {l}) = **{v}**",
        "h_aperta": "- Tighter limit: **{qual}** (max CPA {v})",
        "h_ota_nome": "OTA", "h_margem_nome": "margin",
        "h_matar": "- KILL with no booking after spending 2x target CPA = **{v}**",
        "h_aviso": "- Note: the OTA lens only holds for bookings that would otherwise come through an OTA. Brand "
                   "search can be displacement (they would book direct anyway), not incremental: judge brand and non-brand separately.",
        "h_cos_erro": "ERROR: target cost of sale ({t}) >= OTA commission ({c}); a direct booking would cost more than the OTA.",
        "e_margem": "ERROR: margin {m} outside (0, 1]. Use a fraction, e.g. 0.40",
        "e_lucro": "ERROR: target profit ({l}) >= margin ({m}). No ROAS delivers that profit; lower the target profit.",
        "e_lt": "ERROR: low-ticket needs --front and --net-to-gross",
        "e_ticket": "ERROR: provide --ticket, --margin and --profit",
        "e_lead": "ERROR: lead-crm needs --lead-to-sale",
        "e_hotel": "ERROR: hotel needs --adr, --nights and --ota-commission",
    },
}

LANG = "pt"
MOEDA = "R$"


def t(chave, **kw):
    return T[LANG][chave].format(**kw)


def din(v):
    s = f"{v:,.2f}"
    if LANG == "pt":
        s = s.replace(",", "X").replace(".", ",").replace("X", ".")
    return f"{MOEDA} {s}" if LANG == "pt" else f"{MOEDA}{s}"


def x(v):
    s = f"{v:.2f}x"
    return s.replace(".", ",") if LANG == "pt" else s


def pct(v):
    casas = 2 if abs(v) < 0.1 else 1
    s = f"{v * 100:.{casas}f}%"
    return s.replace(".", ",") if LANG == "pt" else s


def num(v):
    s = f"{v:g}"
    return s.replace(".", ",") if LANG == "pt" else s


def checar_margem(m, lucro):
    if not 0 < m <= 1:
        sys.exit(t("e_margem", m=m))
    if lucro >= m:
        sys.exit(t("e_lucro", l=pct(lucro), m=pct(m)))


def bloco_roas(ticket, m, lucro, linhas, regra_matar=True):
    cpa_be = ticket * m
    cpa_alvo = ticket * (m - lucro)
    linhas += [
        t("be", m=pct(m), v=x(1 / m)),
        t("alvo", m=pct(m), l=pct(lucro), v=x(1 / (m - lucro))),
        t("mer", v=x(1 / (m - lucro))),
        t("cpa_be", t=din(ticket), m=pct(m), v=din(cpa_be)),
        t("cpa_alvo", t=din(ticket), m=pct(m), l=pct(lucro), v=din(cpa_alvo)),
    ]
    if regra_matar:
        linhas.append(t("matar", v=din(2 * cpa_alvo)))
    return cpa_be, cpa_alvo


def hotel(a, linhas):
    if a.adr is None or a.noites is None or a.comissao_ota is None:
        sys.exit(t("e_hotel"))
    c, k = a.comissao_ota, a.cancelamento
    reserva = a.adr * a.noites
    real = reserva * (1 - k)
    linhas += [
        t("h_reserva", adr=din(a.adr), n=num(a.noites), v=din(reserva)),
        t("h_real", b=din(reserva), c=pct(k), v=din(real)),
        "",
        t("h_ota", c=pct(c)),
        t("h_cos_max", v=pct(c)),
        t("h_roas_min", c=pct(c), v=x(1 / c)),
        t("h_roas_min_plat", c=pct(c), k=pct(k), v=x(1 / (c * (1 - k)))),
        t("h_cpa_max", r=din(real), c=pct(c), v=din(real * c)),
    ]
    if a.cos_alvo:
        if a.cos_alvo >= c:
            sys.exit(t("h_cos_erro", t=pct(a.cos_alvo), c=pct(c)))
        ta = a.cos_alvo
        linhas += [
            "",
            t("h_alvo", t=pct(ta)),
            t("h_roas_alvo", t=pct(ta), v=x(1 / ta)),
            t("h_roas_alvo_plat", t=pct(ta), k=pct(k), v=x(1 / (ta * (1 - k)))),
            t("h_cpa_alvo", r=din(real), t=pct(ta), v=din(real * ta)),
            t("h_matar", v=din(2 * real * ta)),
        ]
    else:
        linhas.append(t("h_sem_alvo"))
    limites = [(t("h_ota_nome"), real * c)]
    if a.margem is not None:
        lucro = a.lucro or 0.0
        checar_margem(a.margem, lucro)
        linhas += [
            "",
            t("h_margem", m=pct(a.margem), l=pct(lucro)),
            t("h_be_m", m=pct(a.margem), v=x(1 / a.margem)),
            t("h_cpa_max_m", r=din(real), m=pct(a.margem), v=din(real * a.margem)),
            t("h_cpa_alvo_m", r=din(real), m=pct(a.margem), l=pct(lucro), v=din(real * (a.margem - lucro))),
        ]
        limites.append((t("h_margem_nome"), real * a.margem))
    qual, v = min(limites, key=lambda z: z[1])
    linhas += ["", t("h_aperta", qual=qual, v=din(v)), t("h_aviso")]


def main():
    p = argparse.ArgumentParser()
    p.add_argument("tipo", choices=sorted(TIPOS))
    p.add_argument("--lang", choices=["pt", "en"], default="pt")
    p.add_argument("--moeda", "--currency", dest="moeda", default=None)
    p.add_argument("--ticket", type=float)
    p.add_argument("--margem", "--margin", dest="margem", type=float)
    p.add_argument("--lucro", "--profit", dest="lucro", type=float)
    # low-ticket
    p.add_argument("--front", type=float)
    p.add_argument("--bump", type=float, default=0.0)
    p.add_argument("--taxa-bump", "--bump-rate", dest="taxa_bump", type=float, default=0.0)
    p.add_argument("--upsell", type=float, default=0.0)
    p.add_argument("--taxa-upsell", "--upsell-rate", dest="taxa_upsell", type=float, default=0.0)
    p.add_argument("--item", action="append", default=[], metavar="PRECO:TAXA")
    p.add_argument("--liquido-sobre-bruto", "--net-to-gross", dest="liquido_sobre_bruto", type=float)
    p.add_argument("--reembolso", "--refund", dest="reembolso", type=float, default=0.0)
    p.add_argument("--outros-custos", "--other-costs", dest="outros_custos", type=float, default=0.0)
    # lead-crm
    p.add_argument("--lead-venda", "--lead-to-sale", dest="lead_venda", type=float)
    p.add_argument("--lead-mql", "--lead-to-mql", dest="lead_mql", type=float)
    p.add_argument("--lead-orcamento", "--lead-to-quote", dest="lead_orcamento", type=float)
    # hotel
    p.add_argument("--adr", type=float, help="diaria media / average daily rate")
    p.add_argument("--noites", "--nights", dest="noites", type=float, help="noites por reserva / avg length of stay")
    p.add_argument("--cancelamento", "--cancellation", dest="cancelamento", type=float, default=0.0)
    p.add_argument("--comissao-ota", "--ota-commission", dest="comissao_ota", type=float)
    p.add_argument("--cos-alvo", "--target-cos", dest="cos_alvo", type=float)
    a = p.parse_args()

    global LANG, MOEDA
    LANG = a.lang
    MOEDA = a.moeda or ("R$" if LANG == "pt" else "$")
    tipo = TIPOS[a.tipo]
    linhas = [t("titulo", tipo=a.tipo), ""]

    if tipo == "hotel":
        hotel(a, linhas)
    elif tipo == "low-ticket":
        if a.front is None or a.liquido_sobre_bruto is None or a.lucro is None:
            sys.exit(t("e_lt"))
        itens = [(a.bump, a.taxa_bump), (a.upsell, a.taxa_upsell)]
        for it in a.item:
            preco, taxa = it.split(":")
            itens.append((float(preco), float(taxa)))
        itens = [(p_, t_) for p_, t_ in itens if p_ and t_]
        ticket = a.front + sum(p_ * t_ for p_, t_ in itens)
        m = a.liquido_sobre_bruto * (1 - a.reembolso) - a.outros_custos
        partes = "".join(f" + {pct(t_)} x {din(p_)}" for p_, t_ in itens)
        linhas += [
            t("ticket_ef", f=din(a.front), partes=partes, v=din(ticket)),
            t("margem_lt", lb=pct(a.liquido_sobre_bruto), r=pct(a.reembolso), o=pct(a.outros_custos), v=pct(m)),
        ]
        checar_margem(m, a.lucro)
        bloco_roas(ticket, m, a.lucro, linhas)
        linhas.append(t("base_lt"))
    else:
        if a.ticket is None or a.margem is None or a.lucro is None:
            sys.exit(t("e_ticket"))
        checar_margem(a.margem, a.lucro)
        cpa_be, cpa_alvo = bloco_roas(a.ticket, a.margem, a.lucro, linhas, regra_matar=tipo != "lead-crm")
        if tipo == "lead-crm":
            if not a.lead_venda:
                sys.exit(t("e_lead"))
            linhas += [
                t("cpl_max", lv=pct(a.lead_venda), v=din(cpa_be * a.lead_venda)),
                t("cpl_alvo", c=din(cpa_alvo), lv=pct(a.lead_venda), v=din(cpa_alvo * a.lead_venda)),
                t("matar_lead", v=din(2 * cpa_alvo * a.lead_venda)),
            ]
            for nome, taxa in ((t("mql"), a.lead_mql), (t("orc"), a.lead_orcamento)):
                if taxa:
                    linhas.append(t("custo_etapa", n=nome, c=din(cpa_alvo), lv=pct(a.lead_venda), tx=pct(taxa),
                                    v=din(cpa_alvo * a.lead_venda / taxa)))
            linhas.append(t("ciclo"))

    print("\n".join(linhas))


if __name__ == "__main__":
    main()
