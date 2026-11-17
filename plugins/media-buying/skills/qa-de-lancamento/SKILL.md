---
name: qa-de-lancamento
description: Confere uma campanha do Meta Ads contra o plano escrito, antes de subir e 72 h depois - países e tipo de local, idade, público Advantage+, posicionamentos, ABO ou CBO, orçamento, evento e pixel, URL e UTM, nomes - e faz a leitura técnica do começo da entrega (gasto fora do país, verba concentrada num anúncio, reprovações, página). Só lê; não julga desempenho. Use quando o usuário disser "QA da campanha", "confere antes de subir", "checa se está igual ao plano", "subi a campanha, confere", "leitura de 72 horas", "launch QA".
---

# QA de lançamento

O erro mais caro de uma campanha nova não é o criativo: é ela estar configurada diferente do
que foi planejado (país, idade, posicionamento, tipo de orçamento) e ninguém ver por dias.
Esta skill compara a conta com o plano, campo a campo, e diz o que bloqueia e o que só avisa.
Ela **só lê**: corrigir é com o usuário ou com uma ação aprovada à parte.

## Antes de começar
1. Ache a pasta da conta (`**/contas/<slug>/`) e leia `plano-de-lancamento.md`. Sem plano,
   pare: ofereça montar a partir de `modelos/plano-de-lancamento.md` com o usuário. Sem plano
   não existe QA, só opinião.
2. Leia `regras.md` (o que é proibido na conta) e `marca.md` (o que os anúncios não podem
   dizer), se existirem.
3. Diga o modo: **pré-lançamento** (campanha em rascunho ou criada e ainda pausada) ou
   **72 h** (campanha no ar há 1 a 4 dias). Na dúvida, rode os dois.
4. Dados pelo **conector oficial do Meta Ads**. Só ferramentas de leitura (entidades,
   rascunhos, histórico de atividade, quebras, criativos, erros, conjuntos de dados).
   **Nunca** chame ferramenta que cria, edita, pausa ou ativa, mesmo que o conector sugira.

## Modo pré-lançamento: plano x conta
Leia campanha, conjuntos e anúncios (rascunho com `object_state=draft`, se ainda não
publicados) com os atributos de configuração, e compare:

| Campo do plano | Onde está na conta | Gravidade se diferente |
|---|---|---|
| Objetivo | `objective` da campanha | BLOQUEIA |
| ABO ou CBO | orçamento na campanha (`daily_budget`/`lifetime_budget` da campanha) = CBO; no conjunto = ABO | BLOQUEIA |
| Orçamento diário | `daily_budget` (em centavos na API) | BLOQUEIA se maior que o plano; AVISO se menor |
| Países | `targeting.geo_locations` (`countries`, `country_groups`; "worldwide" é mundo inteiro) | BLOQUEIA |
| Tipo de local | `geo_locations.location_types`: `home` = moram; `recent` = estiveram; `travel_in` = viajando | AVISO (a Meta às vezes grava `frequently_in` junto de `home`; registrar, não bloquear) |
| Idade | `age_min`, `age_max`, `age_range` | BLOQUEIA se fora da faixa com idade como limite |
| Idade como limite | `targeting_automation.advantage_audience`: 1 = Advantage+ ligado, idade e gênero viram sugestão | BLOQUEIA se o plano pede limite e está 1 |
| Gênero | `genders` (1 homens, 2 mulheres) | BLOQUEIA |
| Posicionamentos | `publisher_platforms`, `facebook_positions`, `instagram_positions`, `audience_network_positions` (use os campos `effective_*` quando vierem; `page_types` não decide) | BLOQUEIA se entra algo da lista "fora de propósito" ou se o plano lista posicionamentos exatos e a conta tem outros; plano "automáticos" não confere a lista |
| Evento e pixel | `optimization_goal` e `promoted_object` do conjunto | BLOQUEIA |
| Nomes | nome exato de campanha, conjunto e anúncio | AVISO (quebra a leitura por `utm_content`) |
| URL final e UTM | link do criativo de cada anúncio (ferramentas de criativo, campo `link_url`; em criativo de vídeo ele pode não vir, aí tente a prévia do anúncio) | BLOQUEIA se a URL for outra; AVISO se faltar UTM; sem o dado, "não conferido" e o usuário confere no Gerenciador |
| Status | `effective_status` de anúncios e conjuntos; reprovados | BLOQUEIA se reprovado |
| Datas | início e fim do conjunto | AVISO |

Campo do plano em branco: escreva "FALTANDO no plano" e não confira. Campo com "qualquer":
não confira.

Confira também, quando houver como:
- **Página:** a URL final abre (sem 404, sem redirecionamento para outra página) e o
  PageSpeed no celular (mediana de algumas rodadas; um número só engana).
- **Texto do anúncio** contra o que `marca.md` proíbe (sem reabrir o que o dono da conta já
  aceitou e está registrado lá).
- **Aprimoramentos criativos automáticos** ligados, quando o plano pede o criativo como está.

## Modo 72 h: leitura técnica
Sem veredito de desempenho (isso é da `revisao-meta`). Leia do início da campanha até hoje e
marque:
1. **Entrega começou?** Conjunto ou anúncio com status ativo e gasto zero há mais de 24 h:
   motivo (aprendizado limitado, reprovação, orçamento baixo, público pequeno).
2. **Gasto por país fora do plano.** Peça a quebra por país **conjunto por conjunto**
   (`object_ids` do conjunto): no nível campanha a lista de países pode vir cortada. Some o
   gasto fora dos países do plano e mostre em dinheiro e em %.
3. **Verba concentrada.** Um anúncio com mais de 80% do gasto do conjunto: os outros não estão
   sendo testados. Se o plano era testar criativos em igualdade, o remédio é conjunto próprio
   (ABO), não pausar os sem verba.
4. **Idade e posicionamento entregues** contra o plano (quebras por idade e por
   posicionamento), quando o Advantage+ estiver ligado.
5. **Rastreio:** o evento de otimização registrou alguma coisa? Cliques no link viram
   visualização da página (menos de 50% indica página lenta ou link quebrado)? Se houver fonte
   de verdade das vendas, as compras batem?
6. **Mudanças desde o lançamento** (histórico de atividade): quem mudou o quê, para o usuário
   saber que a leitura de desempenho vai precisar ser separada antes e depois.

## Saída
Sem travessão, palavras simples.

1. **Uma linha de veredito:** "pode subir", "não subir: N bloqueios" ou, no modo 72 h,
   "rodando como planejado" / "rodando diferente do plano em N pontos".
2. **Tabela por campanha e conjunto:** campo, plano, conta, situação (OK, BLOQUEIA, AVISO,
   FALTANDO no plano).
3. **Modo 72 h:** gasto fora do plano (valor e %), concentração por anúncio, rastreio.
4. **Correções em passo a passo** no Gerenciador, uma por bloqueio, na ordem: o que gasta
   dinheiro errado primeiro. Lembre que editar conjunto no ar pausa a entrega até reativar.
5. **O que não foi conferido** e por quê (campo em branco, ferramenta sem o dado).

Ao salvar, use `qa-lancamento-AAAA-MM-DD.md` na pasta da oferta ou do cliente.

## Guardrails
- Nenhuma ferramenta de escrita, em nenhuma hipótese. Correção é ação separada, com "sim".
- Nunca supor o plano: o que não está escrito é FALTANDO.
- Nunca inventar número; dado que a ferramenta não trouxe aparece como FALTANDO.
- QA não é revisão de desempenho: nada de MATAR ou ESCALAR aqui.
