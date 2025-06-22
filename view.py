# importando SQLite & Pandas
import sqlite3 as lite
import pandas as pd
import os
import sys

# Função para encontrar o caminho correto dos recursos (imagens, banco de dados)
def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

# criando conexão
con = lite.connect(resource_path('dados.db'))

# funcao inserir categoria ----------------------------
def inserir_categoria(i):
    with con:
        cur = con.cursor()
        query = "INSERT INTO Categoria (nome) VALUES (?)"
        cur.execute(query,i)

# funcao inserir receitas -----------------------------
def inserir_receita(i):
    with con:
        cur = con.cursor()
        query = "INSERT INTO Receitas (categoria, adicionado_em,valor) VALUES (?,?,?)"
        cur.execute(query,i)

# funcao inserir gastos -------------------------------
def inserir_gastos(i):
    with con:
        cur = con.cursor()
        query = "INSERT INTO Gastos (categoria, retirado_em,valor) VALUES (?,?,?)"
        cur.execute(query,i)

# funcao deletar receitas ----------------------------- 
def deletar_receitas(i):
    with con:
        cur = con.cursor()
        query = "DELETE FROM Receitas WHERE id=?"
        cur.execute(query,i)

# funcao deletar gastos ------------------------------- 
def deletar_gastos(i):
    with con:
        cur = con.cursor()
        query = "DELETE FROM Gastos WHERE id=?"
        cur.execute(query,i)        

# funcao ver categoria --------------------------------
def ver_categoria():
    lista_itens = []

    with con:
         cur = con.cursor()
         cur.execute("SELECT * FROM Categoria")
         linha = cur.fetchall()
         for l in linha:
             lista_itens.append(l)

    return lista_itens

# funcao ver receita ----------------------------------
def ver_receitas():
    lista_itens = []

    with con:
         cur = con.cursor()
         cur.execute("SELECT * FROM Receitas")
         linha = cur.fetchall()
         for l in linha:
             lista_itens.append(l)

    return lista_itens
      # ver gastos

# funcao ver gastos ----------------------------------- 
def ver_gastos():
    lista_itens = []

    with con:
         cur = con.cursor()
         cur.execute("SELECT * FROM Gastos")
         linha = cur.fetchall()
         for l in linha:
             lista_itens.append(l)

    return lista_itens

# funcao para dados da tabela -------------------------
def tabela():

    gastos =  ver_gastos()
    receitas = ver_receitas()

    tabela_lista = []
    
    for i in gastos:
        tabela_lista.append(i)

    for i in receitas:
        tabela_lista.append(i)

    return tabela_lista        

# funcao grafico bar ---------------------------------
def bar_valores():
    # receita total
    receitas = ver_receitas()
    receitas_lista =  []

    for i in receitas:
        receitas_lista.append(i[3])
    
    receita_total = sum(receitas_lista)

    # despesas total
    gastos = ver_gastos()
    gastos_lista =  []

    for i in gastos:
        gastos_lista.append(i[3])
    
    gasto_total = sum(gastos_lista)

    # saldo total 
    saldo_total = receita_total - gasto_total

    return [receita_total, gasto_total, saldo_total]

# funcao grafio pie ----------------------------------
def pie_valores():
    gastos = ver_gastos()
    tabela_lista = []

    for i in gastos:
        tabela_lista.append(i)

    dataframe =  pd.DataFrame(tabela_lista, columns=['id','categoria','data','valor'])
    dataframe = dataframe.groupby('categoria')['valor'].sum()

    lista_quantias = dataframe.values.tolist()
    lista_categorias = [] 

    for i in dataframe.index:
        lista_categorias.append(i)

    return([lista_categorias, lista_quantias])    

# funcao percentagem ---------------------------------- 
def percentagem_valor():
    # receita total
    receitas = ver_receitas()
    receitas_lista = [i[3] for i in receitas] if receitas else [0]
    receita_total = sum(receitas_lista)

    # despesas total
    gastos = ver_gastos()
    gastos_lista = [i[3] for i in gastos] if gastos else [0]
    gasto_total = sum(gastos_lista)

    # percentagem total 
    if receita_total == 0:
        # Se não há receitas, retorna 0% ou outro valor padrão
        total = 0
        # Alternativa: total = -gasto_total  # Mostraria o déficit percentual
    else:
        total = ((receita_total - gasto_total) / receita_total) * 100

    return [total]


    