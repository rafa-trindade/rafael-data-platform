# Git Drill — Nível Pleno

---

## 1. Conflito em múltiplos arquivos

**Cenário**: você e um colega trabalharam em paralelo em 3 arquivos diferentes do mesmo pipeline (`extract.py`, `transform.py`, `load.py`), e 2 deles têm conflito na hora do merge.

**Tarefa**: crie os 3 arquivos na `main`, comite. Crie uma branch, edite `extract.py` e `transform.py` (deixe `load.py` intacto), comite. Volte pra `main`, edite as MESMAS linhas de `extract.py` e `transform.py` de forma diferente, comite. Tente merge — resolva os dois conflitos, um por vez, sem se confundir sobre qual arquivo já foi resolvido.

**Verificação**: `git status` deve mostrar claramente quais arquivos ainda têm conflito (`both modified`) durante o processo, e nenhum no final.

---

## 2. Merge vs Rebase — mesma situação, duas abordagens

**Cenário**: você tem uma branch de feature com 3 commits, e a `main` avançou enquanto você trabalhava. Você quer trazer sua branch atualizada.

**Tarefa**: faça isso DUAS vezes em branches separadas (`feature-merge` e `feature-rebase`, ambas partindo do mesmo ponto): numa, atualize com `git merge main`; na outra, atualize com `git rebase main`. Compare o histórico resultante com `git log --graph --oneline` nas duas branches.

**Verificação**: você deve conseguir explicar, olhando os dois grafos, por que um mantém um "commit de merge" extra e o outro reescreve o histórico linearmente — e qual prefere usar em qual situação (branch compartilhada vs branch pessoal).

---

## 3. Desfazer um commit já enviado (revert vs reset)

**Cenário**: você fez push de um commit que quebrou um pipeline em produção. A branch é compartilhada com outras pessoas, então você NÃO pode reescrever o histórico (force-push é perigoso ali).

**Tarefa**: faça um commit "quebrado" e dê push. Desfaça ele com `git revert` (não com `reset`), e dê push de novo.

**Verificação**: o histórico deve mostrar DOIS commits (o original e o revert), não o commit original desaparecendo — isso é o que torna seguro fazer em branch compartilhada.

**Contraste (só pra entender, não pra fazer em branch real)**: se fosse uma branch só sua, local, ainda não compartilhada, `git reset --hard HEAD~1` removeria o commit inteiramente do histórico — mas isso reescreve história, nunca faça isso numa branch que outros já puxaram.

---

## 4. `git stash` no meio de uma troca de contexto

**Cenário**: você está no meio de uma mudança não-finalizada quando alguém pede urgentemente pra você corrigir um bug crítico em outra branch. Você não quer commitar a mudança incompleta, mas também não quer perdê-la.

**Tarefa**: comece a editar um arquivo (sem commitar), rode `git stash` pra guardar a mudança temporariamente, mude de branch, faça o "hotfix" simulado, volte pra branch original, e recupere a mudança guardada com `git stash pop`.

**Verificação**: depois do `stash`, `git status` deve estar limpo (como se a mudança nunca tivesse existido); depois do `pop`, a mudança deve voltar exatamente como estava.

---

## 5. Investigar histórico de um arquivo específico

**Cenário**: você quer entender quando e por que uma linha específica de um arquivo de configuração foi alterada, sem abrir cada commit manualmente.

**Tarefa**: faça 3-4 commits alterando o mesmo arquivo ao longo do tempo. Use `git log -p -- nome_do_arquivo` (mostra o diff de cada commit que tocou aquele arquivo) e `git blame nome_do_arquivo` (mostra quem/quando editou cada linha) pra rastrear a origem de uma linha específica.

**Verificação**: você deve conseguir apontar exatamente em qual commit uma linha específica foi introduzida ou modificada.