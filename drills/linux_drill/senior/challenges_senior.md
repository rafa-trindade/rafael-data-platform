# Linux Drill — Nível Sênior

---

## 1. Processar um arquivo gigante sem carregar tudo na memória

**Cenário**: você recebe um arquivo de log de 5GB (simule com `docker logs lab-postgres --since 24h > log_grande.txt` se necessário, ou gere um arquivo grande de teste) e precisa contar quantas linhas contêm "ERROR", sem que seu editor de texto trave tentando abrir o arquivo inteiro.

**Tarefa**: use `grep -c` (que processa linha a linha, sem carregar o arquivo inteiro em memória) em vez de abrir o arquivo num editor. Compare mentalmente com o que aconteceria se você tentasse `cat arquivo | less` num arquivo de 50GB.

**Verificação**: o comando deve retornar rápido mesmo em arquivos grandes, sem consumo de memória proporcional ao tamanho do arquivo (confirme com `top` rodando em paralelo, se quiser ver o uso real).

---

## 2. Paralelismo com `xargs`

**Cenário**: você tem uma lista de 50 arquivos que precisam ser comprimidos (`gzip`), e fazer um por vez é lento — você quer paralelizar.

**Tarefa**: gere 10 arquivos de teste (`touch arquivo_{1..10}.txt`), e use `find` + `xargs -P` (com paralelismo) pra comprimir todos ao mesmo tempo, em vez de um loop sequencial.

**Verificação**: todos os arquivos devem virar `.gz`, e o tempo total deve ser visivelmente menor que rodar um por um (teste com `time` antes e depois).

---

## 3. Diagnosticar um pipeline lento — CPU, memória e disco

**Cenário**: alguém reporta que "o servidor está lento" durante a execução de um job pesado. Você precisa descobrir SE o problema é CPU, memória ou disco, sem acesso a ferramenta de monitoramento além do próprio terminal.

**Tarefa**: usando `top`/`htop` (CPU e memória), `df -h` (espaço em disco), e `iostat` ou `vmstat` (se disponível; se não, `cat /proc/loadavg`), monte um checklist mental de qual métrica olhar primeiro pra cada sintoma:
- Container reiniciando sozinho → o que checar?
- Query no Postgres muito lenta de repente → o que checar?
- Disco enchendo rápido sem explicação → o que checar?

**Verificação**: escreva (mentalmente ou em um arquivo `.md` de notas) qual comando você rodaria primeiro pra cada um dos 3 sintomas, e por quê.

---

## 4. Script shell robusto com tratamento de erro

**Cenário**: você quer melhorar um script simples pra que ele PARE imediatamente se qualquer comando falhar (em vez de continuar executando os próximos comandos silenciosamente, mascarando o erro).

**Tarefa**: escreva um script de teste com 3 comandos em sequência, onde o segundo comando propositalmente falha (ex: `cat arquivo_que_nao_existe.txt`). Rode sem `set -e` primeiro (observe que os comandos seguintes rodam mesmo assim), depois adicione `set -e` no topo do script e rode de novo.

**Verificação**: sem `set -e`, o terceiro comando executa mesmo depois da falha do segundo. Com `set -e`, o script para na hora que o segundo comando falha.

---

## 5. `trap` para limpeza garantida

**Cenário**: seu script cria um arquivo temporário durante a execução. Você quer garantir que esse arquivo temporário seja removido MESMO se o script falhar no meio ou for interrompido (Ctrl+C).

**Tarefa**: escreva um script que cria um arquivo temporário, usa `trap` pra registrar uma limpeza (`rm` do arquivo) que rode automaticamente ao sair do script (`EXIT`), depois simule uma falha no meio do script (ex: `exit 1` propositalmente) e confirme que o arquivo foi removido mesmo assim.

**Verificação**: depois do script terminar (com erro ou sem), o arquivo temporário não deve mais existir, independente de como o script terminou.

---

## 6. Analisar uso de disco por diretório

**Cenário**: o disco da VPS está enchendo e você precisa descobrir RAPIDAMENTE qual pasta está consumindo mais espaço, sem checar pasta por pasta manualmente.

**Tarefa**: use `du` com as flags certas pra listar o tamanho de cada subpasta de `/opt/rafael-data-platform`, ordenado do maior para o menor.

**Verificação**: o resultado deve mostrar `backups/` (provavelmente) no topo ou próximo do topo, já que é onde os dumps/backups se acumulam.