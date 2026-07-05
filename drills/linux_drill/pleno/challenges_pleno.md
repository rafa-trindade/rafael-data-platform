# Linux Drill - Nível Pleno

---

## 1. Extrair e transformar colunas de log (`awk`)

**Cenário**: os logs do Postgres têm timestamp, nível (LOG/FATAL/ERROR) e mensagem, separados por espaços. Você quer extrair só o nível de cada linha, pra saber a distribuição de severidade.

**Tarefa**: usando `docker logs lab-postgres` + `awk`, extraia a terceira "palavra" de cada linha de log (geralmente onde fica o nível) e conte a ocorrência de cada valor distinto.

**Verificação**: você deve conseguir ver algo como uma contagem de "LOG", "FATAL", etc - combine com `sort` + `uniq -c` no final do pipeline.

---

## 2. Substituição de texto em massa (`sed`)

**Cenário**: você quer testar uma mudança no `docker-compose.yml` - trocar temporariamente a porta `9047` do Dremio por `9048` - sem editar manualmente no VS Code.

**Tarefa**: use `sed` pra fazer essa substituição direto no terminal, primeiro só EXIBINDO o resultado (sem alterar o arquivo), depois de fato aplicando a mudança num arquivo de cópia (nunca teste `sed -i` direto no arquivo de produção sem backup).

**Verificação**: `cat` no arquivo de cópia deve mostrar `9048` no lugar de `9047`, e o arquivo original deve continuar intacto.

---

## 3. Ordenar e deduplicar (`sort` + `uniq`)

**Cenário**: você tem uma lista de IPs que tentaram acessar sua VPS (do `/var/log/ufw.log`) e quer saber quais IPs aparecem com mais frequência.

**Tarefa**: extraia os IPs de origem (`SRC=`) das linhas de bloqueio do UFW, ordene, e conte a frequência de cada IP único, mostrando os 5 mais frequentes.

**Verificação**: o resultado deve ser uma lista ordenada por frequência (mais alto primeiro), com no máximo 5 linhas.

---

## 4. Agendamento com `cron`

**Cenário**: você quer que o `scripts/backup.sh` rode automaticamente todo dia às 3h da manhã, sem precisar lembrar de rodar manualmente.

**Tarefa**: configure uma entrada no crontab do usuário pra isso, redirecionando a saída (stdout e stderr) pra um arquivo de log.

**Verificação**: `crontab -l` deve mostrar a entrada configurada corretamente, com o caminho absoluto do script (cron não usa o mesmo `$PATH`/diretório do seu shell interativo).

---

## 5. Variáveis de ambiente em scripts

**Cenário**: seu `scripts/backup.sh` hoje lê credenciais direto do `docker/.env` via `grep`. Você quer entender a diferença entre isso e exportar variáveis de ambiente pra sessão.

**Tarefa**: exporte manualmente uma variável (`export MEU_TESTE=valor`), confirme que ela existe na sessão atual, depois abra um NOVO terminal/sessão e confirme que ela NÃO existe mais lá (não persiste entre sessões, a menos que colocada em `.bashrc`).

**Verificação**: `echo $MEU_TESTE` deve funcionar na sessão original e falhar (vazio) numa sessão nova.

---

## 6. Gerenciamento de processos (`ps`, `kill`, `nohup`)

**Cenário**: você rodou um script de teste (`sleep 300`, simulando um processo longo) e agora precisa: (a) encontrar o PID dele, (b) encerrá-lo antes do tempo, (c) rodar de novo mas de um jeito que sobreviva mesmo se você desconectar do SSH.

**Tarefa**: rode `sleep 300 &`, encontre o PID com `ps aux | grep sleep`, mate com `kill`. Depois rode de novo usando `nohup sleep 300 &`, feche o terminal (ou desconecte o SSH), reconecte e confirme que o processo ainda está rodando.

**Verificação**: depois de reconectar, `ps aux | grep sleep` ainda deve mostrar o processo ativo (prova que sobreviveu à desconexão).

---

## 7. Monitorar recursos em tempo real

**Cenário**: você quer saber, sem entrar no Portainer, quanto de CPU e memória cada container `lab-*` está consumindo agora.

**Tarefa**: use `docker stats` (com a flag pra não ficar em loop infinito, se preferir) pra ver isso direto no terminal.

**Verificação**: a saída deve listar todos os containers ativos com percentual de CPU e uso de memória.