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
antAngulo = round(np.tan(e[1] / Tensao[1]),8)
limElast = 0

for id in range(2,tamanho):
    angulo = round(np.tan(e[id]/Tensao[id]),8)
    if angulo != antAngulo and limElast == 0:
        limElast = Tensao[id-1]

#Plotagem,definindo a posição dos limites e as regiões
fig, axs = plt.subplot_mosaic([['left', 'upright'],
                               ['left', 'lowright']], layout='constrained')
class Regiao:
    def __init__(self, inicio, fim, x, y, label, limite,cor):
        self.inicio = np.where(y == inicio)[0][0]
        self.fim = np.where(y == fim)[0][0] + 1
        self.x = x[self.inicio:self.fim]
        self.y = y[self.inicio:self.fim]
        self.limite = limite
        self.label = label
        self.cor = cor

regElastica = Regiao(0, limElast, e, Tensao, "Região Elástica", "Limite de Escoamento","orange")
regPlastica = Regiao(limElast, limRT, e, Tensao, "Região Plástica", "Limite de Resistência a Tração","blue")
regRuptura = Regiao(limRT, Tensao[-1], e, Tensao, "Região da Ruptura", "Ruptura","red")

limFinalX_plot1 = regPlastica.x[4]
limInicialX_plot1 = 0

limFinalY_plot1 = regPlastica.y[4]
limInicialY_plot1 = 0

limFinalX_plot2 = regRuptura.x[1]+2
limInicialX_plot2 = regPlastica.x[4]

limFinalY_plot2 = max(regRuptura.y) + 100000
limInicialY_plot2 = regPlastica.y[4]


plotagem.plotMosaico(fig, axs, "Tensão X Deformação",  "ε deformação [m]", "σ tensão [Pa]", "left",[regElastica, regPlastica, regRuptura],[0,max(e)+20,0,max(Tensao)+100000])
plotagem.plotMosaico(fig, axs, "Limite de Escoamento",  "", "", "upright",[regElastica, regPlastica],[limInicialX_plot1, limFinalX_plot1,limInicialY_plot1,limFinalY_plot1])
plotagem.plotMosaico(fig, axs, "Limite de Resistência a Tração",  "", "", "lowright",[regPlastica, regRuptura],[limInicialX_plot2, limFinalX_plot2,limInicialY_plot2,limFinalY_plot2])

plt.tight_layout
plt.show()
