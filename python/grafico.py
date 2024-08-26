from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
import numpy as np
from scipy.signal import butter, lfilter
import tkinter as tk
import matplotlib.cm as cm  # Adiciona a linha de importação

def filtro_passa_faixa(sinal, lowcut, highcut, fs=1000):
    """
    Aplica um filtro passa-faixa Butterworth de segunda ordem.

    Args:
      sinal: Lista de dados do sinal.
      lowcut: Frequência de corte inferior do filtro em Hz.
      highcut: Frequência de corte superior do filtro em Hz.
      fs: Frequência de amostragem do sinal em Hz.

    Returns:
      sinais_filtrados: Lista de dados do sinal filtrado.
    """

    nyq = 0.5 * fs
    low = lowcut / nyq
    high = highcut / nyq
    b, a = butter(3, [low, high], btype='band')
    return lfilter(b, a, sinal)

# aplica filtros e retorna uma lista de sinais
def aplicar_filtros(sinal):
    return [
        filtro_passa_faixa(sinal, 2, 4),
        filtro_passa_faixa(sinal, 4, 8),
        filtro_passa_faixa(sinal, 8, 13),
        filtro_passa_faixa(sinal, 13, 30),
        filtro_passa_faixa(sinal, 30, 80),
        # np.array(sinal),
    ]

