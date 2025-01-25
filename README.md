# PD Hours API
Esta API desenvolvida para gerenciar um sistema de controle de horas trabalhadas. Ela permite o cadastro de funcionários, squads e relatórios, além de realizar consultas relacionadas as horas gastas. 

## Tecnologias utilizadas
- Python: Linguagem utilizada para o desenvolvimento da aplicação.
- FastAPI: Framework para criação de APIs assíncronas e rápidas.
- Uvicorn: Servidor ASGI para rodar a aplicação FastAPI.
- Dockerfile e Docker-compose: Utilizados para containerização e fácil configuração do ambiente de desenvolvimento.
- Pytest: Framework para a realização de testes
- Unittest.mock: Framework utilizado para realizar mocks

## Como executar o projeto
1. Clone o repositório:
    ```
    https://github.com/FerNagata/PD-Hours-API.git
    ```

2. Executando com Docker Compose:

    1. **Certifique-se de ter o Docker e Docker Compose instalados:**

        [Instruções para instalar o Docker](https://docs.docker.com/get-docker/)

        [Instruções para instalar o Docker Compose](https://docs.docker.com/compose/install/)

    2. **Construa e execute os contêineres:**

        Navegue até o diretório `api` (onde está localizado o arquivo `docker-compose.yml`) e execute:
        ```
        docker-compose up --build
        ```

        O comando acima irá construir a imagem Docker e iniciar os contêineres.

    3. **Acesse a API**:

        Após a execução, a API estará disponível em: http://localhost:8000.

### Testando a API

- Após a execução, você pode acessar a documentação interativa da API fornecida pelo **Swagger** diretamente pelo navegador no seguinte endereço:
[http://localhost:8000/docs](http://localhost:8000/docs)

    Essa interface permite que você visualize e teste todos os endpoints expostos pela API.

- Caso queira executar os testes automatizados, certifique-se de ter o pytest, caso não tenha execute o seguinte comando:
    ```
    pip install pytest
    ```

    Após isso, execute o comando abaixo no terminal para rodar os testes:
    ```
    pytest
    ```

- Este repositório também possui um artefato com o relatório dos testes realizados, que está disponível através do GitHub Actions.

---
### Padrões de Commit

Este repositório segue uma convenção de commits para manter um histórico claro e consistente. Abaixo está uma tabela com os tipos de commits e suas descrições.

| Tipo de Commit | Descrição |
| -------------- | --------- |
| `feat`         | Adição de uma nova funcionalidade |
| `fix`          | Correção de um bug |
| `docs`         | Mudanças na documentação |
| `style`        | Alterações que não afetam o significado do código (espaços em branco, formatação, ponto e vírgula ausente, etc.) |
| `refactor`     | Refatoração de código, que não altera a funcionalidade nem corrige bugs |
| `perf`         | Alterações de código que melhoram o desempenho |
| `test`         | Adição ou correção de testes |
| `build`        | Mudanças que afetam o sistema de build ou dependências externas (ferramentas de compilação, bibliotecas, etc.) |
| `ci`           | Mudanças em arquivos e scripts de configuração de CI (Integração Contínua) |
| `chore`        | Outras mudanças que não modificam o código fonte ou os testes |
| `revert`       | Reversão de um commit anterior |
| `merge`        | Mesclagem de branches |
| `hotfix`       | Correção urgente de um bug crítico |
