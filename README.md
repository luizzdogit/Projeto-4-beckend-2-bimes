# Painel de Cotações - Projeto 4

Painel Django que consulta a cotação USD/BRL na AwesomeAPI, guarda o histórico
no banco de dados e o exibe com `fetch()`.

## Funcionalidades

- `/consultar/` consulta a cotação e salva um registro quando a API responde
  corretamente.
- Tratamento de falhas de rede e de respostas inesperadas da API.
- `/api/historico/` retorna os registros em JSON, do mais recente para o mais
  antigo.
- Admin Django para consultar os registros de cotação.

## Como rodar

No PowerShell, a partir da pasta do projeto:

```powershell
python -m venv venv
.\venv\Scripts\python.exe -m pip install -r requirements.txt
.\venv\Scripts\python.exe manage.py migrate
.\venv\Scripts\python.exe manage.py runserver
```

Abra <http://127.0.0.1:8000/consultar/>. Para acessar o Admin, crie um
superusuário com `.\venv\Scripts\python.exe manage.py createsuperuser` e abra
<http://127.0.0.1:8000/admin/>.

## Variável de ambiente (opcional)

`COTACAO_URL` permite substituir a URL da API externa. Sem essa variável, o
projeto usa `https://economia.awesomeapi.com.br/json/last/USD-BRL`.

Exemplo temporário no PowerShell:

```powershell
$env:COTACAO_URL = "https://economia.awesomeapi.com.br/json/last/USD-BRL"
.\venv\Scripts\python.exe manage.py runserver
```

## Prints

Adicione capturas de tela do painel e da listagem de registros no Admin:

- `docs/prints/painel.png`
- `docs/prints/admin-registros.png`

Quando os arquivos estiverem disponíveis, inclua-os aqui:

```markdown
![Painel de Cotações](docs/prints/painel.png)
![Registros no Admin](docs/prints/admin-registros.png)
```

## Autor

`<Luiz Enrique Carrilho> - IESB 2026`
