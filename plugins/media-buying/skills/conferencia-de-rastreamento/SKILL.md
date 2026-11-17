---
name: conferencia-de-rastreamento
description: Confere se o pixel da Meta conta as vendas certas - compara, dia a dia, os eventos de compra recebidos (navegador e servidor), as compras atribuídas no Gerenciador e as vendas reais da fonte de verdade (Hotmart, loja, cardápio, CRM), acha compra contada em dobro, compra sem valor e venda sumindo, e diz se dá para julgar anúncio. Só lê. Use quando o usuário disser "confere o rastreamento", "o pixel está contando certo?", "compras a mais no pixel", "pixel x Hotmart", "tracking check", ou quando a revisão do Meta avisar divergência acima de 20%.
---

# Conferência de rastreamento

Todo veredito do pack (MATAR, ESCALAR, CPA, ROAS) sai do pixel. Se ele conta venda que não existe,
anúncio ruim parece bom e recebe verba; se perde venda, anúncio bom é pausado. E a Meta aprende quem
compra com os eventos que recebe, então a contagem errada também ensina o público errado. Esta skill
mede a contagem antes de qualquer julgamento. Ela **só lê**: corrigir é com o dono da conta.

**Quando rodar:** na primeira vez que a conta entra no pack; 1 vez por mês; no mesmo dia de qualquer
mudança de checkout, funil de upsell, GTM, pixel ou banner de cookies; e sempre que `revisao-meta` ou
`brief-diario` avisarem pixel e fonte de verdade divergindo mais de 20%.

## Antes de começar
1. Ache a pasta da conta (`**/contas/<slug>/`) e leia `numeros.md`: qual é a fonte de verdade das
   vendas e o que cada venda manda ao pixel (preço cheio ou líquido; principal, bump e upsell).
2. Período: os últimos **14 dias completos** (sem hoje). Menos que 7 dias não serve.
3. ID da conta de anúncios e do conjunto de dados (pixel). Sem o ID do pixel, liste os conjuntos de
   dados da conta pelo conector.

## Coleta (só ferramentas de leitura)
1. **Vendas reais por dia**, da fonte de verdade: quantidade e valor, separando principal, bump e
   upsell, só vendas aprovadas ou completas. No export da Hotmart, use a data da venda e a coluna de
   faturamento líquido em dólar. **Nunca** leia, copie ou mostre nome, e-mail, telefone ou documento
   de cliente: só contagens e valores.
2. **Compras atribuídas por dia** no Gerenciador, nível conta, `time_increment` "1": compras do pixel
   e valor das compras. Leia também a `attribution_setting` dos conjuntos ativos.
3. **Eventos recebidos pelo pixel** (estatísticas do conjunto de dados, no máximo 28 dias, horários
   em Unix): evento Purchase por dia com origem só navegador e só servidor; e Purchase agrupado por
   URL (de que página vem cada evento).
4. **Saúde do pixel:** qualidade por evento (nota de correspondência e chaves enviadas) e detalhes do
   conjunto de dados (ativo, último disparo do navegador e do servidor, correspondência automática).
5. **Fuso horário:** as estatísticas do pixel vêm no horário do Pacífico; o Gerenciador, no fuso da
   conta; a fonte de verdade, no dela. Diferença que some no total da semana é fuso, não erro.

## Cálculo
Monte um CSV com uma linha por dia (`data, reais, atribuidas, valor_atribuido, valor_real,
recebidos_navegador, recebidos_servidor`) e rode:
`python scripts/calc_rastreamento.py dias.csv --menor-valor <menor valor que uma venda manda ao pixel> --moeda US$`
Mostre a saída. O script dá o casamento (atribuídas ÷ reais), as compras a mais sem valor, os
eventos recebidos por venda e o veredito.

## O que conferir
| Ponto | Como ler | Problema quando |
|---|---|---|
| Casamento | atribuídas ÷ vendas reais, no total do período | acima de 105%: conta o que não existe ou conta duas vezes; abaixo de 80%: perde venda; queda de 20 pontos de uma semana para outra |
| Compras a mais sem valor | dia com mais compras atribuídas que vendas e o valor batendo com o real | qualquer uma: há algo disparando Purchase sem venda (página de funil, recarga, status de pagamento) |
| Recebidos por venda | eventos do navegador + do servidor ÷ vendas reais | perto de 2 é normal (os dois mandam e a Meta deduplica); acima de 3, o servidor manda mais de um evento por venda ou outras páginas disparam Purchase |
| De onde vem | Purchase por URL | Purchase vindo de página que não é a confirmação de compra (quiz, upsell, obrigado próprio) |
| Cobertura do servidor | eventos do servidor ÷ do navegador | abaixo de 75%: venda bloqueada no navegador fica sem registro |
| Valor e moeda | valor atribuído ÷ valor real | diferença acima de 10%, moeda errada, ou valor bruto num dia e líquido no outro |
| Janela de atribuição | `attribution_setting` dos conjuntos | conjuntos com janelas diferentes não se comparam em CPA |
| Nota de correspondência | qualidade do Purchase | sem nota ou abaixo de 6: registrar; corrigir só depois de contagem dobrada e venda sumindo |
| Eventos personalizados | lista de eventos do pixel | GTM mandando todo evento do site ao pixel: só ruído, mas confirme que nenhum se chama Purchase |
| Restrição de saúde | Visão geral do conjunto de dados no Gerenciador de Eventos | produto de saúde, gravidez ou bem-estar pode cair em categoria com limite de dados; o conector não mostra: peça o print ao usuário |
| Compra de teste | uma compra real reembolsada (ou modo teste) por meio de pagamento principal | não aparece exatamente um Purchase com o valor certo |

**Padrões já vistos em low-ticket com Hotmart:**
- Bump e upsell chegam ao pixel como Purchase separado. O certo é comparar com transações, não com
  pedidos.
- A Hotmart manda valor líquido (ex.: cerca de US$ 8,80 de um principal de US$ 9,90).
- Depois que um funil de upsell foi ligado, já apareceram compras atribuídas a mais e sem valor
  (cerca de 1 em cada 10). Suspeita: o widget do funil nas páginas de oferta. Confirmar
  com compra de teste antes de mexer.

## Saída
Sem travessão, palavras simples.
1. **Veredito numa linha:** "Seguro para julgar anúncio: sim / com ressalva / não", com o casamento.
2. **Tabela por dia** (saída do script) e os totais.
3. **Achados** da tabela "O que conferir", do mais caro para o mais barato. Para cada um: o número
   que mostra o problema e o efeito no CPA (ex.: 116% de casamento faz o CPA do pixel parecer 14%
   menor que o real).
4. **Primeira correção**, em passo a passo, e quem faz (dono da conta, Hotmart, desenvolvedor).
   Depois dela, rodar esta skill de novo.
5. **O que não foi conferido** e por quê (dado que o conector não traz, print que falta).

Grave em `rastreamento-AAAA-MM-DD.md` na pasta da conta e atualize em `numeros.md` a linha de
base: casamento, compras sem valor e data. Enquanto o veredito for "não", as outras skills usam a
fonte de verdade, não o pixel, e escrevem isso no topo.

## Guardrails
- Só leitura. Nenhuma ferramenta de escrita, nem no pixel nem na conta.
- Nenhum dado pessoal de cliente: só contagens e valores.
- Nunca inventar número: o que o conector ou a fonte de verdade não trouxe é FALTANDO.
- Uma correção por vez: mexer em duas coisas no rastreamento impede saber qual resolveu.
