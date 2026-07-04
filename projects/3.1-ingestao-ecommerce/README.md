# 3.1 - Ingestão Batch (E-commerce)

**Camada:** 3 - Pipelines
**Consome:** nada (ponto de entrada da trilha)
**Produz:** dados brutos em `bronze/vendas/` e `bronze/eventos/` no MinIO

## Como rodar
\`\`\`bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python src/generate_data.py
python src/upload_to_minio.py
\`\`\`

## Status
- [x] Geração de dados fictícios
- [ ] Upload pro MinIO