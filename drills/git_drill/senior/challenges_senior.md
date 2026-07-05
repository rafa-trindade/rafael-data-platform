# Git Drill — Nível Sênior

---

## 1. Rebase interativo pra limpar histórico antes de um PR

**Cenário**: você trabalhou numa feature por 2 dias e acumulou 8 commits desorganizados ("wip", "fix typo", "teste", "agora funciona"). Antes de abrir o PR, você quer apresentar um histórico limpo e compreensível pro time.

**Tarefa**: crie uma branch com pelo menos 5 commits "sujos" (mensagens ruins, alguns fixes triviais). Use `git rebase -i HEAD~5` pra: squash (juntar) commits relacionados, reescrever mensagens, e reordenar se fizer sentido.

**Verificação**: depois do rebase, `git log --oneline` deve mostrar um histórico bem menor e com mensagens que contam uma história coerente, não o caos original.

---

## 2. `git bisect` pra achar o commit que quebrou algo

**Cenário**: uma DAG (ou qualquer script) que funcionava há uma semana está falhando agora, e você não sabe em qual dos ~15 commits recentes o bug foi introduzido.

**Tarefa**: crie um repositório de teste com uma sequência de commits, onde um commit no meio (ex: o 8º) introduz deliberadamente um bug (ex: uma função que passa a retornar errado). Use `git bisect start`, marque o commit atual como `bad` e um commit antigo conhecido como `good`, e deixe o bisect fazer busca binária até apontar o commit exato.

**Verificação**: o `git bisect` deve convergir pro commit correto em `log2(n)` passos, não percorrendo todos os 15 manualmente.

---

## 3. Conflito em arquivo gerado automaticamente (lock file)

**Cenário**: dois desenvolvedores adicionaram dependências Python diferentes ao mesmo projeto, e o `requirements.txt` (ou um lock file equivalente) tem conflito — mas esse tipo de arquivo não deve ser editado "criativamente" como texto livre, tem estrutura/ordem que importa.

**Tarefa**: simule duas branches adicionando linhas diferentes ao mesmo `requirements.txt` na mesma posição. Ao resolver o conflito, em vez de escolher um lado ou o outro arbitrariamente, **combine ambas as dependências** de forma que o arquivo final faça sentido (sem duplicar, mantendo ordem alfabética se essa for a convenção do projeto).

**Verificação**: o `requirements.txt` final deve conter AMBAS as dependências adicionadas nas duas branches, sem duplicação, sem marcadores de conflito sobrando.

---

## 4. Hook de pre-commit (lint automático)

**Cenário**: o time quer garantir que nenhum commit com código Python mal formatado (ou com um erro de sintaxe óbvio) chegue ao repositório, sem depender de disciplina manual de cada pessoa lembrar de rodar o linter.

**Tarefa**: crie um hook `.git/hooks/pre-commit` (script shell) que rode uma checagem simples (ex: `python3 -m py_compile` em arquivos `.py` staged) e BLOQUEIE o commit se a checagem falhar.

**Verificação**: um commit com Python sintaticamente inválido deve ser rejeitado automaticamente pelo hook, antes de gerar o commit; um commit válido deve passar sem interferência.

---

## 5. Estratégia de branching para times de dados

**Cenário**: você é responsável por decidir a estratégia de branching de um time que versiona pipelines dbt e scripts de ingestão. Deploys em produção acontecem via CI/CD ao mergear na `main`.

**Tarefa** (conceitual, sem código — registre sua resposta em um arquivo `.md`):
1. Você recomendaria trunk-based development ou GitFlow pra esse time? Justifique considerando a frequência de deploy.
2. Como você trataria uma mudança de schema no dbt que precisa ser testada em um ambiente intermediário antes de ir pra produção — isso muda sua resposta acima?
3. Quem revisa um PR de mudança de modelagem dimensional antes do merge, e o que esse review deveria verificar (além de sintaxe)?

**Verificação**: sua resposta deve reconhecer o trade-off central — trunk-based favorece deploy contínuo e simplicidade, mas exige feature flags/testes robustos; GitFlow dá mais controle de "quando" algo vai pra produção, mas adiciona overhead de coordenação. Não existe resposta "certa" única — o que importa é justificar pro contexto dado.