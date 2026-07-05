# Linux Drill - Nível Junior

---

## 1. Navegação e inspeção rápida

**Cenário**: você acabou de entrar via SSH numa VPS que nunca usou antes e precisa se orientar rápido.

**Tarefa**: sem usar nenhuma ferramenta gráfica, descubra:
- Em qual diretório você está agora
- O que existe dentro de `/opt/rafael-data-platform` (listagem detalhada, incluindo arquivos ocultos)
- O tamanho total da pasta `backups/`

**Verificação**: você deve conseguir responder as três perguntas usando só `pwd`, `ls -la` e `du -sh`, sem abrir nenhum editor.

---

## 2. Permissões de arquivo

**Cenário**: um script (`scripts/backup.sh`) não está executando quando você tenta rodar `./scripts/backup.sh` - dá erro de "Permission denied".

**Tarefa**: diagnostique o problema usando `ls -l`, identifique o que falta, e corrija com `chmod`.

**Verificação**: depois da correção, `./scripts/backup.sh` deve rodar sem erro de permissão (mesmo que falhe por outro motivo depois).

---

## 3. Buscar texto dentro de arquivos (`grep`)

**Cenário**: você suspeita que um erro específico ("connection refused") apareceu nos logs do Postgres em algum momento, mas não sabe quando.

**Tarefa**: usando `docker logs lab-postgres` combinado com `grep`, encontre todas as linhas que contêm "FATAL" nos últimos logs. Depois, refine pra contar QUANTAS vezes isso aconteceu (sem contar manualmente).

**Verificação**: seu comando final deve retornar um número (não uma lista) usando `grep -c` ou `wc -l`.

---

## 4. Encontrar arquivos (`find`)

**Cenário**: você quer saber quais arquivos `.sql` existem em todo o projeto, sem saber de cor onde cada um está.

**Tarefa**: use `find` a partir da raiz do projeto pra listar todos os arquivos terminados em `.sql`.

**Verificação**: a saída deve incluir pelo menos os arquivos de `drills/sql-drill/`, sem listar nada de fora do projeto.

---

## 5. Contar linhas, palavras, caracteres (`wc`)

**Cenário**: você quer saber rapidamente o "tamanho" de um dos seus arquivos de drill sem abrir ele.

**Tarefa**: usando `wc`, descubra quantas linhas tem o arquivo `drills/sql-drill/drill_sql_01/seed_drill_01.sql`.

**Verificação**: o número deve bater com o que aparece no VS Code (contagem de linhas do editor).

---

## 6. Pipes e encadeamento de comandos

**Cenário**: você quer saber quantos containers `lab-*` estão rodando agora, sem contar na mão a lista do `docker ps`.

**Tarefa**: combine `docker ps` com `grep` e `wc -l` num único comando encadeado por pipe (`|`).

**Verificação**: o resultado deve bater com a contagem visual de containers ativos.

---

## 7. Redirecionamento de saída

**Cenário**: você quer salvar o resultado de um `docker ps` num arquivo de texto, pra consultar depois sem precisar rodar o comando de novo.

**Tarefa**: redirecione a saída de `docker ps` pra um arquivo `status.txt`. Depois, faça de novo mas ADICIONANDO ao final do arquivo (sem sobrescrever), rodando o comando outra vez.

**Verificação**: o arquivo deve conter duas cópias do resultado depois do segundo comando (você usou `>` na primeira vez, `>>` na segunda).

---

## 8. Variáveis de ambiente básicas (leitura)

**Cenário**: você quer confirmar rapidamente qual usuário do sistema está logado e qual é o diretório "home" dele, sem digitar de cabeça.

**Tarefa**: use variáveis de ambiente (`$USER`, `$HOME`) num comando `echo` pra exibir as duas informações numa linha só.

**Verificação**: a saída deve mostrar seu usuário real (`rafael`) e o caminho `/home/rafael`.