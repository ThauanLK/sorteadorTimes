import streamlit as st

from times import QUANTIDADES_PERMITIDAS, interpretar_jogadores, sortear_times


st.set_page_config(page_title="Sorteador de times", page_icon="⚽", layout="centered")
st.title("⚽ Sorteador de times")
st.write("Reúna 10, 15 ou 20 jogadores e sorteie times de cinco.")

origem = st.radio("Como deseja adicionar os jogadores?", ["Colar nomes", "Anexar TXT"])
conteudo = ""
if origem == "Colar nomes":
    conteudo = st.text_area(
        "Nomes dos jogadores",
        height=220,
        placeholder="Ana\nBruno\nCarlos\n...",
        help="Use um nome por linha ou separe por vírgulas. Listas numeradas como '1 - Ana' também funcionam.",
    )
else:
    arquivo = st.file_uploader("Selecione a lista de jogadores", type=["txt"])
    st.caption("Arquivo UTF-8, com um nome por linha ou nomes separados por vírgulas.")
    if arquivo is not None:
        try:
            conteudo = arquivo.getvalue().decode("utf-8-sig")
        except UnicodeDecodeError:
            st.error("Não foi possível ler o arquivo. Salve o TXT em UTF-8 e tente novamente.")

jogadores = interpretar_jogadores(conteudo)
assinatura = (origem, tuple(jogadores))
if st.session_state.get("entrada") != assinatura:
    st.session_state.entrada = assinatura
    st.session_state.pop("times", None)

quantidade = len(jogadores)
valido = quantidade in QUANTIDADES_PERMITIDAS
st.caption(f"{quantidade} jogadores adicionados")
if quantidade and not valido:
    st.warning("A lista precisa conter 10, 15 ou 20 jogadores para formar times de cinco.")

if st.button("Sortear times", type="primary", disabled=not valido):
    st.session_state.times = sortear_times(jogadores)

if "times" in st.session_state:
    st.divider()
    st.subheader("Times sorteados")
    for numero, time in enumerate(st.session_state.times, start=1):
        with st.container(border=True):
            st.subheader(f"Time {numero}")
            st.text("\n".join(time))
    st.caption("Para fazer um novo sorteio, toque em Sortear times novamente.")
