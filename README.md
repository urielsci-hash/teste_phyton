# Painel de Qualidade — Sinergia Agro (Versão Python/Flask)

Painel de gestão à vista digital para a fábrica de Serra Negra/SP. Originalmente construído em PHP, esta versão foi reescrita inteiramente em **Python (Flask)**.

## Permissões por departamento

- **Qualidade**: Status da qualidade (pirâmide + desvios), Indicadores, Em formulação.
- **RH / Marketing**: Mural (imagens ou texto), Notícias RSS.
- **TI**: Usuários (criar, editar, redefinir senha, desativar, excluir) e o Log de auditoria. Não acessa nenhum conteúdo/arquivo das outras áreas.
- **Visualização**: só vê a tela pública — use para a Smart TV e para acesso remoto da diretoria. Sem acesso a nenhuma página de admin.

Qualquer usuário logado também pode abrir a tela pública normalmente, como pré-visualização.
Todo usuário cadastrado pelo TI na tela de Usuários recebe uma senha inicial e é obrigado a trocá-la no primeiro acesso.

## Configuração do Ambiente e Testes (GitHub Codespaces / Local)

O sistema suporta nativamente o banco de dados **SQLite** para testes rápidos (sem precisar configurar MySQL na máquina) e MySQL para produção.

### Rodando o projeto localmente:
1. Instale as dependências executando:
   `pip install -r requirements.txt`
2. Crie ou inicie o banco de dados de teste rodando o script:
   `python init_db.py`
3. Inicie o servidor Flask:
   `python app.py` ou `flask run`
4. Acesse pelo navegador em `http://127.0.0.1:5000`.

### Senhas e primeiro uso:
Como o banco vem vazio, você deve inserir manualmente os primeiros departamentos e um usuário de TI:
1. Abra a rota `http://127.0.0.1:5000/gerar-senha`.
2. Gere um hash para a sua senha desejada.
3. Insira diretamente no banco de dados (por script ou extensão SQLite). (A tabela de `departamentos` tem ID 4 para TI).

## Colocando no Ar (Locaweb / cPanel)

1. Para rodar em produção, seu plano de hospedagem deve oferecer a função **"Setup Python App"**.
2. No ambiente de produção, crie um arquivo `.env` na raiz contendo os dados do MySQL:
```
USE_SQLITE=False
DB_HOST=localhost
DB_NAME=uriel_sinergia
DB_USER=uriel_sinergia
DB_PASS=SuaSenhaAqui
SECRET_KEY=sua_chave_secreta_flask
```
3. O `database.py` reconhecerá a chave `USE_SQLITE=False` e automaticamente passará a utilizar a conexão PyMySQL para o banco da Locaweb.
4. Envie a estrutura via FTP/Git.

## Segurança e Padrões

- Senhas com hash `werkzeug.security` (`generate_password_hash` / `check_password_hash`).
- Templates baseados em **Jinja2**, protegidos contra injeções.
- Queries utilizam *parameterized statements* para evitar SQL Injection.
- Exclusão de usuário é bloqueada quando há histórico associado (preserva rastreabilidade).
- Log de auditoria limpo automaticamente após 30 dias.
