import random
import re
from dataclasses import dataclass
from pathlib import Path

TAMANHO_TIME = 5
QUANTIDADES_PERMITIDAS = (10, 15, 20)
TENTATIVAS_SORTEIO = 100


@dataclass(frozen=True)
class Jogador:
    nome: str
    peso: int

    @property
    def goleiro(self):
        return self.peso == 1

    @property
    def pontos(self):
        return 0 if self.goleiro else self.peso

    def __str__(self):
        nivel = "Goleiro" if self.goleiro else f"Nível {self.peso}"
        return f"{self.nome} — {nivel}"


def interpretar_jogadores(conteudo):
    """Lê uma linha 'Nome, peso', permitindo uma vírgula final e numeração."""
    jogadores = []
    for numero, linha in enumerate(conteudo.lstrip("\ufeff").splitlines(), start=1):
        if not linha.strip():
            continue
        campos = linha.strip().removesuffix(",").split(",")
        if len(campos) != 2:
            raise ValueError(f"Linha {numero}: use Nome, peso (exemplo: Ana, 4).")
        nome = re.sub(r"^\d+\s*-\s*", "", campos[0].strip()).strip()
        peso = campos[1].strip()
        if not nome or peso not in {"1", "2", "3", "4", "5"}:
            raise ValueError(f"Linha {numero}: informe um nome e um peso inteiro de 1 a 5.")
        jogadores.append(Jogador(nome, int(peso)))
    return jogadores


def pontuacao_time(time):
    return sum(jogador.pontos for jogador in time)


def _qualidade(times):
    pontos = [pontuacao_time(time) for time in times]
    return max(pontos) - min(pontos), sum(ponto ** 2 for ponto in pontos)


def _melhorar_times(times):
    """Troca jogadores da mesma posição enquanto houver melhoria estrita."""
    while True:
        melhor = _qualidade(times)
        troca = None
        for a in range(len(times)):
            for b in range(a + 1, len(times)):
                for i, jogador_a in enumerate(times[a]):
                    for j, jogador_b in enumerate(times[b]):
                        if jogador_a.goleiro != jogador_b.goleiro:
                            continue
                        times[a][i], times[b][j] = jogador_b, jogador_a
                        qualidade = _qualidade(times)
                        times[a][i], times[b][j] = jogador_a, jogador_b
                        if qualidade < melhor:
                            melhor = qualidade
                            troca = (a, b, i, j)
        if troca is None:
            return
        a, b, i, j = troca
        times[a][i], times[b][j] = times[b][j], times[a][i]


def sortear_times(jogadores):
    """Busca times equilibrados, mantendo cinco pessoas e goleiros distribuídos."""
    if len(jogadores) not in QUANTIDADES_PERMITIDAS:
        raise ValueError("É necessário informar 10, 15 ou 20 jogadores.")
    if any(jogador.peso not in range(1, 6) for jogador in jogadores):
        raise ValueError("Os pesos devem estar entre 1 e 5.")

    quantidade_times = len(jogadores) // TAMANHO_TIME
    goleiros = [jogador for jogador in jogadores if jogador.goleiro]
    linha = [jogador for jogador in jogadores if not jogador.goleiro]
    melhor_resultado = None
    for _ in range(TENTATIVAS_SORTEIO):
        times = [[] for _ in range(quantidade_times)]
        random.shuffle(goleiros)
        random.shuffle(linha)
        for indice, goleiro in enumerate(goleiros):
            times[indice % quantidade_times].append(goleiro)
        for jogador in linha:
            disponiveis = [time for time in times if len(time) < TAMANHO_TIME]
            menor_pontuacao = min(map(pontuacao_time, disponiveis))
            candidatos = [time for time in disponiveis if pontuacao_time(time) == menor_pontuacao]
            random.choice(candidatos).append(jogador)
        _melhorar_times(times)
        if melhor_resultado is None or _qualidade(times) < _qualidade(melhor_resultado):
            melhor_resultado = times
        # Uma diferença de zero ou um é o mínimo possível para somas inteiras.
        if _qualidade(melhor_resultado)[0] <= 1:
            break
    random.shuffle(melhor_resultado)
    return melhor_resultado


def main():
    caminho = Path(__file__).resolve().with_name("jogadores.txt")
    try:
        jogadores = interpretar_jogadores(caminho.read_text(encoding="utf-8-sig"))
        if len(jogadores) not in QUANTIDADES_PERMITIDAS:
            raise ValueError("É necessário informar 10, 15 ou 20 jogadores.")
    except (OSError, UnicodeError, ValueError) as erro:
        print(f"Não foi possível carregar os jogadores: {erro}")
        return

    quantidade_times = len(jogadores) // TAMANHO_TIME
    goleiros = sum(jogador.goleiro for jogador in jogadores)
    if goleiros != quantidade_times:
        print(f"Atenção: {goleiros} goleiro(s) para {quantidade_times} times. Serão distribuídos igualmente quando possível.")
    if input("Deseja sortear os times? (s/n): ").strip().lower() != "s":
        print("Sorteio cancelado.")
        return
    for numero, time in enumerate(sortear_times(jogadores), start=1):
        print(f"Time {numero} ({pontuacao_time(time)} pontos):")
        for jogador in time:
            print(f"  {jogador}")
    print("Jogo inicial",)

if __name__ == "__main__":
    main()
