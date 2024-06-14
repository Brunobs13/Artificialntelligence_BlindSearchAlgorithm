#Bruno Ricardo de Sa Ferreira 
#Efolio A - Ano 2024 
#Introducao a IA 
#Professor Jose Coelho 
#Numero de estudante 2201529
#Data de entrega: 15 de Abril de 2024

#!/usr/bin/env python3
from collections import deque
import time

verbas = {
	4: {
		1: ([(1,1)], [1])  
	},
	8: {
		1: ([(1,1),(1,5) ], [1,1]),
		2: ([(2,4)], [2])
	},
	12: {
		1: ([(2,2),(6,6)], [2,2]),
		2: ([(1,1),(1,7),(7,1)], [1,1,1]),
		3: ([(4,3)], [3])
	},
	16: {
		1: ([(1,1),(1,9),(9,1),(9,9)], [1,1,1,1]),
		2: ([(3,3),(8,8)], [3,2]),
		3: ([(2,2),(2,8),(8,8)], [2,2,2])
	},
	20: {
		1: ([(1,1),(1,11),(6,6),(11,1),(11,11)], [1,1,1,1,1]),
		2: ([(4,4)], [4]),
		3: ([(3,3),(9,9)], [3,3]),
		4: ([(2,2),(2,10),(10,2),(10,10)], [2,2,2,2]),
		5: ([(3,3),(10,2),(2,10)], [3,2,2])
	}
}


