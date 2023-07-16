# -*- coding: utf-8 -*-
from tkinter import *
from tkinter.ttk import Combobox
import pyodbc

# Configurações do banco de dados SQL Server
server = 'SQL5085.site4now.net'
database = 'db_a9c2c8_tarefas'
username = 'db_a9c2c8_tarefas_admin'
password = 'Vitoriade10.'

# Função para conectar ao banco de dados
def conectar_banco():
    conn = pyodbc.connect(f"DRIVER=ODBC Driver 17 for SQL Server;SERVER={server};DATABASE={database};UID={username};PWD={password}")
    return conn

# Função para obter todas as tarefas
def obter_tarefas():
    conn = conectar_banco()
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM Tarefas')
    tarefas = cursor.fetchall()

    conn.close()

    return tarefas

# Função para obter todas as categorias
def obter_categorias():
    conn = conectar_banco()
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM Categoria')
    categorias = cursor.fetchall()

    conn.close()

    return categorias

# Função para obter todos os status
def obter_status():
    conn = conectar_banco()
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM Status')
    status = cursor.fetchall()

    conn.close()

    return status

# Função para adicionar uma nova tarefa
def adicionar_tarefa():
    titulo = entry_titulo.get()
    descricao = entry_descricao.get()
    categoria = combo_categoria.get()
    status = combo_status.get()
    # Obtenha os valores dos outros campos conforme necessário

    conn = conectar_banco()
    cursor = conn.cursor()

    cursor.execute('''
        INSERT INTO Tarefas (titulo, descricao, categoria_id, status_id) VALUES (?, ?, ?, ?)
    ''', (titulo, descricao, categoria, status))
    
    conn.commit()
    conn.close()

    # Atualize a lista de tarefas
    atualizar_lista_tarefas()

# Função para excluir uma tarefa selecionada
def excluir_tarefa():
    index = lista_tarefas.curselection()
    if index:
        tarefa = lista_tarefas.get(index)
        tarefa_id = tarefa.split(':')[1].strip()

        conn = conectar_banco()
        cursor = conn.cursor()

        cursor.execute('DELETE FROM Tarefas WHERE id = ?', (tarefa_id,))
        
        conn.commit()
        conn.close()

        # Atualize a lista de tarefas
        atualizar_lista_tarefas()

# Função para atualizar a lista de tarefas
def atualizar_lista_tarefas():
    lista_tarefas.delete(0, END)
    tarefas = obter_tarefas()
    for tarefa in tarefas:
        lista_tarefas.insert(END, "Tarefa ID: {}, Titulo: {}".format(tarefa[0], tarefa[1]))

# Função para verificar login e senha
def verificar_login_senha():
    login = entry_login.get()
    senha = entry_senha.get()
    # Adicione sua lógica de verificação de login e senha aqui

# Cria a janela principal
janela = Tk()
janela.title("Tarefas")

# Cria uma lista para exibir as tarefas
lista_tarefas = Listbox(janela)
lista_tarefas.pack()

# Obtém as tarefas do banco de dados e adiciona à lista
atualizar_lista_tarefas()

# Cria campos de entrada para adicionar novas tarefas
entry_titulo = Entry(janela)
entry_titulo.pack()

entry_descricao = Entry(janela)
entry_descricao.pack()

# Obtém categorias e status do banco de dados
categorias = obter_categorias()
status = obter_status()

# Cria campo de seleção para categoria
combo_categoria = Combobox(janela)
combo_categoria['values'] = categorias
combo_categoria.pack()

# Cria campo de seleção para status
combo_status = Combobox(janela)
combo_status['values'] = status
combo_status.pack()

# Cria botões para adicionar e excluir tarefas
button_adicionar = Button(janela, text="Adicionar Tarefa", command=adicionar_tarefa)
button_adicionar.pack()

button_excluir = Button(janela, text="Excluir Tarefa", command=excluir_tarefa)
button_excluir.pack()

# Cria campos de entrada para login e senha
entry_login = Entry(janela)
entry_login.pack()

entry_senha = Entry(janela, show="*")
entry_senha.pack()

# Cria botão para verificar login e senha
button_verificar = Button(janela, text="Verificar Login e Senha", command=verificar_login_senha)
button_verificar.pack()

# Inicia o loop principal da janela
janela.mainloop()

