---
name: revisao-meta
description: Revisa os anúncios ativos do Meta Ads e dá a cada um o rótulo MATAR, OBSERVAR ou ESCALAR, aponta em que estágio cada anúncio vaza (hook, retenção, clique, conversão) e roda o radar de fadiga. Use quando o usuário disser "revisão do Meta", "o que pausar", "quais anúncios escalar", "analisa meus criativos", "radar de fadiga", "anúncios cansados", ou mandar um export do Gerenciador de Anúncios.
---

# Revisão do Meta Ads

Dizer "ROAS bom, mantém; ROAS ruim, pausa" mostra o que aconteceu, não por quê. Esta revisão
lê cada anúncio estágio por estágio, contra a média da própria conta, e devolve uma lista
numerada de ações para o usuário aprovar.

## Antes de começar
1. Ache a pasta da conta (`**/contas/<slug>/`). Leia `numeros.md`, `regras.md` e
   `aprendizados.md`. Sem `numeros.md`, pare e rode `numeros-da-conta` primeiro.
2. Pegue os dados, nesta ordem de preferência:
   - **Conector oficial do Meta Ads** (se as ferramentas dele estiverem nesta sessão):
     use as ferramentas de relatório no nível anúncio, para 7 e 14 dias, com os mesmos campos
     do export abaixo, e peça os recortes por posicionamento, idade e dia. **O conector também
     escreve** (cria campanha pausada, muda orçamento, pausa, ativa): nunca chame uma
     ferramenta de escrita sem um "sim" do usuário para aquela ação específica, e depois de
     executar, leia de novo para confirmar que ficou como aprovado.
   - **Export do Gerenciador:** nível Anúncio, últimos 7 dias **e** últimos 14 dias (dois
     arquivos, ou um com detalhamento por dia). Colunas necessárias: nome do anúncio,
     conjunto, campanha, status de veiculação, data de início, valor usado, impressões,
     frequência, CPM, cliques no link, CTR (link), reproduções de vídeo de 3 s, ThruPlays,
     resultados/compras, valor de conversão. Diga ao usuário quais colunas faltaram.
3. **Vendas reais:** se a fonte de verdade (`numeros.md`) não for o pixel, peça o número
   real do período. Quando pixel e fonte de verdade divergirem mais de 20%, avise antes
   de rotular: a decisão pode estar sendo tomada em cima de rastreamento quebrado, e sugira
   rodar `conferencia-de-rastreamento`. Em
   low-ticket o valor de compra do pixel costuma registrar só o front: ROAS do pixel
   subestima a esteira (bump/upsell), então julgue pelo CPA contra os dois cenários de
   `numeros.md` até ter a plataforma de pagamento.
   **Venda real por anúncio:** se a plataforma de pagamento guarda a origem da venda (Hotmart:
   campo `sck`/"Origem de checkout"; loja: `utm_content`; CRM: campo de origem), e os links dos
   anúncios passam o nome do anúncio nesse parâmetro, conte as vendas aprovadas por anúncio e
   use o **CPA real** (gasto do anúncio ÷ vendas reais dele) no lugar do CPA do pixel. Diga
   quantas vendas do período ficaram sem origem. Sem esse parâmetro nos links, recomende
   incluir (é o que permite matar anúncio pela venda de verdade).
4. **Colunas personalizadas** (ex.: "HOOK RATE", "HOLD RATE" criadas na conta): use como
   vieram, mas pergunte a fórmula se ela mudar a leitura. Mostre a outra interpretação
   quando for relevante (ThruPlay ÷ impressões é diferente de ThruPlay ÷ 3 s).
5. **Recortes** (export por posicionamento, idade, dia): confira se os totais batem entre
   eles antes de usar. Dia parcial (o dia do export) não entra na leitura de tendência.
6. **Plano × realidade:** se houver plano da campanha documentado, compare verba diária,
   idade, países e posicionamentos planejados com o que o export mostra entregando.

## Métricas por anúncio
| Estágio | Conta | Se estiver baixo, o problema é |
|---|---|---|
| Hook | reproduções de 3 s ÷ impressões | os 3 primeiros segundos não param o scroll |
| Retenção | ThruPlays ÷ reproduções de 3 s | para, mas não fica: história lenta, produto aparece tarde |
| Clique | cliques no link ÷ impressões (CTR link) | assiste mas não quer o bastante: oferta, prova, CTA |
| Conversão | conversões ÷ cliques no link | clica mas não compra: página, preço, checkout, velocidade |

- Compare cada anúncio com a **média da conta no mesmo formato** (vídeo com vídeo, estático
  com estático). Benchmark de fora não vale.
- Estático não tem hook/retenção: leia CTR e conversão.
- Em low-ticket e lead-crm, o estágio "conversão" se abre em pós-clique (quiz, VSL,
  checkout, lead → MQL). Se esses dados existirem, use `diagnostico-anuncio` para o anúncio
  que vazar ali.

## Rótulos
Use os limiares de `regras.md`; se não houver, estes padrões:

- **MATAR:** gastou 2x o CPA alvo sem nenhuma conversão, **ou** CPA 50%+ acima do alvo por
  3 dias seguidos com volume suficiente.
