# 🎤 ROTEIRO DE APRESENTAÇÃO — DIAGNÓSTICO ESTRATÉGICO NUBANK

**Público:** Banca Acadêmica · **Tempo:** 10 a 15 minutos · **Tom:** Didático e Explicativo

---

## ⏱ DIVISÃO DE TEMPO

| Bloco | Conteúdo | Tempo |
|-------|----------|-------|

| 1 | Abertura e contextualização | ~1 min |
| 2 | Metodologia | ~1,5 min |
| 3 | Saúde Financeira | ~3 min |
| 4 | Voz do Cliente | ~3 min |
| 5 | Cruzamento dos dados | ~2 min |
| 6 | Plano de Ação e Conclusão | ~2 min |
| 7 | Encerramento | ~30 seg |

---

## 🟣 BLOCO 1 — ABERTURA (~1 min)

> *Slide: Capa — "Diagnóstico Estratégico 360°"*

**Fala sugerida:**

"Bom dia a todos. O trabalho que vamos apresentar hoje é um Diagnóstico Estratégico 360° do Nubank, combinando duas perspectivas que raramente aparecem juntas: a saúde financeira regulatória do banco — com dados públicos do Banco Central — e a percepção real dos seus clientes, extraída de 122 reclamações públicas.

A pergunta central que guiou a pesquisa foi: **o que os números oficiais e a voz dos clientes, juntos, nos dizem sobre os riscos do Nubank?**"

---

## 🟣 BLOCO 2 — METODOLOGIA (~1,5 min)

> *Slide: Metodologia & Escopo*

**Fala sugerida:**

"O trabalho foi estruturado em três pilares metodológicos.

O primeiro foi a análise dos **dados financeiros regulatórios**, especificamente o Relatório Pilar 3 exigido pelo Bacen, cobrindo o período de Q1 a Q3 de 2025 — ou seja, de janeiro a setembro do ano passado. Para quem não está familiarizado, Q1, Q2, Q3 e Q4 são simplesmente os quatro trimestres do ano.

O segundo pilar foi a **análise das reclamações públicas**, com 122 registros coletados do Reclame Aqui. Aqui utilizamos dois modelos de Machine Learning: o Random Forest para classificar a gravidade das reclamações, e o K-Means para agrupá-las em perfis de problema.

O terceiro pilar foi o **cruzamento das duas fontes**, buscando correlações entre os riscos financeiros e as dores dos clientes."

---

## 🟣 BLOCO 3 — SAÚDE FINANCEIRA (~3 min)

> *Slides: Painel de Capital · Decomposição do RWA · Gráfico Cascata · Projeções Q4*

**Fala sugerida:**

"Começando pela saúde financeira. O indicador mais importante aqui é o **Índice de Basileia**, que mede se o banco tem capital suficiente para cobrir seus riscos. O mínimo regulatório é 10,5%. O Nubank abriu 2025 em 16,9% — uma posição confortável — mas encerrou o Q3 em 14,6%, com uma queda acelerada que chama atenção.

*(apontar para o gráfico de linha)*
O que está puxando essa queda? Principalmente o crescimento do **RWA** — os ativos ponderados pelo risco. Em apenas 6 meses, ele subiu de R$135 bilhões para R$158 bilhões, impulsionado pela expansão agressiva da carteira de crédito.

Outro dado que nos surpreendeu foi o **RWA de câmbio**, que cresceu 882% entre o Q2 e o Q3 — em apenas um trimestre. Isso indica que o banco assumiu uma exposição cambial muito relevante num curto período.

E quando olhamos para a inadimplência — clientes que deixaram de pagar —, o cenário é igualmente preocupante. O estoque de ativos problemáticos saiu de R$13,5 bilhões para R$22,1 bilhões em um trimestre. Um crescimento de 64%.

*(apontar para o gráfico de projeção)*
Projetando essa tendência, o Índice de Basileia pode chegar a cerca de 11,4% no Q4 — apenas 0,9 ponto percentual acima do mínimo regulatório. Ainda dentro do limite, mas com margem muito reduzida."

---

## 🟣 BLOCO 4 — VOZ DO CLIENTE (~3 min)

> *Slides: Dashboard de Reclamações · Tabela de Clusters · Heatmap · Insights Avançados*

**Fala sugerida:**

"Agora vamos para o segundo pilar: o que os clientes estão dizendo.

Das 122 reclamações analisadas, a categoria mais frequente foi **Cartão de Crédito**, com 36 ocorrências, seguida por **Cobrança Indevida**, com 22. Mas quantidade não é tudo — o que realmente importa é o impacto.

Para ir além da contagem simples, aplicamos um algoritmo de **clustering** — que é uma técnica onde o modelo agrupa automaticamente os textos que se parecem entre si, sem que a gente precise definir os grupos previamente. Identificamos 4 perfis distintos:

