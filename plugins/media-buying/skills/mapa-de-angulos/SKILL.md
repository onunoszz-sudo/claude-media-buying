---
name: mapa-de-angulos
description: Monta o mapa de ângulos de uma conta - a grade ângulo x pessoa x formato a partir das palavras reais dos clientes (comentários, respostas de quiz, mensagens, avaliações), marca o que já foi testado e com que resultado, aponta as casas vazias com mais evidência e escreve ganchos para elas, cada um passado por uma checagem de política (atributo pessoal, alegação de saúde, promessa) antes de ir para produção. Use quando o usuário disser "mapa de ângulos", "ângulos novos", "pesquisa de gatilho", "o que testar de criativo", "ideias de anúncio", "ganchos novos para a conta", "checa a política desses ganchos".
---

# Mapa de ângulos

Criativo novo que nasce da cabeça de quem faz o anúncio costuma repetir o que já roda. Esta skill
parte do que os clientes dizem com as próprias palavras, organiza isso numa grade e mostra onde
ainda não há anúncio. O resultado alimenta a `rodada-de-teste`.

## Antes de começar
1. Ache a pasta da conta (`**/contas/<slug>/`). Leia `marca.md` (o que não pode ser dito),
   `vencedores.md`, `aprendizados.md` e `testes.md`.
2. Junte as **palavras reais** (quanto mais fontes, melhor), e anote de onde veio cada frase:
   - comentários dos anúncios e do perfil;
   - respostas abertas do quiz ou do formulário;
   - mensagens de suporte, WhatsApp, e-mail;
   - avaliações e depoimentos já autorizados;
   - termos de pesquisa do Google (o que a pessoa digita).
3. Liste os anúncios que já rodaram com o ângulo, a pessoa e o formato de cada um, e o resultado
   (venda real quando houver, senão a métrica do estágio).

Sem nenhuma palavra real, diga isso e pare: um mapa feito só de suposição não vale a rodada.

## 1. As três colunas
- **Ângulo:** o motivo que faz a pessoa agir. Tipos: dor (o que dói hoje), medo (o que pode
  acontecer), desejo (o que quer sentir ou ter), objeção (por que não compraria) e identidade
  (quem ela é ou quer ser).
- **Pessoa:** quem fala ou quem é o alvo, pela situação e não pela demografia (ex.: "primeira
  vez, terceiro trimestre" em vez de "mulher 25-34").
- **Formato:** UGC/depoimento, especialista falando, demonstração, animação/novela, estático com
  prova, carrossel.

Dois anúncios são do mesmo ângulo quando a razão de compra é a mesma, mesmo com palavras diferentes.
Trocar só o rosto ou a cor não cria ângulo novo.

## 2. A grade
1. Agrupe as frases reais por ângulo e conte quantas há em cada um (é a força da evidência).
2. Cruze ângulo x pessoa. Em cada casa: os anúncios que já rodaram nela, o formato e o resultado
   (VENCEDOR, PERDEDOR, SEM VERBA, NÃO TESTADO).
3. Marque as **casas vazias com mais evidência**: muitos clientes falam disso e nenhum anúncio
   fala. São as primeiras candidatas.
4. Casa já testada e perdedora só volta com formato diferente e um motivo escrito.

## 3. Ganchos para as 3 melhores casas
Para cada casa escolhida:
- 3 frases reais que sustentam o ângulo (anonimizadas, sem nome nem dado pessoal);
- 5 ganchos de até 3 segundos falados ou 8 palavras escritas, cada um com o formato sugerido;
- a hipótese em uma linha: "se mostrar X para quem sente Y, a pessoa clica porque Z".

## 4. Checagem de política (todo gancho, antes de produção)
Marque cada gancho como OK, REESCREVER ou VETADO:
| Risco | Exemplo do problema | Como reescrever |
|---|---|---|
| Atributo pessoal | afirmar ou perguntar algo sobre a condição de quem vê ("você está acima do peso?", "sua ansiedade...") | falar da situação ou de um personagem em terceira pessoa |
| Alegação de saúde ou resultado garantido | "cura", "sem dor", "perca X kg em Y dias" | descrever o que o produto ensina ou faz, sem prometer desfecho |
| Antes e depois / corpo | comparação de corpo, close de parte do corpo | mostrar a rotina ou a pessoa inteira |
| Proibido pela conta | qualquer item do `marca.md` | seguir o `marca.md` |
| Histórico de reprovação | frase ou imagem parecida com anúncio já reprovado | usar a linha de reprovação registrada no `marca.md` |

Gancho VETADO não aparece na lista final. Mostre a versão reescrita ao lado dos REESCREVER.

## Saída
Sem travessão, palavras simples.
1. **Uma linha:** quantas frases reais, de quantas fontes, quantas casas vazias com evidência.
2. **A grade** (ângulo x pessoa) com o status de cada casa.
3. **As 3 casas para testar agora**, com evidência, hipótese e os 5 ganchos já checados.
4. **Fila:** as próximas casas, em ordem de evidência.

Grave o mapa em `angulos.md` na pasta da conta (atualize a cada rodada) e passe as 3 casas para a
`rodada-de-teste`.

## Guardrails
- Nunca inventar frase de cliente nem depoimento. Frase sem fonte não entra.
- Nunca copiar anúncio de concorrente: concorrente mostra quais ângulos existem, não o texto.
- Dado pessoal de cliente não vai para o mapa.
- A checagem de política reduz o risco de reprovação, mas não garante aprovação: a decisão final
  é da Meta e do dono da conta.