territorio = {
	1: {
		'matriz': [[0,7,0,0,4], [0,0,0,4,0], [1,0,0,0,0], [4,4,1,0,0], [6,0,3,4,4]],
		'verba': 4,
		'objetivo': [19, 20],
		
	},
	2: {
		'matriz': [[4,0,0,10,1], [1,0,0,0,0], [0,0,1,6,3], [0,4,0,0,2], [8,0,6,3,0]],
		'verba': 4,
		'objetivo': [21, 22]
	},
	3: {
		'matriz': [[0,8,0,4,5,10,0], [0,4,0,7,0,4,0], [0,2,4,2,0,0,2], [0,7,0,1,2,0,0], [2,4,0,0,3,0,2], [0,4,0,0,3,0,0], [2,0,0,0,0,0,0]],
		'verba': 8,
		'objetivo': [67, 68]
		},
	4: {
		'matriz': [[0,0,1,0,7,0,1], [0,1,4,0,0,0,4], [0,0,0,0,2,0,0], [3,1,0,8,5,7,7], [0,4,0,3,0,0,0], [0,0,0,3,2,4,2], [0,8,3,6,3,0,0]],
		'verba': 8,
		'objetivo': [59, 60]
		},
	5: {
		'matriz': [[6,7,2,0,0,0,0,0,0], [3,3,6,0,8,4,3,1,0], [0,0,8,0,0,0,2,4,0], [0,0,0,1,0,3,2,0,0], [0,0,0,7,4,0,1,0,0], [12,8,0,5,4,1,4,3,4], [8,0,1,2,4,3,3,0,0], [1,1,0,0,0,0,5,0,0], [4,0,0,0,4,6,0,13,2]],
		'verba': 12,
		'objetivo': [125, 126]
		},
	6: {
		'matriz': [[0,0,0,0,0,0,0,0,0], [4,0,8,4,0,0,0,0,0], [0,0,0,0,0,0,0,0,0], [0,0,0,0,3,0,0,1,0], [0,3,0,0,0,0,0,0,0], [0,0,0,1,1,0,0,3,0], [0,0,2,4,0,0,0,1,0], [0,2,0,0,8,0,4,3,10], [0,0,3,0,0,4,0,0,0]],
		'verba': 12,
		'objetivo': [57, 58]
		},
	7: {
		'matriz': [[0,0,0,0,0,3,0,0,0,0,0], [0,0,11,2,0,0,9,3,0,0,3], [0,0,0,3,1,0,2,0,0,0,0], [4,1,2,3,0,4,0,0,4,0,0], [5,0,0,0,4,0,1,0,4,3,0], [0,0,0,7,4,0,1,0,0,7,0], [0,8,0,0,0,0,3,0,1,0,3], [0,3,0,0,5,2,3,0,0,0,2], [0,0,0,3,1,0,2,8,0,0,0], [0,3,4,0,7,0,0,7,0,0,0], [4,2,0,4,0,3,0,0,5,7,0]],
		'verba': 16,
		'objetivo': [140, 141]
		},
	8: {
		'matriz': [[1,0,0,0,0,0,0,0,0,0,0], [0,0,0,0,0,0,0,0,0,0,0], [0,0,10,10,0,0,0,4,5,0,0], [0,4,1,0,8,0,0,0,0,0,5], [8,0,0,0,0,0,6,0,0,0,0], [0,0,0,0,13,0,0,0,2,0,3], [0,0,0,0,4,0,0,0,0,1,0], [0,0,0,0,0,0,0,0,0,0,0], [0,0,4,0,0,0,0,3,0,0,0], [4,1,0,0,0,0,0,0,0,0,0], [0,0,0,0,0,0,0,0,0,0,0]],
		'verba': 16,
		'objetivo': [93, 94]
		},
	9: {
		'matriz': [[2,4,0,0,6,7,3,4,0,0,3,0,1], [0,0,2,0,3,0,0,6,0,0,8,11,3], [0,3,0,8,0,0,2,0,0,0,0,0,4], [2,0,0,0,0,0,0,0,0,3,2,0,0], [0,6,0,8,0,3,0,0,0,0,0,0,1], [0,3,0,2,0,0,9,0,0,0,0,5,6], [1,9,4,0,0,2,4,0,0,0,3,2,0], [2,3,0,4,0,0,0,6,2,0,1,0,3], [0,0,0,0,0,6,0,0,0,2,2,0,8], [7,2,4,2,0,0,6,4,1,0,0,0,7], [0,0,0,11,0,0,0,0,3,4,0,9,0], [0,0,0,0,1,4,3,4,0,0,0,3,11], [0,0,4,7,7,0,0,2,0,2,5,0,1]],
		'verba': 20,
		'objetivo': [211, 212]
		},
		10: {
		'matriz': [[0,0,1,4,0,0,9,0,0,0,12,0,1], [0,0,0,0,0,0,0,0,0,1,0,0,0], [1,0,0,0,0,0,2,0,0,2,0,0,0], [0,0,0,0,0,9,4,0,0,0,6,0,0], [0,6,9,0,0,0,0,0,0,0,0,0,0], [0,0,0,0,0,0,0,1,6,10,0,1,4], [0,3,0,0,0,1,0,0,0,0,0,2,0], [0,0,0,1,3,0,0,0,0,9,0,0,0], [9,0,0,3,3,0,0,0,0,3,4,0,0], [0,1,4,0,0,0,0,0,0,5,0,1,0], [0,0,0,0,0,0,0,0,0,0,0,0,0], [2,0,0,0,0,3,3,0,0,0,0,0,10], [0,0,0,0,0,0,0,0,0,4,0,0,0]],
		'verba': 20,
		'objetivo': [125, 126]
		},
}

# Movimentos possíveis: esquerda, baixo, direita, cima
movimentos = [(0, -1), (1, 0), (0, 1), (-1, 0)]

# Verifica se a posição está dentro dos limites do território
def dentro_do_mapa(x, y, matriz):
	return 0 <= x < len(matriz) and 0 <= y < len(matriz[0])

# Calcula o número de famílias protegidas para todas as delegacias
def calcular_todas_familias(delegacias, raios, territorio):
	todas_familias = 0
	protegidas = set()  # Conjunto para armazenar zonas já protegidas
	for (dx, dy), raio in zip(delegacias, raios):
		for x in range(dx - raio, dx + raio + 1):
			for y in range(dy - raio, dy + raio + 1):
				if dentro_do_mapa(x, y, territorio) and (x, y) not in protegidas:
					todas_familias += territorio[x][y]
					protegidas.add((x, y))
	return todas_familias