class gfCaptura:
    """
    Classe responsável por criar e gerenciar o gráfico de sinal.
    """
    def __init__(self, master, tipo='padrao', sampling_rate=1000):
        """
        Inicializa o gráfico.

        Args:
            master: A janela principal Tkinter.
            tipo: Tipo de gráfico (padrao ou analise).
            sampling_rate: Taxa de amostragem do sinal.
        """
        self.master = master
        self.fig = Figure(figsize=(8, 6), dpi=100)
        self.fig.tight_layout = True
        self.fs = sampling_rate
        self.ax1 = self.fig.add_subplot(3, 1, 1)  # Sinal original
        self.ax2 = self.fig.add_subplot(3, 1, 2)  # Espectrograma
        self.ax3 = self.fig.add_subplot(3, 1, 3)  # Gráfico de colunas
        self.buffer = []
        self.tipo = tipo

        # Define os limites dos eixos y para os subplots
        self.ax1.set_ylim(0, 1023)
        self.ax2.set_ylim(0, 1)  # Limite para o espectro
        self.ax3.set_ylim(0, 100000)  # Limite para o gráfico de colunas

        # Cria a tela Tkinter para o gráfico
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.master)
        self.canvas.draw()  # Renderiza o gráfico inicialmente

        # Adiciona a toolbar se o tipo do gráfico for "analise"
        if tipo == "analise":
            self.toolbar = NavigationToolbar2Tk(self.canvas, self.master)
            self.toolbar.update()
            self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

    def atualiza(self, sinal):
        """
        Atualiza o gráfico com novos dados.

        Args:
            sinal: Lista de dados do sinal.
        """
        self.buffer = sinal
        self.ax1.cla()  # Limpa o subplot do sinal original
        self.ax2.cla()  # Limpa o subplot do espectrograma
        self.ax3.cla()  # Limpa o subplot do gráfico de colunas
        self.ax1.plot(self.buffer, color='b')  # Plota o sinal original
        self.ax1.set_ylim(0, 1023)
        self.ax2.set_ylim(0, 100000)
        self.plota_espectrograma(self.buffer)
        self.plota_grafico_colunas(self.buffer)  # Plota o gráfico de colunas
        self.canvas.draw()  # Atualiza a tela do gráfico

    def fecha(self):
        """Fecha a janela do gráfico."""
        print("Grafico.fecha()")
        self.master.destroy()

    def on_close(self, event):
        """Fecha a janela do gráfico quando o botão de fechar é clicado."""
        print("Grfico.on_close()")
        self.fecha()

    def ativo(self):
        """Verifica se a janela do gráfico está ativa."""
        print("Grafico.ativo()")
        return self.master.winfo_exists()

    def plota_espectrograma(self, sinal):
        """
        Plota o espectrograma do sinal.

        Args:
            sinal: Lista de dados do sinal.
        """
        # Aguarda o buffer atingir 5000 antes de plotar o espectrograma
        if (len(sinal) >= 5000):
            # Cria um vetor de tempo com base no comprimento da lista de inteiros
            t = np.linspace(0, 1, len(sinal))

            # Calcula a FFT do sinal
            freq = np.fft.fftfreq(len(sinal), d=t[1] - t[0])
            espectro = np.fft.fft(sinal)

            # Filtra as frequências negativas
            espectro = espectro[:len(espectro) // 2]
            freq = freq[:len(freq) // 2]

            # Encontra o índice das frequências desejadas (0.5 Hz a 80 Hz)
            indice_min = np.argmin(np.abs(freq - 0.5))
            indice_max = np.argmin(np.abs(freq - 80))

            # Plota o espectrograma
            self.ax2.plot(freq[indice_min:indice_max], np.abs(espectro[indice_min:indice_max]))
            self.ax2.set_xlim(0.5, 80)
            self.ax2.grid(True)

    def plot_sinal(self, sinal):
        """
        Plota os dados de uma lista de sinais.
        """
        sinais = self.aplicar_filtros(sinal)

        self.ax.clear()
        # Plota os sinais filtrados
        self.ax.set_xlabel("Tempo (s)")

        # Plota cada sinal com um deslocamento vertical
        labels = ["Delta", "Theta", "Alpha", "Beta", "Gamma", "Bruto"]  # Lista de labels
        for i, sinal in enumerate(sinais):
            self.ax.plot(sinal + 800 - i * 200, label=labels[i])  # Plota no mesmo subplot

        # Configura os ticks do eixo x para o último subplot
        self.ax.set_xticks(range(0, len(sinais[0]), 1000))
        self.ax.set_xticklabels([str(i / 1000) for i in range(0, len(sinais[0]), 1000)])
        self.ax.set_yticks([])  # Remove os ticks do eixo y do último subplot

        # Coloca a legenda do lado esquerdo do gráfico
        self.ax.legend(loc='lower left', bbox_to_anchor=(0.9, 0))  # Altera a posição da legenda

        self.canvas.draw()



    import matplotlib.cm as cm

    def plota_grafico_colunas(self, sinal):
        """
        Plota um gráfico de colunas mostrando a intensidade do sinal em cada faixa de frequência, com cores em degradê.
    
        Args:
            sinal: Lista de dados do sinal.
        """
        sinais_filtrados = aplicar_filtros(sinal)
        
        # Calcula a intensidade média de cada faixa de frequência
        intensidades = [np.mean(np.abs(sinal)) for sinal in sinais_filtrados]
    
        # Normaliza as intensidades para o intervalo de 0 a 50
        intensidades_normalizadas = [intensidade / np.max(intensidades) * 50 for intensidade in intensidades]
    
        # Define as labels para cada faixa de frequência
        labels = ["Delta", "Theta", "Alpha", "Beta", "Gamma"]
    
        # Define o mapa de cores
        cmap = cm.get_cmap('viridis')  # Mapa de cores 'RdYlGn_r' (invertido)
    
        # Plota o gráfico de colunas com cores em degradê
        bars = self.ax3.bar(labels, intensidades_normalizadas)
        for bar, intensidade in zip(bars, intensidades_normalizadas):
            bar.set_color(cmap(intensidade / 50))  # Define a cor da barra usando o mapa de cores
    
        # Adiciona linhas horizontais de 5 em 5
        for i in range(5, 51, 5):
            self.ax3.hlines(i, -0.5, 4.5, linestyles='--', colors='gray', linewidth=0.5)
    
        self.ax3.set_ylim(0, 50)
        
        
class gfAnalise:
    def __init__(self, master):
        self.master = master  # Armazena a referência ao master (janela Tkinter)
        self.fig = Figure(tight_layout = True)
        self.ax = self.fig.add_subplot()
        self.buffer = []

        # Configura os limites do eixo y aqui
        #self.ax.set_ylim(0, 1023)

        # Cria o canvas TkAgg
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.master)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        # Cria o menu do gráfico
        self.toolbar = NavigationToolbar2Tk(self.canvas, self.master)
        self.toolbar.update()
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

    def plot(self, sinal):
        """
        Plota os dados de uma lista de sinais
        """
        sinais = aplicar_filtros(sinal)
        
        self.ax.clear()
        # Plota os sinais filtrados
        self.ax.set_xlabel("Tempo (s)")

        # Plota cada sinal com um deslocamento vertical
        labels = ["Delta", "Theta" , "Alpha", "Beta", "Gamma", "Bruto"]  # Lista de labels
        for i, sinal in enumerate(sinais):
            self.ax.plot(sinal + 800 -i * 50, label=labels[i])  # Plota no mesmo subplot

        # Configura os ticks do eixo x para o último subplot
        self.ax.set_xticks(range(0, len(sinais[0]), 1000))
        self.ax.set_xticklabels([str(i / 1000) for i in range(0, len(sinais[0]), 1000)])
        self.ax.set_yticks([])  # Remove os ticks do eixo y do último subplot

        # Coloca a legenda do lado esquerdo do gráfico
        self.ax.legend(loc='lower left', bbox_to_anchor=(0.9, 0))  # Altera a posição da legenda

        self.canvas.draw()
   



                
