#!/bin/python3
import tkinter as tk
import serial.tools.list_ports
import datetime
import time

# meus módulos
from grafico import gfCaptura
from conexao import Conexao
from arquivo import write

# Importa NavigationToolbar2Tk
#from matplotlib.backends.backend_tkagg import  NavigationToolbar2Tk 

nome_arquivo = ""
time_window = 1
conexao_ativa = False
buffer_conexao = []
graph_running = False  # Adiciona a variável de controle para o loop do gráfico

# Cria a janela principal
root = tk.Tk()
root.title("Cerebrino - Captura e gravação de sinais")

# Cria o frame de botões
button_frame = tk.Frame(master=root)
button_frame.pack(side=tk.BOTTOM, fill=tk.X)

# Cria o label do dropdown
port_label = tk.Label(button_frame, text="Port:")
port_label.grid(row=0, column=0, pady=5)

# Lê a lista de portas
port_options = [port.device for port in serial.tools.list_ports.comports()]
port_variable = tk.StringVar(button_frame)

# Define o valor inicial da variável
port_variable.set("teste")  # Define "teste" como valor inicial

# Cria o OptionMenu
port_dropdown = tk.OptionMenu(button_frame, port_variable, "none", *port_options)
port_dropdown.grid(row=0, column=1, pady=5)

# Conecta o evento de clique no dropdown
port_dropdown.bind("<Button-1>", lambda event: update_port_options())

# Cria o gráfico
grafico_instancia = gfCaptura(root)  # Cria a instância do gráfico

# Organiza o gráfico na janela
grafico_instancia.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True) 

# Cria os botões
button_start = tk.Button(master=button_frame, text="start")
button_start.grid(row=0, column=3, pady=5)
button_stop = tk.Button(master=button_frame, text="stop")
button_stop.grid(row=0, column=4, pady=5)
button_save = tk.Button(master=button_frame, text="save")
button_save.grid(row=0, column=5, pady=5)

# Função para atualizar o gráfico continuamente
def update_graph():
    global buffer_conexao, graph_running
    while graph_running:  # Adiciona a condição para controlar o loop
        buffer_conexao.extend(conexao.read())
        grafico_instancia.atualiza(buffer_conexao[-(5000):])
        root.update()  # Atualiza a janela Tkinter
        time.sleep(0.1)  # Ajuste o intervalo de atualização aqui

# Função para atualizar as opções do dropdown
def update_port_options():
    """Atualiza as opções do dropdown com as portas disponíveis,
    mantendo "teste" na primeira posição.
    """
    port_dropdown['menu'].delete(0, 'end')  # Limpa as opções existentes

    # Adiciona "none" como a primeira opção
    port_dropdown['menu'].add_command(label="teste", command=lambda value="teste": port_variable.set(value))

    # Adiciona as portas disponíveis
    new_options = [port.device for port in serial.tools.list_ports.comports()]
    for option in new_options:
        port_dropdown['menu'].add_command(label=option, command=lambda value=option: port_variable.set(value))

    # Define "none" como o valor inicial se houver novas opções
    if new_options:
        port_variable.set("teste")


# Funções dos botões
def button_start_click():
        print("start()")
        global nome_arquivo, conexao, graph_running, buffer_conexao
        buffer_conexao = []
        data_hora = datetime.datetime.now()
        nome_arquivo = "./dados/" + f"{data_hora.strftime('%y%m%d-%H-%M-%S')}.raw"

        selected_port = port_variable.get()
        conexao = Conexao()
        if  port_variable.get() == 'teste':
            simula = True
        else:
            simula = False
        # print(f"Porta selecionada: {selected_port}")
        conexao.connect(selected_port, 115200)
        conexao.start()
        graph_running = True  # Define a variável de controle como True

        button_start.config(state=tk.DISABLED)
        button_stop.config(state=tk.NORMAL)
        button_save.config(state=tk.DISABLED)
        port_dropdown.config(state=tk.DISABLED)
        
        # Organiza o gráfico na janela
        grafico_instancia.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True) 
        
        update_graph()  # Inicia a atualização do gráfico


def button_stop_click():
    global buffer_conexao, graph_running
    graph_running = False  # Define a variável de controle como False
    # buffer_conexao = conexao.read()
    conexao.stop()
    button_start.config(state=tk.NORMAL)
    button_save.config(state=tk.NORMAL)
    button_stop.config(state=tk.DISABLED)
    port_dropdown.config(state=tk.NORMAL)


def button_save_click():
    write(nome_arquivo, buffer_conexao)
    button_start.config(state=tk.NORMAL)
    button_stop.config(state=tk.DISABLED)
    button_save.config(state=tk.DISABLED)
    port_dropdown.config(state=tk.NORMAL)


def close():
    # Execute as instruções aqui antes de fechar
    print("Botão fechar pressionado!")
    global graph_running, conexao, conexao_ativa
    graph_running = False
    if conexao_ativa:
        conexao.stop()
    root.destroy()  # Fecha a janela


root.protocol("WM_DELETE_WINDOW", close)


# Conecta as funções nos botões

button_start.config(command=button_start_click, state=tk.NORMAL)
button_stop.config(command=button_stop_click, state=tk.DISABLED)
button_save.config(command=button_save_click, state=tk.DISABLED)

# Inicia o loop principal do Tkinter
root.mainloop()
