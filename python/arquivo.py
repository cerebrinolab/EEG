"""
Created on Wed Feb 28 23:13:36 2024

@author: luiz fernando
"""

import numpy as np
import os
import struct

def read(path, inicio=0, nbytes=None):
  with open(path, "rb") as arquivo:
    if nbytes is None:
      nbytes = os.path.getsize(path)
    arquivo.seek(inicio)
    dados_bytes = arquivo.read(nbytes)
  dados = []
  for i in range(0, len(dados_bytes), 2):
    valor_uint16 = struct.unpack("<H", dados_bytes[i:i+2])[0]
    dados.append(valor_uint16)
  return dados

def write(path, dados):
  with open(path, "wb") as arquivo:
    dados_bytes = np.array(dados, dtype=np.uint16).tobytes()
    arquivo.write(dados_bytes)
