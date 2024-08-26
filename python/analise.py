#!/bin/python3
import tkinter as tk
from tkinter import filedialog
import os
import arquivo
from grafico import gfAnalise  # Importe a classe gfAnalise do módulo grafico

root = tk.Tk()
root.title("Cerebrino - Análise de arquivo")

# Cria uma instância da classe gfAnalise
grafico = gfAnalise(root)


def selecionar_arquivo():
    """Abre uma caixa de diálogo para o usuário selecionar um arquivo."""
    global arquivo_selecionado
    arquivo_selecionado = filedialog.askopenfilename(
        initialdir="./dados",
        title="Selecione um arquivo",
        filetypes=(("Arquivos de texto", "*.raw"), ("Todos os arquivos", "*.*"))
    )
    if arquivo_selecionado:
        nome_arquivo = os.path.basename(arquivo_selecionado)
        label_arquivo["text"] = f"Arquivo: {nome_arquivo}"
        sinal = arquivo.read(arquivo_selecionado)  # Lê os dados do arquivo
        #gfm.plot(filtro.aplicar_filtros(sinal))  # Aplica os filtros e Plota os dados usando o método plot() da classe gfAnalise
        grafico.plot(sinal)

button_frame = tk.Frame(master=root)
button_frame.pack(side=tk.BOTTOM, fill=tk.X)
# Cria os botões e o rótulo
botao_selecionar = tk.Button(master=button_frame, text="Selecionar Arquivo", command=selecionar_arquivo)
botao_selecionar.grid(row=0, column=0, pady=5)


label_arquivo = tk.Label(master=button_frame, text="")
label_arquivo.grid(row=0, column=1, pady=5)

root.mainloop()
