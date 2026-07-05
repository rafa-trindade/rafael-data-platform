# Data System Design Drill - Nível Pleno

---

## Case 1 - Pipeline de ingestão incremental

### Contexto
Você trabalha numa empresa de e-commerce. A equipe de vendas quer um
dashboard atualizado a cada hora com o faturamento do dia. A tabela
de origem (Postgres transacional) tem 50 milhões de linhas e cresce
200 mil linhas/dia. Você não pode fazer full load a cada hora.

### Perguntas
1. Como você desenharia a ingestão incremental? Que coluna/estratégia
   usaria para identificar "o que mudou desde a última execução"?
2. O que acontece se um registro for ATUALIZADO (não só inserido)
   depois da sua última carga? Sua estratégia cobre isso?
3. Como você trataria "late arriving data" - um registro com
   data_venda de ontem, mas que só chegou no sistema hoje de manhã?
4. Desenhe (texto) o fluxo completo: origem → bronze → silver → gold,
   indicando onde cada decisão acima se aplica.

### Resposta modelo

**1. Estratégia de incremental**: usar uma coluna de watermark, tipicamente
`updated_at` (timestamp de última modificação). A cada execução, guarda-se
o maior `updated_at` já processado; na próxima execução, filtra-se
`WHERE updated_at > ultimo_watermark`. Isso captura tanto inserts quanto
updates, desde que a tabela de origem mantenha esse campo atualizado
via trigger ou aplicação.

Se a tabela de origem **não** tiver essa coluna (cenário comum), a
alternativa é CDC de verdade (Debezium lendo o WAL do Postgres), que
captura toda mudança sem depender de a aplicação manter um campo.

**2. Updates**: cobertos pelo uso de `updated_at` como watermark - um
update muda esse campo, então o registro é recapturado na próxima
janela. O destino (silver) deve receber isso como **upsert** por chave
primária, não insert puro, senão duplica a linha.

**3. Late arriving data**: o watermark por `updated_at` já ajuda
parcialmente (o registro será capturado quando de fato chegar), mas
se a agregação de "faturamento do dia" já rodou e fechou aquela hora,
o dado atrasado não é refletido automaticamente. A solução é ter uma
**janela de reprocessamento**: sempre reprocessar as últimas N horas
de agregação (não só a hora corrente), aceitando o custo extra de
recomputar um pouco de histórico recente pra garantir completude.

**4. Fluxo**:

```
Postgres (origem)
→ [extração incremental via updated_at ou CDC]
→ Bronze (dados brutos, append-only, particionado por data de ingestão)
→ [upsert por chave, aplicando updated_at como critério de "mais recente"]
→ Silver (dados limpos, deduplicados, schema validado)
→ [agregação com janela de reprocessamento das últimas N horas]
→ Gold (faturamento por hora, consumido pelo dashboard)
```

### Follow-ups
- "E se a coluna updated_at não existir na tabela de origem?" → CDC via logical replication (Debezium) é a resposta esperada.
- "Como você garantiria que essa ingestão é idempotente se o job falhar na metade?" → upsert por chave primária no silver resolve isso naturalmente.
- "Que formato de arquivo você usaria no bronze, e por quê?" → Parquet ou até JSON/Avro se o schema muda com frequência; Parquet se já é relativamente estável e quer eficiência de leitura.

### Checklist de autoavaliação
- [ ] Mencionou watermark ou CDC como estratégia de incremental
- [ ] Considerou updates, não só inserts
- [ ] Tratou late arriving data com solução concreta (janela de reprocessamento)
- [ ] Desenhou o fluxo completo bronze → silver → gold

---

## Case 2 - Retry e monitoramento de um pipeline crítico

### Contexto
Um pipeline que carrega dados financeiros falha ocasionalmente por
timeout numa API externa. Quando falha silenciosamente, o time só
descobre 2 dias depois que o relatório financeiro está desatualizado.

### Perguntas
1. Como você desenharia a lógica de retry para essa chamada de API?
2. Que sinais de monitoramento você adicionaria pra não depender de
   alguém notar "manualmente" que o pipeline parou?
3. Retry indefinido é uma boa ideia? Por quê?

### Resposta modelo

