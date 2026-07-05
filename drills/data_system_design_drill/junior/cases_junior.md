# Data System Design Drill - Nível Junior

---

## Case 1 - Batch vs Streaming: escolha de estratégia

### Contexto
Uma empresa de varejo quer atualizar o estoque disponível no site
sempre que uma venda acontece numa loja física. O time de dados
precisa decidir: essa ingestão deve ser batch ou streaming?

### Perguntas
1. Quais fatores você consideraria pra decidir entre batch e streaming aqui?
2. Que latência é aceitável nesse cenário, e por quê?
3. Se a resposta for "depende", quais as duas opções e quando cada uma se aplica?

### Resposta modelo

O fator decisivo aqui é **quão rápido a informação precisa refletir
no destino**. Estoque errado no site gera venda de produto que não
existe - isso é um problema de experiência do cliente, não só de
dados.

**Streaming** se justifica quando:
- O negócio realmente precisa de atualização em segundos/minutos (evitar overselling)
- Existe infraestrutura de mensageria disponível (Kafka, Kinesis, etc) ou justificativa pra criar uma
- O volume de eventos é constante o suficiente pra não desperdiçar
  recursos com um sistema sempre ligado

**Batch** se justifica quando:
- Uma janela de atualização de 15-60 minutos é aceitável pro negócio
- Simplicidade operacional importa mais que latência mínima
- O time não tem maturidade/infra de streaming ainda

**Resposta esperada para este caso específico**: estoque de e-commerce
tipicamente justifica **streaming** (ou near-real-time via micro-batch
de poucos minutos), porque overselling gera cancelamento de pedido e
prejuízo direto ao cliente. Mas é importante que o candidato **não
responda "streaming" de cara sem justificar o trade-off** - o valor
da resposta está em explicar o raciocínio, não em acertar a palavra certa.

### Follow-ups que um entrevistador faria
- "E se o volume de vendas for muito baixo (10 vendas/dia)? Streaming ainda se justifica?"
- "Como você mediria se a solução escolhida está atendendo a latência esperada?"

### Checklist de autoavaliação
- [ ] Mencionou latência aceitável como critério central
- [ ] Considerou custo/complexidade operacional do streaming
- [ ] Não deu uma resposta binária sem justificar trade-off

---

## Case 2 - Idempotência numa carga diária

### Contexto
Um pipeline batch roda todo dia às 3h da manhã, carregando vendas do
dia anterior num Data Warehouse. Um analistate pergunta: "e se esse
job travar na metade e alguém rodar de novo manualmente às 9h? Vamos
duplicar dados?"

### Perguntas
1. O que é idempotência, em termos simples?
2. Quais estratégias você usaria pra garantir que rodar o mesmo job
   duas vezes não duplica dados?
3. Isso muda se a carga for um INSERT puro vs um MERGE/UPSERT?

### Resposta modelo

**Idempotência** significa que executar a mesma operação múltiplas
vezes produz o mesmo resultado que executar uma única vez - não há
efeito colateral acumulativo.

Estratégias comuns:
- **Truncate-and-load**: apaga a partição/tabela de destino antes de
  carregar de novo. Simples, mas só funciona bem se a carga é sempre
  do "dia completo" (não incremental).
- **Upsert por chave (merge)**: usa uma chave de negócio (ex: venda_id)
  pra decidir se insere ou atualiza. Rodar duas vezes com o mesmo
  input resulta no mesmo estado final.
- **Deduplicação antes da escrita**: remove duplicatas do próprio
  lote antes de escrever, útil quando a fonte pode reenviar o mesmo
  registro.

Se a carga é um **INSERT puro** (sem verificação de chave), rodar duas
vezes literalmente duplica cada linha - não é idempotente por
natureza. Se é um **MERGE/UPSERT** por chave, a operação já é
idempotente por construção, desde que a chave de negócio seja estável
e única.

**Resposta esperada**: o candidato deve reconhecer que a estratégia
correta pra esse cenário (reprocessamento acidental) é usar
truncate-and-load na partição do dia específico, OU upsert por chave
- ambas resolvem o problema, com trade-offs diferentes de custo e
complexidade.

### Follow-ups
- "Se a tabela de destino for muito grande, truncate-and-load da tabela inteira é uma boa ideia?"
- "Como você garantiria que ninguém rode o job manual e o agendado ao mesmo tempo?" (dica: lock/mutex distribuído)

### Checklist de autoavaliação
- [ ] Definiu idempotência corretamente
- [ ] Citou pelo menos duas estratégias concretas
- [ ] Diferenciou insert puro de upsert em termos de idempotência

---

## Case 3 - Particionamento de uma tabela de eventos

### Contexto
Uma tabela de eventos de cliques tem 2 bilhões de linhas e cresce
5 milhões de linhas por dia. As queries mais comuns filtram por
intervalo de data (ex: "eventos dos últimos 7 dias").

### Perguntas
1. Por que particionamento importa nesse cenário?
2. Que coluna você usaria como chave de partição, e por quê?
3. Existe algum risco de particionar "errado" aqui?

### Resposta modelo

Particionamento existe pra evitar que uma query precise escanear TODA
a tabela quando só precisa de uma fração dela - isso é chamado de
**partition pruning**. Sem partição, uma query "últimos 7 dias" numa
tabela de 2 bilhões de linhas faria full scan, sendo ordens de
magnitude mais lenta e cara (especialmente em engines que cobram por
dado escaneado, como Athena/BigQuery).

**Coluna de partição**: a data do evento (ex: `data_evento`), granularidade
diária (`ano/mes/dia`), já que o padrão de acesso dominante é filtro por
data. Particionar por algo que não é usado nos filtros (ex: `usuario_id`)
não ajuda em nada as queries típicas.

**Risco de particionar errado**: **partições pequenas demais** (ex: por
hora, quando o volume diário já é gerenciável) geram excesso de
arquivos pequenos, degradando performance de leitura (problema
conhecido como "small file problem"). Partições grandes demais (ex:
por ano, numa tabela que cresce rápido) fazem cada partição virar
gigante e perder o benefício do pruning. O equilíbrio certo depende
do volume diário e do padrão de consulta.

### Follow-ups
- "Se 90% das queries filtram por usuario_id E por data, você particionaria por ambos?"
- "O que muda se a tabela for Parquet num data lake vs uma tabela nativa de Postgres particionada?"

### Checklist de autoavaliação
- [ ] Explicou partition pruning corretamente
- [ ] Escolheu partição alinhada ao padrão de consulta, não arbitrária
- [ ] Mencionou o risco de partições pequenas/grandes demais