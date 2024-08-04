"""
	TENSÃO X DEFORMAÇÃO
"""
from plotagem import plotagem
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Recebendo os dados do corpo de prova
dados = pd.read_excel("dadosEnsaioTracao.xlsx").to_numpy()
F = dados[:,0]
dl = dados[:,1]

# Definindo as dimenções inicias do corpo de prova
Lo = 0.0508
Do = 0.0127
A = (np.pi*Do**2.0)/4

Tensao = F / A
e = dl/Lo

# Cálculo do limite de resistência a tração
limRT = max(Tensao)

#Cálculo do limite de elasticidade
tamanho = Tensao.size
antAngulo = round(np.tan(e[2] / Tensao[2]),8)
limElast = 0

for id in range(3,tamanho):
    angulo = round(np.tan(e[id]/Tensao[id]),8)
    if angulo != antAngulo and limElast == 0:
        limElast = Tensao[id-1]

#Plotagem,definindo a posição dos limites e as regiões
fig, axs = plt.subplot_mosaic([['upleft', 'right'],
                               ['lowleft', 'right']], layout='constrained')
class Regiao:
    def __init__(self, inicio, fim, x, y, label):
        self.inicio = np.where(y == inicio)[0][0]
        self.fim = np.where(y == fim)[0][0] + 1
        self.x = x[self.inicio:self.fim]
        self.y = y[self.inicio:self.fim]
        self.label = label

regPlastica = Regiao(limElast, limRT, e, Tensao, "Região Plástica")
regElastica = Regiao(0, limElast, e, Tensao, "Região Elástica")
regRuptura = Regiao(limRT, Tensao[-1], e, Tensao, "Região da Ruptura")

plotagem.plotGeral(fig, axs, "Tensão X Deformação",  "deformação [m]", "tensão [Pa]", "right",[regElastica, regPlastica, regRuptura])
plotagem.plotMosaico(fig, axs, "Limite de Resistência a Tração", e, Tensao, "ε", "σ","upleft")
plotagem.plotMosaico(fig, axs, "Limite de Escoamento",e, Tensao, "ε", "σ","lowleft")

plt.tight_layout
plt.show()