def busca_em_largura_limitada_simultanea(inicio, raio, matriz, objetivo, delegacias, raios, estados_gerados, id_territorio, i, limite):
	fila = deque([(delegacias, 0)])  # Adiciona uma flag para rastrear a profundidade de cada estado
	visitados = set([tuple(delegacias)])
	solucoes_encontradas = [False]*len(objetivo)
	num_expansoes = 1  # Contador para o número de expansões
	familias_protegidas_inicial = calcular_todas_familias(delegacias, raios, matriz)
	for j in range(len(objetivo)):
		if not solucoes_encontradas[j] and familias_protegidas_inicial >= objetivo[j]:
			solucoes_encontradas[j] = True
			print(f"Busca em Profundidade Limitada Simultânea encontrou a SOLUÇÃO {j+1} na coordenada inicial. Famílias protegidas: {familias_protegidas_inicial}")
			print(f"Coordenadas das delegacias da solução {j+1}: {delegacias}")
	while fila:
		delegacias_atual, profundidade = fila.popleft()
		if profundidade <= limite:  # Se a profundidade não exceder o limite
			expansoes = []  # Lista para guardar as expansões possíveis
			for id_delegacia, (x, y) in enumerate(delegacias_atual):
				for dx, dy in movimentos:
					nx, ny = x + dx, y + dy
					if (nx, ny) not in delegacias_atual and dentro_do_mapa(nx - raio, ny - raio, matriz) and dentro_do_mapa(nx + raio, ny + raio, matriz):
						delegacias_novas = list(delegacias_atual)
						delegacias_novas[id_delegacia] = (nx, ny)
						delegacias_novas_tupla = tuple(delegacias_novas)
						if delegacias_novas_tupla not in visitados:
							visitados.add(delegacias_novas_tupla)
							fila.append((delegacias_novas, profundidade + 1))  # Adiciona o novo estado à fila com a profundidade incrementada
							estados_gerados += 1
							expansoes.append(delegacias_novas)  # Adiciona a expansão à lista
							# Calcula a soma das famílias protegidas para todas as delegacias
							familias_protegidas = calcular_todas_familias(delegacias_novas, raios, matriz)
							for j in range(len(objetivo)):
								if not solucoes_encontradas[j] and familias_protegidas >= objetivo[j]:
									solucoes_encontradas[j] = True
									print(f"Busca em Profundidade Limitada Simultânea encontrou a SOLUÇÃO {j+1} após gerar {estados_gerados } estados e fazer {num_expansoes} expansões. Famílias protegidas: {familias_protegidas}")
									print(f"Coordenadas das delegacias da solução {j+1}: {delegacias_novas}")
			num_expansoes += 1  # Incrementa o contador de expansões
			#print(f"Expansão {num_expansoes} concluída: {delegacias_atual}, Expansões possíveis: {expansoes}")
	print(f"\nBusca em Largura Limitada Simultânea gerou {estados_gerados} estados e fez {num_expansoes} expansões.")
	return estados_gerados, solucoes_encontradas, calcular_todas_familias(delegacias, raios, matriz), num_expansoes

def busca_em_profundidade_limitada_simultanea(inicio, raio, matriz, objetivo, delegacias, raios, estados_gerados, id_territorio, i, limite):
	pilha = [(delegacias, 0)]  # Adiciona uma flag para rastrear a profundidade de cada estado
	visitados = set([tuple(delegacias)])
	solucoes_encontradas = [False]*len(objetivo)
	num_expansoes = 1  # Contador para o número de expansões
	familias_protegidas_inicial = calcular_todas_familias(delegacias, raios, matriz)
	for j in range(len(objetivo)):
		if not solucoes_encontradas[j] and familias_protegidas_inicial >= objetivo[j]:
			solucoes_encontradas[j] = True
			print(f"Busca em Profundidade Limitada Simultânea encontrou a SOLUÇÃO {j+1} na coordenada inicial. Famílias protegidas: {familias_protegidas_inicial}")
			print(f"Coordenadas das delegacias da solução {j+1}: {delegacias}")
	while pilha:
		delegacias_atual, profundidade = pilha.pop()
		if profundidade <= limite:  # Se a profundidade n exceder o limite
			expansoes = []  # Lista para guardar as expansões possíveis
			for id_delegacia, (x, y) in enumerate(delegacias_atual):
				for dx, dy in movimentos:
					nx, ny = x + dx, y + dy
					if (nx, ny) not in delegacias_atual and dentro_do_mapa(nx - raio, ny - raio, matriz) and dentro_do_mapa(nx + raio, ny + raio, matriz):
						delegacias_novas = list(delegacias_atual)
						delegacias_novas[id_delegacia] = (nx, ny)
						delegacias_novas_tupla = tuple(delegacias_novas)
						if delegacias_novas_tupla not in visitados:
							visitados.add(delegacias_novas_tupla)
							pilha.append((delegacias_novas, profundidade + 1))  # Adiciona o novo estado à pilha com a profundidade incrementada
							estados_gerados += 1
							expansoes.append(delegacias_novas)  # Adiciona a expansão à lista
							# Calcula a soma das famílias protegidas para todas as delegacias
							familias_protegidas = calcular_todas_familias(delegacias_novas, raios, matriz)
							for j in range(len(objetivo)):
								if not solucoes_encontradas[j] and familias_protegidas >= objetivo[j]:
									solucoes_encontradas[j] = True
									print(f"Busca em Profundidade Limitada Simultânea encontrou a SOLUÇÃO {j+1} após gerar {estados_gerados } estados e fazer {num_expansoes} expansões. Famílias protegidas: {familias_protegidas}")
									print(f"Coordenadas das delegacias da solução {j+1}: {delegacias_novas}")
			num_expansoes += 1  # Incrementa o contador de expansões
			#print(f"Expansão {num_expansoes} concluída: {delegacias_atual}, Expansões possíveis: {expansoes}")
	print(f"\nBusca em Profundidade Limitada Simultânea gerou {estados_gerados} estados e fez {num_expansoes} expansões.")
	return estados_gerados, solucoes_encontradas, calcular_todas_familias(delegacias, raios, matriz), num_expansoes

