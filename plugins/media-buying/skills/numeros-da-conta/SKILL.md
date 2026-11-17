---
name: numeros-da-conta
description: Monta (ou revisa) os arquivos de contexto de uma conta de anúncios e calcula os números que decidem tudo depois - ROAS de breakeven, ROAS e CPA alvo, MER alvo, CPL e custo por MQL alvo. Use quando o usuário disser "números da conta", "breakeven", "qual meu ROAS alvo", "configurar conta nova", "onboarding de cliente de tráfego", ou quando outra skill de media buying não encontrar o numeros.md da conta.
---

# Números da conta

Nenhuma outra skill deste pacote julga um anúncio sem estes números. Um ROAS de 2x é ótimo
para uma conta e prejuízo para outra: depende da margem. Esta skill entrevista o usuário,
faz a conta aberta e grava os arquivos de contexto da conta.

## Onde fica o contexto da conta
Cada conta tem uma pasta `contas/<slug-da-conta>/` dentro do projeto do usuário (por
exemplo `docs/trafego/contas/minha-loja/`). Procure com Glob por
`**/contas/*/numeros.md`. Se não houver nenhuma, pergunte onde criar. Os modelos dos 6
arquivos estão em `modelos/` na pasta desta skill:

| Arquivo | Conteúdo |
|---|---|
| `numeros.md` | tipo de funil, fonte de verdade das vendas, números de decisão, limiares |
| `marca.md` | o que vende, para quem, tom, promessas permitidas e proibidas |
| `ofertas.md` | ofertas/produtos, preço, margem, o que empurrar |
| `vencedores.md` | melhores anúncios com números e hipótese |
| `regras.md` | aprovação, passos de verba, o que o agente pode fazer em cada plataforma |
| `aprendizados.md` | começa vazio; a skill `log-de-aprendizados` preenche |

## Passo 1: descobrir o tipo de funil
Pergunte (ou deduza do que já está documentado no projeto):

- **venda-direta:** o anúncio leva à compra na mesma sessão (e-commerce, delivery). Julga
  em ROAS/MER sobre a receita real.
- **low-ticket:** infoproduto barato com bump/upsell (ex.: anúncio → quiz → VSL → checkout
  na Hotmart). Julga em CPA da venda front e ROAS com o ticket efetivo.
- **lead-crm:** o anúncio gera lead e a venda acontece depois, com humano (CRM, WhatsApp,
  orçamento). Julga em CPL e custo por MQL/orçamento no curto prazo e receita ÷ mídia em
  janela longa.
- **hotel:** reserva no motor de reservas do próprio hotel. Julga em **custo de venda** (verba ÷
  receita realizada) contra a comissão da OTA (Booking, Expedia), com cancelamento e com a
  diferença entre data da reserva e data da estadia.

## Passo 2: entrevista, uma pergunta por vez
Espere a resposta antes da próxima. Para cada número, anote **de onde veio** (extrato,
planilha, palavra do cliente, estimativa). Número estimado fica marcado como estimativa.

Comum a todos:
1. Qual é a fonte de verdade das vendas? (Hotmart, Cardápio Web, planilha, CRM.) O pixel da
   plataforma nunca é fonte de verdade.
2. Margem de contribuição: receita menos custo do produto, impostos, taxas de pagamento,
   frete/embalagem, comissões. Se o usuário der uma margem **líquida** (depois de custos
   fixos), avise que é outra coisa e peça a de contribuição.
3. Lucro desejado depois dos anúncios, em % da receita.
4. Verba mensal e divisão entre plataformas.

Só low-ticket:
- Preço do front, do bump e do upsell, e a taxa de aceite de cada um (dos últimos 30 dias).
- **Líquido sobre bruto**: peça um extrato real de vendas da plataforma e calcule valor
  líquido ÷ valor bruto. Não use taxa de plataforma de memória.
- Taxa de reembolso/cancelamento.

Só lead-crm:
- Ticket médio da venda fechada.
- Taxas do funil nos últimos 90 dias: lead → MQL, lead → orçamento, lead → venda. Se o
  CRM não for confiável, use a planilha de vendas real e diga isso no arquivo.

Só hotel:
- Diária média (ADR) e noites por reserva dos últimos 90 dias, do motor de reservas ou do PMS.
- Taxa de cancelamento das reservas diretas.
- **Comissão da OTA pelo contrato do hotel** (faixa comum de 15% a 25%, mas use o número do
  contrato). É o teto de custo de venda: acima dela, a reserva direta sai mais cara que a OTA.
