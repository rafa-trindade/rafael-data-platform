# Segurança - Firewall e Acesso a Bancos de Dados

## Contexto: por que isso foi necessário

Durante os testes iniciais, os logs do Postgres e do MongoDB mostraram tentativas ativas de invasão vindas da internet pública - scanners automatizados testando usuários comuns de apps conhecidos (`outline`, `n8n`, `django`, `supabase_admin`, `airflow`, `strapi`, `odoo`, `kong`, `gogs`, `kestra`, etc) contra o Postgres, e conexões externas reais tentando autenticar no MongoDB.

## Tentativas que não resolveram (histórico, para não repetir o erro)

1. **UFW sozinho** (`ufw deny 5434/tcp` etc): não bloqueou o tráfego. O Docker manipula tabelas do iptables (`nat`/`filter`) de um jeito que não é filtrado pelas regras padrão do UFW na chain `INPUT` - o tráfego pra portas publicadas pelo Docker passa por outro caminho.
2. **Regras diretas na chain `DOCKER-USER`** (allow por IP + deny geral): é a abordagem tecnicamente recomendada pela documentação do Docker para esse cenário, mas na prática, testando com o ataque real acontecendo, **o tráfego continuou passando**. Provavelmente inconsistência de versão de Docker/kernel com a ordem de avaliação das chains nesse ambiente específico.

Conclusão: tentar filtrar tráfego que já chega até a interface pública, depois que o Docker já publicou a porta, é uma abordagem frágil nesse ambiente. A solução adotada elimina o problema pela raiz.

## Solução adotada: bind em loopback + túnel SSH

Em vez de publicar Postgres, MongoDB e Redis em `0.0.0.0` (qualquer IP) e tentar filtrar quem entra, esses serviços são publicados **apenas em `127.0.0.1`** (loopback do próprio host da VPS). Isso torna as portas **inacessíveis pela rede externa**, independente de qualquer configuração de iptables/UFW - não é uma regra que pode falhar, é uma ausência física de rota.

No `docker/docker-compose.yml`:

```yaml
postgres:
  ports:
    - "127.0.0.1:5434:5432"

mongodb:
  ports:
    - "127.0.0.1:27017:27017"

redis:
  ports:
    - "127.0.0.1:6379:6379"
```

## Como acessar do seu computador: túnel SSH

Como as portas só existem no `localhost` da VPS, o acesso remoto é feito via túnel SSH, que encaminha as portas locais da VPS para o seu computador de forma criptografada:

```bash
ssh -L 5434:localhost:5434 -L 27017:localhost:27017 -L 6379:localhost:6379 rafael@_ip_
```

Enquanto esse terminal SSH permanecer aberto, conecte suas ferramentas (pgAdmin, DBeaver, MongoDB Compass, RedisInsight local, etc) apontando para `localhost:5434`, `localhost:27017`, `localhost:6379` - **não mais para o IP público da VPS**.

Se preferir não deixar um terminal ocupado, é possível abrir o túnel em background:

```bashg
ssh -f -N -L 5434:localhost:5434 -L 27017:localhost:27017 -L 6379:localhost:6379 rafael@_ip_
```

Para fechar depois:

```bash
pkill -f "5434:localhost:5434"
```

## Portas que continuam públicas (UIs web)

Essas continuam liberadas geral via UFW, pois são acessadas do navegador em locais variados:

```bash
sudo ufw allow 9001/tcp   # MinIO console
sudo ufw allow 9047/tcp   # Dremio UI
sudo ufw allow 8081/tcp   # Mongo Express
sudo ufw allow 5540/tcp   # RedisInsight
sudo ufw allow 9443/tcp   # Portainer
sudo ufw allow 5050/tcp   # pgAdmin
```
