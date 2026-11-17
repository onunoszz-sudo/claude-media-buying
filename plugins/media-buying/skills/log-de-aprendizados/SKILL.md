---
name: log-de-aprendizados
description: Transforma os resultados da semana (revisões, testes, negativas, diagnósticos) em regras curtas de uma conta de anúncios, com evidência, volume de dado e confiança, grava no aprendizados.md e avisa quando uma regra nova contradiz uma antiga. Use quando o usuário disser "registra o aprendizado", "atualiza os aprendizados", "o que aprendemos essa semana", "log de aprendizados", ou ao fim de uma revisão ou relatório semanal.
---

# Log de aprendizados

Depois de um mês de log, o agente conhece a conta melhor que um gestor novo. Sem log, cada
semana recomeça do zero e o mesmo erro é pago duas vezes.

## Entrada
Os resultados da semana: saídas de `revisao-meta`, `diagnostico-anuncio`,
`termos-de-pesquisa`, `saude-google-ads`, `relatorio-semanal`, ou o que o usuário contar.
Leia o `aprendizados.md` atual da conta (`**/contas/<slug>/`).

## Como escrever uma regra
Uma frase que orienta uma decisão futura, específica da conta:
- "Anúncios de prova social rodam a ROAS 2,4 e os de desconto a 0,6 nesta conta."
- "Buscas com 'barato' nunca converteram em 90 dias."
- "Hooks que mostram o resultado no primeiro segundo têm hook rate 40% acima da média."

Para cada regra registre:
| Campo | O que vai |
|---|---|
| Data | AAAA-MM-DD |
| Regra | a frase |
| Plataforma | Meta, Google, funil, atendimento |
| Evidência | os números que sustentam, com o período |
| Volume de dado | verba e conversões por trás |
| Confiança | **baixa** (uma semana, poucas conversões), **média** (2 a 4 semanas ou um teste limpo), **alta** (repetiu em mais de um teste ou mais de um mês) |
| Status | ativa, em teste, SUBSTITUÍDA em AAAA-MM-DD por <regra nova> |

Não vire regra: um dia isolado, um único anúncio com poucas conversões, uma opinião sem
número. Isso pode entrar como hipótese "em teste".

## Contradições
Antes de gravar, compare cada regra nova com as ativas. Se contradiz uma:
1. mostre as duas lado a lado, com evidência e volume;
2. **pergunte ao usuário** qual fica;
3. a perdedora não é apagada: muda o status para SUBSTITUÍDA com a data.

## Saída
1. As regras propostas em tabela, prontas para gravar.
2. As contradições encontradas, com a pergunta.
3. Depois do "ok" do usuário: grave no `aprendizados.md` e diga quantas regras ativas a
   conta tem por plataforma.

## Guardrails
- Só grava depois de mostrar e o usuário confirmar.
- Nunca inventar evidência; regra sem número fica como "em teste".
- Confiança alta exige repetição. Na dúvida, média.