def busca(estrategia, inicio, raio, matriz, objetivo, delegacias, raios, estados_gerados, id_territorio, i, limite=None):
	if estrategia == 'largura_limitada':
		return busca_em_largura_limitada_simultanea(inicio, raio, matriz, objetivo, delegacias, raios, estados_gerados, id_territorio, i, limite)
	elif estrategia == 'profundidade_limitada':
			return busca_em_profundidade_limitada_simultanea(inicio, raio, matriz, objetivo, delegacias, raios, estados_gerados, id_territorio, i, limite)
		
#qual algoritmo de busca usar
estrategia = input("Que busca quer fazer? Largura Limitada - 1, Profundidade Limitada - 2: \n")

# Mapeia a entrada do usuário para a estratégia
if estrategia == '1':
	estrategia = 'largura_limitada'
	limite = int(input("Por favor, insira o limite de profundidade para a busca em largura limitada: \n"))
elif estrategia == '2':
	estrategia = 'profundidade_limitada'
	limite = int(input("Por favor, insira o limite de profundidade para a busca em profundidade limitada: \n"))
	
# Loop externo para percorrer todos os territórios
for id_territorio, dados_territorio in territorio.items():
	matriz = dados_territorio['matriz']
	verba = dados_territorio['verba']
	objetivo = dados_territorio['objetivo']
	valores = {1: 4, 2: 5, 3: 9, 4: 17}
	# Loop interno para percorrer todas as combinações possíveis para a verba disponível
	for id_combinacao, combinacao in verbas[verba].items():
		delegacias, raios = combinacao
		
		verba_usada = sum(valores[raio] for raio in raios)
		verba_restante = verba - verba_usada
		# a contagem de estados para cada nova combinação
		estados_gerados = 1
		
		start_time = time.time()
		
		# Aplica o algoritmo de busca para a combinação atual
		estados_gerados, solucoes_encontradas, familias_protegidas, num_expansoes = busca(estrategia, delegacias[0], raios[0], matriz, objetivo, delegacias, raios, estados_gerados, id_territorio, id_combinacao, limite)
		
		end_time = time.time()
		elapsed_time = end_time - start_time
		
		print(f"Território {id_territorio}, combinação {id_combinacao}.")
		print(f"Busca em {estrategia.capitalize()} gerou {estados_gerados} estados.")
		print(f"Número de expansões: {num_expansoes}")
		print(f"Verba usada: {verba_usada}, Verba restante: {verba_restante}")
		print(f"Tempo decorrido: {elapsed_time} segundos")
		if not all(solucoes_encontradas):
			if solucoes_encontradas.count(False) == len(objetivo):
				print("Nenhuma solução encontrada.\n")
			else:
				print(f"Solução {solucoes_encontradas.index(False) + 1} não encontrada.\n")
		
			