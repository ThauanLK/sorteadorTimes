entradaJogador = input("Digite a lista de jogadores (separados por vírgula): ")
vetor = entradaJogador.split(",")

if len(vetor) < 2:
    print("É necessário informar pelo menos dois jogadores.")
if len(vetor) == 10:
    sortear = input("Deseja sortear os times? (s/n): ")
if sortear.lower() == "s":
    import random
    random.shuffle(vetor)
    time1 = vetor[:5]
    time2 = vetor[5:]
    print("Time 1:", time1)
    print("Time 2:", time2)
if len(vetor) == 15:
    sortear = input("Deseja sortear os times? (s/n): ") 
    import random
    random.shuffle(vetor)
    time1 = vetor[:5]
    time2 = vetor[5:]
    time3 = vetor[10:]
    print("Time 1:", time1)
    print("Time 2:", time2)
    print("Time 3:", time3)
if len(vetor) == 20:
    sortear = input("Deseja sortear os times? (s/n): ")
    import random
    random.shuffle(vetor)
    time1 = vetor[:5]
    time2 = vetor[5:10]
    time3 = vetor[10:15]
    time4 = vetor[15:]
    print("Time 1:", time1)
    print("Time 2:", time2)
    print("Time 3:", time3)
    print("Time 4:", time4)