- Custo de venda alvo combinado com o hotel (abaixo da comissão).
- Opcional: margem de contribuição por quarto e lucro desejado, para a lente de margem.
- Separar **marca × não-marca**: busca pelo nome do hotel muitas vezes é reserva que viria direto
  de qualquer jeito. A lente OTA vale para a não-marca e para a parte da marca disputada com OTA.

## Passo 3: calcular sem errar conta
Rode o script desta skill e cole a saída no `numeros.md`. Ele mostra cada conta aberta:

```bash
python scripts/calc_numeros.py venda-direta --ticket 150 --margem 0.40 --lucro 0.10
python scripts/calc_numeros.py low-ticket --front 19.90 --bump 9.90 --taxa-bump 0.30 --upsell 37 --taxa-upsell 0.05 --liquido-sobre-bruto 0.88 --reembolso 0.05 --lucro 0.15
python scripts/calc_numeros.py low-ticket --moeda US$ --front 14.90 --item 7.90:0.10 --item 19.90:0.03 --item 29.90:0.02 --liquido-sobre-bruto 0.85 --reembolso 0.05 --lucro 0.20
python scripts/calc_numeros.py lead-crm --ticket 9000 --margem 0.45 --lucro 0.15 --lead-venda 0.0125 --lead-mql 0.25 --lead-orcamento 0.075
python scripts/calc_numeros.py hotel --adr 220 --noites 2.6 --cancelamento 0.18 --comissao-ota 0.18 --cos-alvo 0.12 --margem 0.70 --lucro 0.25
```
`--lang en` gera a saída em inglês (para o cliente americano), e os parâmetros aceitam o nome em
inglês também (`--margin`, `--nights`, `--ota-commission`, `--target-cos`...).

No hotel, o script mostra dois ROAS: sobre a receita **realizada** (depois do cancelamento) e o
equivalente **na plataforma**, que conta a receita reservada antes do cancelamento. Compare o ROAS
do Google e da Meta com o segundo.

As fórmulas, para conferir:
- ROAS de breakeven = 1 ÷ margem
- ROAS alvo = MER alvo = 1 ÷ (margem − lucro desejado)
- CPA máximo = ticket × margem; CPA alvo = ticket × (margem − lucro desejado)
- low-ticket: ticket efetivo = front + soma de (preço × taxa de aceite) de cada item da
  esteira (bump, upsells, downsells; `--item preco:taxa` repetível);
  margem = líquido sobre bruto × (1 − reembolso) − outros custos
- lead-crm: CPL alvo = CPA alvo × taxa lead → venda; custo alvo por MQL = CPA alvo ×
  (lead → venda ÷ lead → MQL)

Se o lucro desejado for maior ou igual à margem, não existe ROAS que entregue: diga isso e
peça um lucro menor.

Oferta nova sem taxas de aceite de bump/upsell ainda: calcule **dois cenários** (só o
front vende; esteira com taxas hipotéticas declaradas) e escreva no `numeros.md` qual deles
os rótulos usam provisoriamente e o que fecha a dúvida (extrato das primeiras vendas).

Taxa de bump ou upsell igual a zero em 3 ou mais vendas: antes de tratar como dado de
comportamento, abra o checkout (só leitura) e confira se os bumps aparecem e se o funil de
upsell está configurado. Esteira desligada é o achado mais barato da conta: ligar sobe o
CPA máximo sem mexer em anúncio.

## Passo 4: leitura honesta
Depois dos números, compare com o histórico real da conta (últimos 30 a 90 dias), se o
usuário tiver:
- Conta abaixo do breakeven: **não recomendar subir verba**. O problema está em oferta,
  ticket, página ou pós-clique antes de estar no anúncio. Diga onde olhar primeiro.
- Conta entre breakeven e alvo: dá para manter e otimizar, ainda sem escalar.
- Conta acima do alvo: pronta para passos de verba de até 20%.
- Conta pequena (poucas conversões por semana): avise que quase tudo vai ficar em
  OBSERVAR e que a janela de julgamento precisa ser maior (14 a 30 dias).

## Passo 5: gravar
Crie ou atualize os 6 arquivos a partir dos modelos, preenchendo só o que o usuário
confirmou. O resto fica como `FALTANDO: <o que falta e onde conseguir>`. Termine com a
lista do que ainda falta para a conta ficar completa.

Crie também o `diario.md` (modelo em `modelos/diario.md`), vazio: daqui em diante toda mudança no
funil ou na campanha vira uma linha nele no mesmo dia, e as outras skills leem esse diário.

## Regras
- Nunca inventar número. Dado ausente vira FALTANDO; dado estranho é apontado antes de usar.
- Mostrar a conta aberta de todo número de decisão.
- Moeda: se as vendas são em dólar e a verba em real (ou o contrário), declarar a cotação
  usada e a data.
