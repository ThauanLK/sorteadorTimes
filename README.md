# Sorteador de times

Tela simples em Streamlit para sortear 10, 15 ou 20 jogadores em times de cinco.
Cole os nomes ou envie um arquivo `.txt` em UTF-8. Use um nome por linha ou
nomes separados por vírgulas. A numeração no formato `1 - Nome` é opcional.

## Executar localmente

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python -m streamlit run app.py
```

Abra o endereço informado no terminal. O resultado permanece durante a sessão;
alterar a lista remove o sorteio anterior. Os nomes enviados pela tela não são
gravados em arquivo pela aplicação.

## Publicar por link

1. Envie `app.py`, `times.py` e `requirements.txt` para seu repositório no GitHub.
2. Acesse https://share.streamlit.io/ e conecte sua conta do GitHub.
3. Escolha **Create app**, selecione o repositório e a branch.
4. Informe `app.py` como arquivo principal e clique em **Deploy**.
5. Abra e compartilhe o link gerado, inclusive no celular.

O arquivo local `jogadores.txt` não é necessário para a versão web.

Documentação: https://docs.streamlit.io/deploy/streamlit-community-cloud/deploy-your-app

## Executar no terminal

```bash
python3 times.py
```

Essa opção lê `jogadores.txt` na mesma pasta de `times.py`.