- **OBSERVAR:** menos de 72 h no ar; conjunto em aprendizado; menos conversões que o mínimo
  de `regras.md` (padrão 3); ou CPA entre o máximo (breakeven) e o alvo.
- **ESCALAR:** CPA abaixo do alvo (ou ROAS acima do alvo) por 3+ dias, com o mínimo de
  conversões, e CPA e frequência estáveis.

Amostra pequena nunca vira vencedor nem perdedor: fica em OBSERVAR, com a quantia de
verba que falta para decidir.

**Custo extra** (ordena a lista de ações): gasto − conversões × CPA alvo. É quanto o anúncio
custou acima do que deveria para o que entregou. Positivo e alto = maior dinheiro perdido,
mesmo que o ROAS da campanha pareça bom. Os 3 piores por custo extra abrem as ações.

Dois rótulos complementares:
- **SEM VERBA:** o anúncio gastou menos que 1x o CPA alvo no período. Não foi testado,
  então não é perdedor. Se vários anúncios estão nessa situação dentro do mesmo conjunto
  com orçamento da campanha (CBO/Advantage+), a Meta concentrou a entrega em um só: o
  remédio é conjunto próprio com verba igual (ABO) para os criativos que precisam de teste,
  não pausar os sem verba.
- **BLOQUEADO PARA ESCALAR (conformidade):** o anúncio usa promessa, credencial,
  depoimento, número ou preço âncora proibido em `marca.md`. Nunca recebe passo de verba,
  mesmo com números de ESCALAR; a ação é trocar pela versão conforme. Se não houver como
  saber o conteúdo do anúncio (sem arquivo, sem transcrição), diga que a conformidade não
  foi checada. Se o `marca.md` registra que o dono da conta aceitou uma promessa específica,
  ela não bloqueia.

## Radar de fadiga
Para todo anúncio com gasto relevante nos últimos 14 dias (padrão: mais que 2x o CPA alvo),
compare os primeiros 7 dias no ar com os últimos 7: frequência, CTR, CPM, CPA, hook rate.
Marque **CANSANDO** quando 2 ou mais pioram juntos. Ordene os cansados por verba: os do
topo precisam de variação nova primeiro (sugira rodar `multiplicador-de-vencedor`).

**Piora geral não é fadiga:** se quase todos os anúncios pioraram na mesma semana (inclusive os
novos), a causa é comum a todos: rastreamento, página, checkout, oferta, preço ou leilão
(sazonalidade). Não marque CANSANDO; diga isso e sugira `conferencia-de-rastreamento` ou
`diagnostico-anuncio` antes de trocar criativo.

## Saída
Sem travessão, palavras simples.

1. **Três linhas:** o que está funcionando, o que está vazando, o que fazer hoje.
2. **Tabela** (um anúncio por linha): anúncio, verba, conversões (reais, se houver), CPA,
   custo extra, ROAS, hook, retenção, CTR, frequência, estágio que vaza, rótulo. Anúncios em
   ordem de custo extra (maior primeiro).
3. **Recortes que mudam decisão:** idade, posicionamento ou dia em que a verba está indo
   sem converter (ex.: uma faixa etária com mais verba que a que compra e zero venda);
   posicionamentos de clique de baixa qualidade (Audience Network com CTR muito acima da
   média, anúncios dentro do Reels). Sempre com o aviso de tamanho de amostra.
4. **Fadiga:** lista dos CANSANDO com as métricas que pioraram (ou "não se aplica" se
   nenhum anúncio tem 14 dias).
5. **Ações numeradas para aprovar:**
   - pausas (nunca apagar);
   - **escada de verba**, no máximo um degrau por conjunto ou campanha, 48 h desde o último:
     - **subir** até 20%: ESCALAR com CPA estável;
     - **segurar:** entrou anúncio novo no conjunto nas últimas 48 h, o conjunto está em
       aprendizado ou houve mudança de página/oferta (a leitura ainda não é limpa);
     - **descer um degrau** (−20%) em vez de matar: CPA entre o alvo e o máximo (breakeven)
       num conjunto que já foi vencedor;
   - quais anúncios precisam de hook novo, história nova, oferta/prova nova ou correção
     de página (pelo estágio que vaza).
6. **Aprendizado candidato** (se houver padrão claro): uma linha para o
   `log-de-aprendizados`.

Ao salvar a revisão em arquivo, use o nome `revisao-meta-AAAA-MM-DD.md` na pasta da oferta
ou do cliente.

Anúncio **reprovado pela Meta**: registre no mesmo dia uma linha no `marca.md` da conta (o que
foi reprovado e a frase/imagem provável), para a regra valer na próxima rodada de criativos.

## Guardrails
- Não mudar nada na conta sem um "sim" do usuário para cada ação numerada.
- Pausar, nunca apagar.
- Nunca mais de 20% por passo de verba; nunca dois passos no mesmo conjunto em 48 h.
- Dia ruim isolado não é tendência: julgar na janela de `numeros.md`.
- Nunca inventar número; métrica ausente aparece como FALTANDO.