- **Cluster 0** — PIX e contestações — risco médio
- **Cluster 1** — Bloqueio de conta — risco alto
- **Cluster 2** — Cobrança indevida — **risco máximo**, com 62% dos casos envolvendo perda financeira real
- **Cluster 3** — Problemas com cartão — risco alto, o maior volume

*(apontar para o heatmap)*
O mapa de calor confirma visualmente onde a concentração é maior: o ponto mais crítico está no cruzamento do Cluster 3 com Cartão de Crédito — 23 reclamações num único grupo.

Para completar a análise, treinamos um modelo **Random Forest** para classificar automaticamente a gravidade de qualquer reclamação nova. O modelo atingiu 94,6% de acurácia. As palavras que mais indicam uma reclamação grave são, nessa ordem: 'cobrança indevida', 'indevida' e 'cobrança'. Ou seja, o padrão linguístico dos clientes reflete diretamente o impacto financeiro que estão sofrendo."

---

## 🟣 BLOCO 5 — CRUZAMENTO DOS DADOS (~2 min)

> *Slide: Tabela de Cruzamento*

**Fala sugerida:**

"O ponto mais importante do trabalho é justamente a conexão entre os dois mundos.

Quando o banco cresce sua carteira de crédito de forma acelerada — o que explica o RWA subindo — ele acaba concedendo crédito a perfis de maior risco. Isso aparece no Bacen como inadimplência crescendo 64%. E aparece no Reclame Aqui como reclamações de cobrança indevida e juros abusivos.

São duas fontes de dado completamente diferentes contando a mesma história.

Um segundo cruzamento relevante: a explosão do RWA cambial de 882% não aparece nas reclamações — é um risco invisível para o cliente, mas muito visível para o regulador. Isso reforça a importância de monitorar os dois ângulos ao mesmo tempo.

Em resumo: **a política de crédito agressiva que sustenta o crescimento do Nubank está criando pressão simultânea nos indicadores regulatórios e na experiência dos clientes.**"

---

## 🟣 BLOCO 6 — PLANO DE AÇÃO E CONCLUSÃO (~2 min)

> *Slides: Plano de Ação · Conclusão*

**Fala sugerida:**

"Com base nos dados, chegamos a cinco recomendações prioritárias.

As duas primeiras são de natureza financeiro-regulatória: implementar um **hedge cambial estrutural** para reduzir a exposição de câmbio, e realizar uma **emissão de capital Nível II** para reforçar o Índice de Basileia antes que ele se aproxime demais do mínimo.

As três seguintes são operacionais: criar um sistema de **early warning de inadimplência** com Machine Learning para agir antes do cliente entrar em atraso grave; implementar **revisão automática de bloqueios** para reduzir os falsos positivos que frustram clientes; e **recalibrar a política de crédito** para equilibrar crescimento com sustentabilidade.

A meta consolidada é atingir, até o Q2 de 2026: Índice de Basileia acima de 15,5%, redução de 40% nas reclamações de cobrança e taxa de entrada na inadimplência abaixo de 50%.

**A conclusão geral é que o Nubank tem fundamentos sólidos e infraestrutura técnica muito melhorada — as reclamações de instabilidade caíram 99% desde setembro de 2024. Mas o modelo de crescimento agressivo está criando riscos que precisam ser gerenciados com mais cuidado antes que se tornem problemas maiores.**"

---

## 🟣 BLOCO 7 — ENCERRAMENTO (~30 seg)

**Fala sugerida:**

"Esse foi o Diagnóstico Estratégico 360° do Nubank. O diferencial do trabalho está na combinação de duas metodologias — análise regulatória quantitativa e mineração de texto com Machine Learning — para chegar a conclusões que nenhuma das duas sozinha permitiria.

Ficamos à disposição para perguntas."

---

## 💡 DICAS PARA A BANCA

- **Ao mostrar os gráficos**, sempre explique o eixo antes de comentar o resultado. Ex: *"Este gráfico mostra o tempo no eixo horizontal e o número de reclamações no eixo vertical..."*
- **Se perguntarem sobre o dataset**: mencione que são dados públicos do Reclame Aqui, não uma amostra estatisticamente representativa — é uma limitação que pode ser citada com naturalidade.
- **Se perguntarem sobre os modelos de ML**: explique que Random Forest é um conjunto de árvores de decisão e que K-Means agrupa pontos por proximidade no espaço vetorial — sem precisar entrar em matemática pesada.
- **Se o tempo apertar**: o Bloco 5 (cruzamento) pode ser resumido em 1 frase e o Bloco 2 (metodologia) pode ser mais rápido.
- **Mantenha contato visual** ao falar dos insights principais — eles são o coração do trabalho.

---
