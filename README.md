# ia-vibecode-agente-mudanca

Este projeto demonstra como carregar perfis de cidades a partir de um arquivo CSV e, agora, como expor esses dados como uma tool simples do LangChain que utiliza os modelos da OpenAI.

## Configuração do ambiente Python

1. Crie e ative um ambiente virtual (requer Python 3.10 ou superior):

   ```bash
   python -m venv .venv
   source .venv/bin/activate
   ```

2. Instale as dependências:

   ```bash
   pip install -r requirements.txt
   ```

3. Copie o arquivo de exemplo `.env.example` para `.env` e edite-o informando sua chave da OpenAI:

   ```bash
   cp .env.example .env
   # edite o arquivo .env e substitua pelo valor da sua chave
   ```

   > O script `run_langchain_agent.py` carregará automaticamente o arquivo `.env`
   > (via `python-dotenv`) antes de inicializar o modelo da OpenAI.

## Executando o agente LangChain

Após configurar o ambiente, execute o agente que utiliza a tool `listar_perfis_cidades`:

```bash
python run_langchain_agent.py
```

O agente utiliza o modelo `gpt-3.5-turbo` (via `ChatOpenAI`) para responder perguntas e, quando necessário, consulta a tool para obter a lista de cidades disponíveis.
