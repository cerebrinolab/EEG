import serial
import threading

class Conexao(threading.Thread):
    def __init__(self):
        super().__init__()
        self.connected = False

    def connect(self, port, baudrate = 115200):
        #
        self.port = port
        self.baudrate = baudrate
        self.dados = []
        try:
            self.cnserial = serial.Serial(self.port, self.baudrate)
            self.connected = True
        except serial.SerialException as e:
            print(f"Erro ao abrir a porta serial: {e}")
            self.connected = False

    def run(self):
        while self.connected:
            byte_lido = ord(self.cnserial.read(1))

            if (byte_lido & 0b10000000) == 0b10000000:
                byte_baixo = ord(self.cnserial.read(1))
                valor_inteiro = (byte_baixo & 0b1111111) | ((byte_lido & 0b111) << 7)
                self.dados.append(valor_inteiro)
            
    def status(self):
        return self.connected

    def stop(self):
        if self.connected:
            self.connected = False
        print("conexão parada")
        
    def read(self, nbytes = 0):

        if nbytes > 0:
            
            if nbytes > len(self.dados):
                return self.dados
            else:
                
                return self.dados[-nbytes:]
        else:
            return self.dados

        
