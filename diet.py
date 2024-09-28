import pandas as pd
from scipy.optimize import linprog

'''

Objetivo: Minimizar custo

Variáveis de decisão: x1, x2, ..., xn - Onde cada xi são dólares gastos com alimento i.

Função objetivo: Somatório dos xi

Restrições: 

'''

# Unidades das demandas nutricionais.
unidade_necessidades_nutricionais = [100, 0.01, 100, 0.1, 1]
unidade_necessidades_nutricionais_nomes = ["calorias", "gramas", "u.i.", "miligramas, miligramas"]

# Unidades da disponibilidade de nutriente no produto X
unidades_disponibilidade_produto_x = [1000, 0.1, 1000, 0.1, 1]
unidades_disponibilidade_produto_x_nomes = ["calorias / dólar", "gramas / dólar", "u.i. / dólar", "miligramas / dólar", "miligramas / dólar"]

# Unidades da disponibilidade de nutrientes nas mercadorias
unidades_disponibilidade_mercadorias = [1000, 1, 1000, 1, 1]
unidades_disponibilidade_mercadorias_nomes = ["calorias / dólar", "gramas / dólar", "u.i. / dólar", "miligramas / dólar", "miligramas / dólar"]

# Read the CSV files into separate variables
disponibilidade_nutricionais = pd.read_csv('disponibilidade-nutricionais.csv')
necessidades_nutricionais = pd.read_csv('necessidades-nutricionais.csv')

# Display the first few rows of each DataFrame to verify
#print("Disponibilidade Nutricionais:")
#print(disponibilidade_nutricionais.head())

#print("\nNecessidades Nutricionais:")
#print(necessidades_nutricionais.head())

alunos = ["Artur", "Daniel", "Tales"]
nutrientes = ["Calorias", "Cálcio", "Vit. A", "Riboflavina", "Ác. asc."]

c = [1] * 9
    
# Para cada aluno
for i in range( len(alunos) ):

    print ("Aluno: " + alunos[i] + "\n")

    A = [] # Matriz tecnologica do problema.

    # Para cada nutriente que o aluno necessita
    for j in range( len(nutrientes) ):

        # Lê disponibilidade da cada nutriente no csv.
        linha = disponibilidade_nutricionais.iloc[:,j+2].tolist()
        
        # Aplica o fator das unidades nos valores lidos do csv, menos nos produtos X.
        for k in range( len(linha)-3 ):
            linha[k] *= unidades_disponibilidade_mercadorias[j]

        # Retira a disponibilidade do nutriente no produto X dos demais alunos
        if alunos[i] == "Artur":
            linha.pop() # Retira os dois últimos elementos
            linha.pop()
        elif alunos[i] == "Daniel":
            linha.pop() # Retira o último
            linha.pop( len(linha) - 1 ) # Retira o penúltimo
        elif alunos[i] == "Tales":
            linha.pop( len(linha) - 1 ) # Retira o penúltimo duas vezes
            linha.pop( len(linha) - 1 )

        linha[ len(linha)-1 ] *= unidades_disponibilidade_produto_x[j]

        print(f"{nutrientes[j]:<{12}}", end=": ")
        print (linha)
        A += [linha]

    print()
    
    b = necessidades_nutricionais.iloc[:,i].tolist()

    for i in range( len(b) ):
        b[i] *= unidade_necessidades_nutricionais[i]

    print("b: ", end = "")
    print(b)
    print()

    print(c)

    # Bounds for each variable (default is (0, None) for non-negative variables)
    x_bounds = [(0, None)] * 9  # Non-negative decision variables

    # Solve the linear programming problem
    res = linprog(c, A_ub=A, b_ub=b, bounds=x_bounds, method='highs')

    # Display the results
    if res.success:
        print("Optimal solution found:")
        print(f"x = {res.x}")
        print(f"Optimal value: {res.fun}")
    else:
        print("No optimal solution found.")



        
