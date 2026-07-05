# Data System Design Drill - Nível Sênior

---

## Case 1 - Arquitetura para 500 milhões de eventos/dia

### Contexto
Você foi contratado pra desenhar do zero a arquitetura de ingestão de
eventos de uma plataforma que gera 500 milhões de eventos por dia
(cliques, page views, transações). O time de produto quer análises
tanto em near-real-time (dashboards operacionais) quanto batch
(relatórios diários consolidados).

### Perguntas
1. Você faria ingestão batch, streaming, ou os dois? Justifique.
2. Como você desenharia a arquitetura de ponta a ponta?
3. Como garantiria idempotência nessa escala?
4. Como monitoraria a saúde desse pipeline?
5. Como escalaria isso se o volume triplicasse?

### Resposta modelo

**1. Batch e streaming, arquitetura Lambda/Kappa híbrida**: dado que
existem dois casos de uso com necessidades de latência muito
diferentes (near-real-time vs relatório diário consolidado), a
resposta mais robusta é **não escolher um só**. Uma arquitetura
comum: ingestão via streaming (Kafka/Kinesis) alimentando dois
consumidores - um caminho "hot" que processa em near-real-time
(Flink/Spark Streaming) pra dashboards operacionais, e um caminho
"cold" que grava o raw no data lake (bronze) e processa em batch
(Spark) pra consolidação diária. Isso é a essência da arquitetura
Lambda; uma alternativa mais moderna (Kappa) usa só o pipeline de
streaming e reprocessa lendo o próprio stream retido por mais tempo,
evitando manter duas lógicas de processamento em paralelo.

**2. Arquitetura de ponta a ponta**:

```
Fontes de eventos
→ Kafka/Kinesis (buffer, replay, decoupling entre produtores e consumidores)
→ Stream processor (Flink/Spark Streaming) → Gold "hot" (métricas near-real-time)
→ Sink pro Data Lake (bronze, particionado por data+hora, formato Parquet/Avro)
→ Spark batch job (diário) → Silver (limpo, deduplicado)
→ Modelagem dimensional → Gold "cold" (relatórios consolidados)
```

**3. Idempotência nessa escala**: cada evento deve ter um ID único
(gerado na origem, não no pipeline) - isso permite deduplicação por
chave em qualquer ponto do pipeline. No lado do stream processor,
usar **exactly-once semantics** quando o processor suportar (Flink
com checkpointing, Kafka com transações). No lado batch, garantir que
a escrita no data lake seja idempotente via partição fixa +
overwrite (reescrever a partição inteira do dia, não fazer append
sujeito a duplicação em reprocessamento).

**4. Monitoramento**: latência end-to-end (tempo entre evento gerado
e evento disponível no destino), taxa de erros/eventos descartados
por validação, lag do consumer Kafka (quão atrasado o processamento
está em relação à produção), volume de eventos por minuto comparado
a uma baseline histórica (detecta queda anormal = problema na fonte
ou no pipeline).

**5. Escalar 3x**: Kafka escala horizontalmente adicionando partições
e brokers; o stream processor escala adicionando task managers/workers.
O ponto de atenção real geralmente não é throughput bruto, mas
**hotspots de particionamento** - se a chave de partição do Kafka
não distribui bem (ex: 80% dos eventos vêm de poucos usuários "hot"),
triplicar o cluster não ajuda tanto quanto parece. Vale revisar a
estratégia de partition key antes de simplesmente adicionar máquinas.

### Follow-ups
- "Por que não simplesmente usar streaming pra tudo, incluindo o relatório diário?" (custo de manter estado por mais tempo, complexidade de reprocessamento histórico)
- "Como você lidaria com um bug na lógica de transformação descoberto depois de 3 dias em produção?" (reprocessar do bronze, que preserva o raw)
- "O que é exactly-once, e por que é mais difícil de garantir em streaming do que em batch?"

### Checklist de autoavaliação
- [ ] Justificou a escolha batch+streaming (não escolheu um só sem razão)
- [ ] Desenhou um fluxo com componentes concretos, não abstrato
- [ ] Abordou idempotência com mecanismo específico (ID único, exactly-once, overwrite de partição)
- [ ] Identificou hotspot de partição como risco real de escalabilidade

---

## Case 2 - Shuffle, broadcast join e formatos de tabela aberta

### Contexto
Um pipeline Spark que faz join entre uma tabela de 2 bilhões de linhas
(fatos) e uma tabela de 500 linhas (dimensão pequena) está lento e
gerando muito shuffle.

### Perguntas
1. Por que esse join está gerando shuffle, e como evitar?
2. Quando você usaria broadcast join, e quando NÃO usaria?
3. Quando você optaria por Delta Lake ou Iceberg em vez de Parquet puro?

### Resposta modelo

**1. Por que gera shuffle**: por padrão, Spark faz um "sort-merge
join" para joins grandes - isso exige repartitionar (embaralhar) os
dados de ambos os lados da mesma chave pros mesmos nodes, o que é
uma operação cara de rede e disco (shuffle). Quando um dos lados é
pequeno (a dimensão de 500 linhas), esse shuffle é desnecessário.

**Como evitar**: usar **broadcast join** - copiar a tabela pequena
inteira pra memória de TODOS os executors, e cada executor faz o
join localmente contra sua partição da tabela grande, sem shuffle
algum no lado grande. O Spark faz isso automaticamente se a tabela
pequena estiver abaixo de um threshold configurável
(`spark.sql.autoBroadcastJoinThreshold`), mas pode ser forçado
explicitamente com um hint (`broadcast()`).

