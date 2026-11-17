---
name: termos-de-pesquisa
description: Lê o relatório de termos de pesquisa do Google Ads e transforma desperdício em lista de palavras-chave negativas agrupadas por tema, com gasto e tipo de correspondência, pronta para colar; também lista termos que converteram e ainda não são palavra-chave. Use quando o usuário disser "termos de pesquisa", "negativar", "palavras negativas", "search terms", "onde o Google está desperdiçando", ou mandar o CSV de termos de pesquisa.
---

# Termos de pesquisa → negativas

Em quase toda conta uma fatia da verba vai para buscas que nunca compram: emprego, grátis,
curso, produto errado, suporte de concorrente, pesquisa informativa. Cortar isso é o
dinheiro mais fácil de economizar no Google. Rodar toda semana, nos últimos 14 a 30 dias.

## Antes de começar
1. Leia `numeros.md`, `ofertas.md`, `marca.md`, `regras.md` e `aprendizados.md` da conta.
2. Peça:
   - o relatório de **termos de pesquisa** (CSV) do período, com campanha, grupo, termo,
     tipo de correspondência, cliques, custo, conversões;
   - a lista atual de **palavras-chave** e de **negativas** (da campanha e das listas
     compartilhadas). Sem essas listas, avise que não dá para checar conflito e marque cada
     sugestão como "conferir conflito".

### Com o MCP do Google Ads conectado (ferramenta `search`, só leitura)
> Ferramenta `search` do servidor oficial: passe as partes separadas, não a consulta inteira. `resource` = o que vem depois do FROM, `fields` = a lista do SELECT, `conditions` = cada trecho do WHERE (ex.: `"segments.date DURING LAST_30_DAYS"`), `orderings` e `limit`. Na dúvida sobre um campo, use `metadata_get_resource_metadata`.

Passe o `customer_id` da conta (só números) e, se o acesso for pela MCC, o `login_customer_id`.
Custo vem em micros: divida por 1.000.000.
```sql
-- termos de pesquisa, por gasto
SELECT search_term_view.search_term, search_term_view.status, campaign.name, ad_group.name,
       metrics.cost_micros, metrics.clicks, metrics.conversions, metrics.conversions_value
FROM search_term_view
WHERE segments.date DURING LAST_30_DAYS
ORDER BY metrics.cost_micros DESC
LIMIT 500

-- palavras-chave ativas
SELECT campaign.name, ad_group.name, ad_group_criterion.keyword.text, ad_group_criterion.keyword.match_type
FROM keyword_view
WHERE ad_group_criterion.status = 'ENABLED'

-- negativas da campanha
SELECT campaign.name, campaign_criterion.keyword.text, campaign_criterion.keyword.match_type
FROM campaign_criterion
WHERE campaign_criterion.negative = TRUE AND campaign_criterion.type = 'KEYWORD'

-- negativas de listas compartilhadas (a tabela da campanha não mostra estas)
SELECT shared_set.name, shared_criterion.keyword.text, shared_criterion.keyword.match_type
FROM shared_criterion
WHERE shared_set.type = 'NEGATIVE_KEYWORDS'
```
O servidor oficial só lê: as negativas aprovadas entram pela interface (ou pelo navegador, se o
usuário pedir), nunca pelo MCP.

## Como analisar
- **Olhe gasto, não cliques.** Um termo com R$ 80 e zero conversão importa mais que um com
  3 cliques.
- Agrupe em temas: emprego/vagas, grátis/barato, curso/como fazer, produto ou serviço
  errado, outra cidade/região, concorrente (suporte, login, telefone), informativo,
  outro idioma.
- Para cada tema: gasto total, os termos, e a negativa sugerida com correspondência:
  - **exata** `[termo]` bloqueia só aquela busca. Use quando estiver em dúvida.
  - **frase** `"termo"` bloqueia toda busca que contém a frase. Mais forte, mais risco.

## Checagem de conflito (obrigatória)
Antes de sugerir uma negativa de **frase**, confira se ela bloquearia:
1. a marca da conta ou um produto de `ofertas.md`;
2. alguma palavra-chave ativa;
3. algum termo que **converteu** no período.

Exemplo do erro que esta checagem evita: a negativa de frase "aluguel" bloqueava "aluguel
de painel de led", justamente o serviço vendido. Se houver conflito, rebaixe para exata ou
descarte, e explique.

## Saída
1. **Resumo em 3 linhas:** gasto total no período, gasto em termos sem conversão, quanto as
   negativas sugeridas cortariam (estimativa sobre o período analisado).
2. **Tabela por tema:** tema, gasto, termos, negativa sugerida, correspondência, conflito
   checado (sim/não).
3. **Lista pronta para colar** na tela de negativas do Google Ads, uma por linha, já com
   a sintaxe (`[exata]` ou `"frase"`), e em qual nível aplicar (lista compartilhada,
   campanha ou grupo).
4. **Termos que converteram e não são palavra-chave**, com sugestão de grupo.
5. **Aprendizado candidato** para o `log-de-aprendizados` (ex.: "buscas com 'barato' nunca
   converteram em 90 dias").

## Guardrails
- Nunca sugerir negativa que bloqueie a marca, um produto ativo ou um termo que converteu.
- Não aplicar nada sem "sim". Se o usuário aprovar e o agente tiver acesso ao Google Ads no
  navegador, aplicar só o que foi aprovado e conferir depois na tabela de negativas.
- Termo com pouca amostra e intenção plausível fica de fora: anote para a próxima rodada.
