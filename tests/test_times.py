import random
import unittest
from collections import Counter
from unittest.mock import patch

from times import Jogador, interpretar_jogadores, pontuacao_time, sortear_times


class SorteioTests(unittest.TestCase):
    def test_leitura_do_formato_com_espacos_bom_e_virgula_final(self):
        self.assertEqual(
            interpretar_jogadores('\ufeff1 - Ana, 1,\r\n\nBruno , 5 \nCarlos, 3,'),
            [Jogador('Ana', 1), Jogador('Bruno', 5), Jogador('Carlos', 3)],
        )

    def test_entrada_invalida_informa_linha(self):
        for linha in ('Ana', 'Ana, 0', 'Ana, 6', 'Ana, 2.5', ', 3', 'Ana, 3, extra'):
            with self.subTest(linha=linha):
                with self.assertRaisesRegex(ValueError, 'Linha 2'):
                    interpretar_jogadores('João, 1\n' + linha)

    def test_tamanho_preservacao_e_distribuicao_dos_goleiros(self):
        rng = random.Random(42)
        with patch('times.TENTATIVAS_SORTEIO', 5):
            for quantidade in (10, 15, 20):
                for goleiros in (0, 1, quantidade // 5, quantidade // 5 + 1, quantidade):
                    jogadores = [Jogador(str(i), 1 if i < goleiros else rng.randint(2, 5)) for i in range(quantidade)]
                    original = jogadores.copy()
                    times = sortear_times(jogadores)
                    self.assertTrue(all(len(time) == 5 for time in times))
                    self.assertEqual(Counter(j for time in times for j in time), Counter(original))
                    self.assertEqual(jogadores, original)
                    contagens = [sum(j.goleiro for j in time) for time in times]
                    self.assertLessEqual(max(contagens) - min(contagens), 1)

    def test_equilibrio_em_caso_com_solucao_exata(self):
        jogadores = [Jogador(str(i), peso) for i, peso in enumerate([1, 2, 3, 4, 5] * 4)]
        times = sortear_times(jogadores)
        self.assertEqual([pontuacao_time(time) for time in times], [14] * 4)

    def test_quantidade_invalida(self):
        with self.assertRaises(ValueError):
            sortear_times([Jogador('Ana', 3)])


if __name__ == '__main__':
    unittest.main()
