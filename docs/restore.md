# Restore

`scripts/restore.sh <timestamp>` restaura Postgres (todos os bancos), MongoDB, MinIO e Dremio a partir de um backup gerado por `backup.sh`.

## Uso

```bash
./scripts/restore.sh 20260704_002021
```

Sem argumento, o script lista os backups disponíveis em `backups/`.

## O que acontece

1. Pede confirmação explícita (`sim`) antes de sobrescrever qualquer dado
2. Restaura papéis/permissões globais primeiro (`postgres/_globals.sql`)
3. Para cada banco encontrado em `postgres/*.sql`:
   - Se for o banco `postgres` (manutenção padrão): restaura por cima, sem dropar
   - Para qualquer outro banco: encerra conexões ativas, **dropa o banco e recria do zero**, depois restaura o dump - garante estado idêntico ao backup, sem risco de dados duplicados ou resíduos de execuções anteriores
4. Restaura o dump do MongoDB via `mongorestore --drop`
5. Para o container do MinIO, substitui o conteúdo do volume, reinicia
6. Faz o mesmo para o Dremio

## Compatibilidade com backups antigos

Backups gerados antes desta atualização (formato `postgres_<db>.sql` na raiz, um banco só) **não são compatíveis** com esta versão do `restore.sh`. O script detecta isso e avisa em vez de falhar de forma confusa - rode um novo `./scripts/backup.sh` antes de restaurar, se cair nesse caso.

## Cuidados

- Restore **sobrescreve** os dados atuais dos serviços afetados - não é incremental
- Bancos do Postgres (exceto `postgres`) são **dropados e recriados**, então qualquer dado criado depois do backup e não incluído nele será perdido nesse banco
- Sempre rode `./scripts/backup.sh` antes de um restore, caso precise reverter
- Dremio pode precisar reconfigurar as fontes de dados dependendo da versão restaurada