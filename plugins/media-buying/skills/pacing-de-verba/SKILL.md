---
name: pacing-de-verba
description: Controla o ritmo de gasto de uma ou várias contas de anúncios contra o orçamento do mês (ou do período contratado) - pace, projeção do fim do mês, diário recomendado e status NO RITMO, ABAIXO, ACIMA ou ESTOURA, com a correção dividida em passos de até 20%. Use quando o usuário disser "pacing", "como está o gasto do mês", "vai estourar o orçamento", "estou gastando pouco", "orçamento do cliente", "fechar o mês no orçamento", ou rodar a revisão de sexta.
---

# Pacing de verba

Em agência, gastar o orçamento contratado (nem mais, nem menos) é obrigação de todo dia.
Gastar de menos deixa resultado na mesa e o cliente pergunta por que pagou a gestão;
gastar de mais vira conversa difícil de reembolso. Esta skill olha o portfólio inteiro e
devolve a lista de correções, a maior em dinheiro primeiro.

## Dados
Uma linha por conta e plataforma, num CSV com estas colunas (cabeçalho em português ou inglês):

| Coluna | O que é |
|---|---|
| `conta` / `account` | nome da conta ou cliente |
| `plataforma` / `platform` | Google Ads, Meta... |
| `orcamento` / `budget` | orçamento do período |
| `gasto` / `spend_to_date` | gasto **até ontem** (dias completos) |
| `inicio` / `start`, `fim` / `end` | período, AAAA-MM-DD, inclusivo |
| `diario_atual` / `current_daily` | opcional: orçamento diário configurado hoje (sem ele, usa o ritmo médio) |
| `planejado_ate_hoje` / `planned_to_date` | opcional: gasto planejado até ontem, para curva sazonal (sem ele, linear) |

De onde tirar:
- **Google Ads com o MCP conectado:** por conta, `SELECT campaign.name, campaign_budget.amount_micros,
  metrics.cost_micros FROM campaign WHERE segments.date DURING THIS_MONTH AND campaign.status = 'ENABLED'`
  (custo em micros ÷ 1.000.000; o diário atual é a soma de `amount_micros` das campanhas ativas).
  Hoje não entra: some só até ontem.
- **Meta com o conector oficial:** gasto do mês até ontem no nível conta e o orçamento diário das
  campanhas/conjuntos ativos.
- **Sem conector:** export das plataformas ou a planilha de controle da agência.
- **Orçamento contratado:** do `regras.md` de cada conta (`**/contas/<slug>/`). Se não estiver lá,
  FALTANDO: pergunte, nunca suponha.

## Rodar
```bash
python scripts/calc_pacing.py portfolio.csv --hoje AAAA-MM-DD
python scripts/calc_pacing.py portfolio.csv --as-of AAAA-MM-DD --lang en --currency $
```
O script está em `scripts/` nesta pasta, com um `exemplo-portfolio.csv` de 10 contas fictícias.

## Como ler os status
- **NO RITMO:** projeção do fim do período dentro de ±10% do orçamento. Manter; o script mostra o
  diário exato para fechar no orçamento, como ajuste fino opcional.
- **ABAIXO:** projeção mais de 10% abaixo. Subir o diário em passos de até 20% a cada 48 h. Se a
  correção passar de 50%, é **decisão do cliente ou do gestor** (pode ser que a conta não tenha
  demanda ou criativo para absorver a verba; avisar em vez de forçar).
- **ACIMA:** projeção mais de 10% acima; o script mostra o dia em que o dinheiro acaba. Baixar o
  diário. Corte não precisa respeitar o passo de 20%, mas corte grande em conjunto que está
  vendendo bem merece conversa com o cliente sobre aumentar o orçamento.
- **ESTOURA:** o orçamento do período já foi gasto. Pausar ou pedir aumento ao cliente, hoje.

Antes de recomendar subir verba, cruze com `numeros.md`: subir orçamento de conta que está abaixo
do breakeven só para "gastar o contratado" é queimar dinheiro do cliente. Nesse caso, a
recomendação é falar com o cliente, não subir.

## Saída
1. A tabela do script (todas as contas, maior desvio em dinheiro primeiro).
2. As ações numeradas para aprovar.
3. Os lembretes de comportamento das plataformas (o diário configurado não é teto exato).
4. Para contas ABAIXO por falta de entrega, uma linha de causa provável (lance, público pequeno,
   criativo reprovado, limite da conta) para checar com `saude-google-ads` ou `revisao-meta`.

## Guardrails
- Nada muda na conta sem "sim" para cada ação.
- Subida em passos de até 20%, um a cada 48 h por campanha ou conjunto.
- Gasto de hoje não entra: o dia está incompleto.
- Nunca inventar orçamento contratado; sem ele, a conta fica fora do cálculo e aparece como FALTANDO.
