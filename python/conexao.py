import serial
import threading
from collections import deque

class Conexao(threading.Thread):
    def __init__(self):
        super().__init__()
        self.connected = False
        self.read_bytes = 0
        self.buffer = deque()  # Utiliza deque como buffer

    def connect(self, port, baudrate = 115200):
        #
        self.port = port
        self.baudrate = baudrate
        try:
            self.cnserial = serial.Serial(self.port, self.baudrate)
            self.connected = True
        except serial.SerialException as e:
            print(f"Erro ao abrir a porta serial: {e}")
            self.connected = False

    def run(self):
        while self.connected:
            # Lê um byte da porta serial
            byte_alto = ord(self.cnserial.read(1))
            
            # Datagrama
            # Se o byte for um byte alto válido, lê o byte baixo e monta o valor inteiro
            if (byte_alto & 0b10000000) == 0b10000000:
                byte_baixo = ord(self.cnserial.read(1))
                valor_inteiro = (byte_baixo & 0b1111111) | ((byte_alto & 0b111) << 7)
                self.buffer.append(valor_inteiro)  # Adiciona o valor ao buffer

#    def status(self):
#        return self.connected
    
    def read(self):
        dados_lidos = list(self.buffer)  # Lê todos os dados do buffer
        self.buffer.clear()  # Limpa o buffer
        return dados_lidos

    def stop(self):
        if self.connected:
            self.connected = False
            self.read_bytes = 0
        if self.cnserial:
            self.cnserial.close()
        # Espera a thread terminar
        self.join()
        print("conexão parada")
        

        