**1. Retry**: usar backoff exponencial com jitter (pequena variação
aleatória no tempo de espera, pra evitar que múltiplas instâncias
retentem exatamente ao mesmo tempo e sobrecarreguem a API de novo - o
"thundering herd problem"). Limitar a um número máximo de tentativas
(ex: 5), e diferenciar erros **transitórios** (timeout, 503) - que
merecem retry - de erros **permanentes** (401 não autorizado, 400 bad
request) - que não devem ser retentados, pois vão falhar de novo do
mesmo jeito.

**2. Monitoramento**: pelo menos três sinais:
- **Alerta de falha**: notificação (Slack/email/PagerDuty) quando o
  pipeline falha após esgotar os retries.
- **Alerta de atraso (SLA)**: se o pipeline deveria ter rodado até às
  9h e não rodou, alertar mesmo sem "falha" explícita - pipeline que
  nunca chegou a executar é tão grave quanto pipeline que falhou.
- **Métrica de freshness dos dados**: monitorar "quantas horas desde
  a última carga bem-sucedida" como métrica contínua, com alerta se
  passar de um threshold - isso pega até situações que os dois
  alertas anteriores não cobrem (ex: pipeline "roda" mas processa
  zero registros por engano).

**3. Retry indefinido não é boa ideia**: se o erro for permanente
(credencial expirada, endpoint descontinuado), retry infinito
desperdiça recursos pra sempre sem nunca resolver, e pode mascarar o
problema real (ninguém percebe que está falhando, porque "está
tentando"). Sempre ter um limite de tentativas, e depois disso,
falhar de forma visível e alertável.

### Follow-ups
- "Como você diferenciaria, no código, um erro transitório de um permanente?" (checar código HTTP/tipo de exceção)
- "Esse pipeline financeiro merece um SLA mais agressivo que outros? Como isso mudaria seu design?"

### Checklist de autoavaliação
- [ ] Mencionou backoff exponencial (não retry fixo/imediato)
- [ ] Diferenciou erro transitório de permanente
- [ ] Propôs pelo menos 2 tipos de alerta/monitoramento diferentes
- [ ] Argumentou contra retry indefinido

---

## Case 3 - Isolamento entre Bronze, Silver e Gold

### Contexto
Um time júnior está construindo o primeiro data lake da empresa e
quer saber por que "simplesmente carregar tudo direto numa tabela
final" não é uma boa prática.

### Perguntas
1. Qual o propósito de cada camada (bronze, silver, gold)?
2. Que tipo de problema o isolamento entre camadas evita?
3. Dê um exemplo concreto de algo que só deveria acontecer no
   silver, não no bronze.

### Resposta modelo

**Propósito de cada camada**:
- **Bronze**: cópia fiel da fonte, sem transformação. Existe pra
  permitir reprocessamento caso alguma regra de negócio mude - se
  você só guarda dados já transformados, perde a capacidade de
  reconstruir o histórico com uma lógica nova.
- **Silver**: dados limpos, deduplicados, com schema validado e
  tipos corretos - mas ainda granular (não agregado), representando
  "a verdade" no nível de registro individual.
- **Gold**: dados agregados/modelados pra consumo direto (dashboards,
  relatórios) - otimizados pra leitura, não pra flexibilidade.

**Problema que o isolamento evita**: se você aplica transformação e
agregação direto na ingestão, qualquer bug na lógica de transformação
**corrompe o dado na origem irreversivelmente** - não há como voltar
e "reprocessar direito", porque o dado bruto original não foi
preservado. Isso também acopla a lógica de negócio à ingestão, então
qualquer mudança de regra exige re-ingerir tudo da fonte (que pode
não estar mais disponível/acessível).

**Exemplo concreto**: deduplicação e normalização de schema (schema
evolution) devem acontecer no silver, não no bronze. No bronze, você
quer o dado exatamente como veio - inclusive duplicatas e
inconsistências - porque isso é evidência útil pra debugar problemas
na origem. É no silver que você decide "qual das duplicatas manter" e
"como normalizar campos que mudaram de formato ao longo do tempo".

### Follow-ups
- "Isso significa que bronze nunca deve ser deletado?" → geralmente sim, ou mantido por um período de retenção longo, justamente pela capacidade de reprocessamento.
- "Como você lidaria com dados sensíveis (PII) que precisam ser mascarados? Em qual camada isso acontece?"

### Checklist de autoavaliação
- [ ] Explicou o propósito de cada camada corretamente
- [ ] Argumentou por que "pular direto pra gold" é arriscado
- [ ] Deu um exemplo concreto de transformação que pertence ao silver