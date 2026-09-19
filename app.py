import random

import streamlit as st

from times import (
    QUANTIDADES_PERMITIDAS, TAMANHO_TIME, interpretar_jogadores,
    sortear_times,
)


def gerar_sorteio(jogadores):
    st.session_state.times = sortear_times(jogadores)
    st.session_state.primeiro_jogo = random.sample(
        range(1, len(st.session_state.times) + 1), 2
    )


def enviar_lista(jogadores, origem):
    gerar_sorteio(jogadores)
    st.session_state.jogadores_enviados = jogadores
    # Novas chaves recriam os campos vazios, inclusive o anexo.
    st.session_state.versao_entrada = st.session_state.get("versao_entrada", 0) + 1
    st.session_state.entrada = (origem, "")


def sortear_novamente():
    gerar_sorteio(st.session_state.jogadores_enviados)


st.set_page_config(page_title="Sorteador de times", page_icon="⚽", layout="centered")
st.title("⚽ Sorteador de times")
st.write("Reúna 10, 15 ou 20 jogadores e sorteie times de cinco.")
st.caption("Peso 1: goleiro · Níveis 2 a 5: jogadores de linha, do menor ao maior nível.")

origem = st.radio("Como deseja adicionar os jogadores?", ["Colar nomes", "Anexar TXT"])
versao_entrada = st.session_state.get("versao_entrada", 0)
conteudo = ""
if origem == "Colar nomes":
    conteudo = st.text_area(
        "Nomes dos jogadores",
        key=f"nomes_{versao_entrada}",
        height=220,
        placeholder="Ana, 1\nBruno, 5\nCarlos, 3\n...",
        help="Use uma linha por jogador: Nome, peso. Uma vírgula no final da linha é opcional.",
    )
else:
    arquivo = st.file_uploader(
        "Selecione a lista de jogadores", type=["txt"], key=f"arquivo_{versao_entrada}"
    )
    st.caption("Arquivo UTF-8, com uma linha por jogador no formato Nome, peso.")
    if arquivo is not None:
        try:
            conteudo = arquivo.getvalue().decode("utf-8-sig")
        except UnicodeDecodeError:
            st.error("Não foi possível ler o arquivo. Salve o TXT em UTF-8 e tente novamente.")

try:
    jogadores = interpretar_jogadores(conteudo)
except ValueError as erro:
    st.error(str(erro))
    jogadores = []
assinatura = (origem, conteudo)
if st.session_state.get("entrada") != assinatura:
    st.session_state.entrada = assinatura
    st.session_state.pop("times", None)
    st.session_state.pop("primeiro_jogo", None)
    st.session_state.pop("jogadores_enviados", None)

quantidade = len(jogadores)
valido = quantidade in QUANTIDADES_PERMITIDAS
st.caption(f"{quantidade} jogadores adicionados")
if quantidade and not valido:
    st.warning("A lista precisa conter 10, 15 ou 20 jogadores para formar times de cinco.")
if valido:
    goleiros = sum(jogador.goleiro for jogador in jogadores)
    quantidade_times = quantidade // TAMANHO_TIME
    if goleiros < quantidade_times:
        st.warning(f"Há {goleiros} goleiro(s) para {quantidade_times} times. Alguns times ficarão sem goleiro cadastrado.")
    elif goleiros > quantidade_times:
        st.warning(f"Há {goleiros} goleiros para {quantidade_times} times. Alguns times terão mais de um goleiro.")

st.button(
    "Sortear times", type="primary", disabled=not valido,
    on_click=enviar_lista, args=(jogadores, origem),
)

if "times" in st.session_state:
    st.divider()
    if "primeiro_jogo" in st.session_state:
        primeiro, segundo = st.session_state.primeiro_jogo
        st.subheader("Primeiro jogo")
        st.success(f"Time {primeiro} × Time {segundo}")
    st.subheader("Times sorteados")
    for numero, time in enumerate(st.session_state.times, start=1):
        with st.container(border=True):
            st.subheader(f"Time {numero}")
            st.text("\n".join(
                f"{jogador.nome} (Goleiro)" if jogador.goleiro else jogador.nome
                for jogador in time
            ))
    st.button("Sortear novamente", on_click=sortear_novamente)
