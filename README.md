# Sorteador de times

Tela simples em Streamlit para sortear 10, 15 ou 20 jogadores em times de cinco.
Cole a lista ou envie um arquivo `.txt` em UTF-8. Use uma linha por jogador:

```text
Ana, 1
Bruno, 5,
Carlos, 3
```

O peso 1 indica goleiro. Os pesos 2 a 5 indicam habilidade dos jogadores de
linha, sendo 5 o maior nível. A vírgula final e a numeração `1 - Nome` são
opcionais. Linhas incompletas ou pesos inválidos impedem o sorteio e mostram
o número da linha a corrigir.

Cada time tem cinco pessoas, incluindo goleiros. Os goleiros são distribuídos
com diferença de no máximo um entre times. Se não houver exatamente um por
time, a tela avisa, mas permite sortear sem inventar goleiros.

O equilíbrio considera a soma dos níveis dos jogadores de linha; o marcador
de goleiro não soma pontos de habilidade. O sorteio experimenta até 100
distribuições aleatórias e melhora cada uma trocando jogadores de linha.
Prioriza a menor diferença entre o maior e o menor total, depois a menor
dispersão. É uma busca aproximada, sem garantia de ótimo global. Com quantidades
desiguais de goleiros, os times terão quantidades diferentes de jogadores de
linha; a comparação continua sendo pela soma, não pela média.

## Executar localmente

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python -m streamlit run app.py
```

Abra o endereço informado no terminal. O resultado permanece durante a sessão;
após um sorteio válido, o campo de nomes ou anexo é limpo. O botão **Sortear
novamente** reutiliza a lista enviada, mantida apenas na sessão. Inserir uma
nova lista remove o sorteio anterior. Os nomes enviados pela tela não são
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
