# Plano de lançamento: <conta>

> Um bloco por campanha. Preenchido antes de subir; a skill `qa-de-lancamento` compara a conta
> com este arquivo. Campo em branco vira "FALTANDO no plano" e não é conferido.
> Valores com "qualquer" não são conferidos de propósito.

## Campanha: <nome exato da campanha>
- **Plataforma:** Meta
- **ID da campanha:** <preencher depois de criar, ajuda a achar>
- **Objetivo:** Vendas | Leads | Tráfego
- **Orçamento:** ABO (no conjunto) | CBO (na campanha)
- **Orçamento diário:** <valor e moeda> (por conjunto se ABO; total se CBO)
- **Início:** AAAA-MM-DD · **Leitura:** AAAA-MM-DD · **Fim ou teto de gasto:** <data ou valor>

### Conjunto: <nome exato do conjunto>
- **Países:** <códigos, ex.: MX, CO>
- **Tipo de local:** moram em | moram ou estiveram recentemente | qualquer
- **Idade:** <mín> a <máx>
- **Idade como limite:** sim (opções de público originais, Advantage+ desligado) | não (Advantage+ ligado, idade é sugestão)
- **Gênero:** mulheres | homens | todos
- **Interesses ou públicos personalizados:** nenhum | <lista>
- **Posicionamentos:** automáticos | <lista exata, ex.: Reels do Facebook, Reels do Instagram>
- **Fora de propósito:** <ex.: Audience Network, anúncios dentro do Reels>
- **Evento de otimização:** <ex.: Compra>
- **Pixel ou conjunto de dados:** <ID>
- **Orçamento do conjunto:** <se ABO>

### Anúncios
| Nome exato | Arquivo do criativo | URL final | Parâmetros de URL |
|---|---|---|---|
| <nome> | <arquivo> | <https://...> | <utm_source=...&utm_content={{ad.name}}> |

### Regras de leitura combinadas
- **Pausar:** <ex.: anúncio com US$ 13,87 sem venda>
- **Escalar:** <ex.: CPA até US$ 6,94 com 5 vendas>
- **Não mexer até:** <data>