**2. Quando usar broadcast join**: quando um dos lados do join é
pequeno o suficiente pra caber confortavelmente na memória de cada
executor (tipicamente até ~10MB-1GB dependendo do cluster). **Quando
NÃO usar**: se a tabela "pequena" na verdade não é tão pequena (ex:
crescer além do esperado), forçar broadcast pode causar
**out-of-memory** nos executors - o hint não valida o tamanho real
em tempo de execução do jeito que o comportamento automático faz.
Também não faz sentido se ambos os lados do join são grandes - aí o
shuffle é inevitável e broadcast não se aplica.

**3. Delta Lake/Iceberg vs Parquet puro**: Parquet puro não suporta
ACID, updates/deletes eficientes, nem time travel - é só um formato
de arquivo. Delta Lake ou Iceberg adicionam uma camada de
metadados/transação sobre arquivos Parquet, permitindo: MERGE/UPSERT
eficiente (essencial se a tabela recebe CDC), time travel (consultar
"como a tabela estava ontem"), schema evolution controlada, e leitura
concorrente segura durante escritas. A escolha entre os dois dois
geralmente depende do ecossistema: Delta Lake tem integração mais
madura com Databricks/Spark; Iceberg é mais neutro em relação a
engine (Trino, Flink, Spark, Dremio o suportam nativamente) - se o
ambiente usa múltiplos engines (o caso deste projeto, com Dremio),
Iceberg tende a ser a escolha mais interoperável.

### Follow-ups
- "O que acontece se você forçar broadcast numa tabela que na verdade tem 5GB?"
- "Time travel é só uma curiosidade ou tem uso prático real? Dê um exemplo."
- "Como Iceberg lida com schema evolution de um jeito que Parquet puro não consegue?"

### Checklist de autoavaliação
- [ ] Explicou shuffle corretamente (não confundiu com partição física)
- [ ] Sabe quando broadcast falha/não deve ser usado, não só quando funciona
- [ ] Diferenciou Parquet (formato de arquivo) de Delta/Iceberg (camada de tabela)

---

## Case 3 - Arquitetura para múltiplos consumidores

### Contexto
Uma mesma tabela de "pedidos" precisa ser consumida por: um time de
BI (queries analíticas pesadas, poucas vezes ao dia), uma API de
e-commerce (queries pontuais de baixa latência, alto volume de
requisições), e um time de ML (leitura em batch pra treinar modelos,
uma vez por semana).

### Perguntas
1. Esses três consumidores deveriam ler da MESMA tabela/sistema?
2. Como você desenharia a arquitetura pra atender os três sem que um
   afete a performance dos outros?
3. Como você evitaria inconsistência entre o que cada consumidor vê?

### Resposta modelo

**1. Não deveriam ler do mesmo sistema físico diretamente.** Cada
consumidor tem um padrão de acesso fundamentalmente diferente
(analítico pesado vs transacional de baixa latência vs batch
semanal), e sistemas otimizados pra um padrão são ruins pro outro -
um banco transacional (Postgres) não é bom pra scan analítico
pesado; um data warehouse columnar não é bom pra latência de
milissegundos numa API.

**2. Arquitetura**: manter uma fonte de verdade única (o banco
transacional de origem, ou um lakehouse central), e replicar/derivar
views especializadas por consumidor:
- **BI**: replicar (via CDC ou ELT periódico) pra um Data Warehouse
  otimizado pra analítica (Postgres com schema analytics, ou
  Snowflake/BigQuery em escala maior).
- **API de e-commerce**: manter um cache (Redis) ou uma réplica de
  leitura (read replica) do banco transacional, isolando o tráfego
  de leitura de alto volume do banco principal de escrita.
- **ML**: consumir do data lake (bronze/silver), não do transacional
  nem do DW de BI - batch semanal tolera latência maior e se beneficia
  de dados já em formato columnar (Parquet) pra leitura eficiente em
  volume.

Isso é o princípio de **isolar padrões de acesso**: cada consumidor
lê de um armazenamento adequado ao seu próprio perfil, todos
alimentados a partir de uma única fonte de verdade, evitando que o
time de BI rodando uma query pesada de repente deixe a API do site
lenta.

**3. Consistência entre consumidores**: como cada um lê uma réplica/
derivação diferente, é normal que existam pequenas defasagens de
tempo (o DW de BI pode estar 15 minutos atrás do transacional, por
exemplo). O importante é que isso seja **conhecido e comunicado**
(SLA de freshness por consumidor), não escondido. Se consistência
forte entre todos for um requisito real de negócio (raro, mas
possível), a arquitetura precisa de um mecanismo mais caro, como
CDC com replicação síncrona - mas isso deve ser justificado pelo
requisito, não assumido por padrão.

### Follow-ups
- "O time de BI reclama que os dados do DW estão sempre 20 minutos atrasados em relação ao sistema principal. Isso é um problema de arquitetura?"
- "Como você decidiria SE vale a pena ter um cache Redis na frente do banco transacional, versus simplesmente escalar o banco?"

### Checklist de autoavaliação
- [ ] Reconheceu que padrões de acesso diferentes pedem armazenamentos diferentes
- [ ] Manteve o conceito de fonte única de verdade, não desenhou 3 sistemas desconectados
- [ ] Discutiu consistência/freshness como trade-off explícito, não ignorou o tema