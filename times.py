import random
import re
from pathlib import Path

TAMANHO_TIME = 5
QUANTIDADES_PERMITIDAS = (10, 15, 20)


def interpretar_jogadores(conteudo):
    """Aceita nomes por linha ou vírgula, com prefixos como '1 - Nome'."""
    jogadores = []
    for item in re.split(r"[\r\n,]+", conteudo.lstrip("\ufeff")):
        nome = re.sub(r"^\d+\s*-\s*", "", item.strip()).strip()
        if nome:
            jogadores.append(nome)
    return jogadores


def sortear_times(jogadores):
    if len(jogadores) not in QUANTIDADES_PERMITIDAS:
        raise ValueError("É necessário informar 10, 15 ou 20 jogadores.")

    embaralhados = jogadores.copy()
    random.shuffle(embaralhados)

    return [
        embaralhados[inicio:inicio + TAMANHO_TIME]
        for inicio in range(0, len(embaralhados), TAMANHO_TIME)
    ]


def main():
    caminho = Path(__file__).resolve().with_name("jogadores.txt")
    try:
        jogadores = interpretar_jogadores(caminho.read_text(encoding="utf-8-sig"))
    except (OSError, UnicodeError) as erro:
        print(f"Não foi possível ler jogadores.txt: {erro}")
        return

    if len(jogadores) not in QUANTIDADES_PERMITIDAS:
        print("É necessário informar 10, 15 ou 20 jogadores.")
        return

    resposta = input("Deseja sortear os times? (s/n): ").strip().lower()
    if resposta != "s":
        print("Sorteio cancelado.")
        return

    for numero, time in enumerate(sortear_times(jogadores), start=1):
        print(f"Time {numero}: {', '.join(time)}")


if __name__ == "__main__":
    main()
