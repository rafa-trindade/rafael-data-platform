# Git Drill — Nível Junior

Crie um sandbox antes de começar:
```bash
mkdir -p ~/git-drill-sandbox && cd ~/git-drill-sandbox && git init
```

---

## 1. Fluxo básico: add, commit, push

**Cenário**: primeiro dia num time novo. Você precisa fazer sua primeira mudança e mandar pro repositório remoto.

**Tarefa**: crie um arquivo `README.md` com qualquer conteúdo, adicione ao stage, comite com uma mensagem clara, e (se tiver um remoto configurado, ex: um repo vazio no GitHub) faça push.

**Verificação**: `git log --oneline` deve mostrar seu commit; `git status` deve dizer "nothing to commit, working tree clean".

---

## 2. `.gitignore`

**Cenário**: você criou um arquivo `.env` com senha de banco de dados por engano dentro do repositório, e quer garantir que ele NUNCA seja commitado, mesmo por acidente no futuro.

**Tarefa**: crie um arquivo `.env` com conteúdo fictício, crie um `.gitignore` que o ignore, confirme que `git status` não lista o `.env` como pendente.

**Verificação**: `git status` não deve mencionar `.env` em nenhuma hipótese, mesmo depois de `git add -A`.

---

## 3. Criar e trocar de branch

**Cenário**: você precisa trabalhar numa feature sem afetar a branch principal (`main`) até terminar.

**Tarefa**: crie uma branch chamada `feature/teste`, mude pra ela, faça um commit ali, e volte pra `main` — confirme que o commit da feature não aparece na `main`.

**Verificação**: `git log --oneline` na `main` não deve mostrar o commit feito em `feature/teste`.

---

## 4. Merge simples (sem conflito)

**Cenário**: sua feature está pronta e você quer trazer ela de volta pra `main`.

**Tarefa**: estando na `main`, rode `git merge feature/teste`.

**Verificação**: o commit da feature agora aparece no histórico da `main`.

---

## 5. Primeiro conflito (arquivo único, mudança simples)

**Cenário**: você e um colega (simulado por você mesmo, em duas branches diferentes) editaram a MESMA linha do mesmo arquivo de jeitos diferentes.

**Tarefa**: crie um arquivo `config.txt` com uma linha `versao=1` na `main`, comite. Crie uma branch `branch-a`, mude a linha pra `versao=2`, comite. Volte pra `main`, mude a mesma linha pra `versao=3`, comite. Tente fazer merge de `branch-a` na `main` — vai dar conflito. Resolva manualmente escolhendo um valor, marque como resolvido, finalize o merge.

**Verificação**: depois de resolver, `git status` deve estar limpo, e o arquivo `config.txt` deve ter só uma versão final da linha (sem os marcadores `<<<<<<<`, `=======`, `>>>>>>>` sobrando).

---

## 6. Diferença entre `pull` e `fetch`

**Cenário**: você quer ver o que mudou no remoto SEM aplicar automaticamente na sua branch local.

**Tarefa**: rode `git fetch` (sem merge automático), depois compare sua branch local com a remota (`git log main..origin/main` ou `git diff main origin/main`), e só então decida rodar `git pull` (ou `git merge origin/main`) pra aplicar.

**Verificação**: depois do `fetch`, seus arquivos locais não devem ter mudado ainda — só depois do merge/pull explícito.