"""
	TENSÃO X DEFORMAÇÃO
"""
from plotagem import plotagem
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Recebendo os dados do corpo de prova
dados = pd.read_excel("dadosEnsaioTracao.xlsx").to_numpy()
Forca = dados[:,0] # Em N
comprimentoFinal = dados[:,1] # Em Metro

# Definindo as dimenções inicias do corpo de prova. OBS: tudo em milímetro
comprimentoInicial = 50.8
diametroInicial = 12.8
area = (np.pi*diametroInicial**2.0)/4

Tensao = Forca / area
e = (comprimentoFinal-comprimentoInicial)/comprimentoInicial

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
fig, axs = plt.subplot_mosaic([['upleft', 'upright'],
                               ['lowleft', 'lowright']],  gridspec_kw={'hspace': 0.5})
class Regiao:
    def __init__(self, inicio, fim, x, y, label, limite, cor):
        self.inicio = np.where(y == inicio)[0][0]
        self.fim = np.where(y == fim)[0][0] + 1
        self.x = x[self.inicio:self.fim]
        self.y = y[self.inicio:self.fim]
        self.limite = limite
        self.label = label
        self.cor = cor
        x0, y0 = self.x[0],self.y[0]
        x1, y1 = self.x[-1],self.y[-1]
        deltaX = x1-x0
        deltaY = y1-y0
        self.variacao = (deltaY)/(deltaX)
        self.angulo = np.arctan2(self.y,self.x)
        self.anguloGraus = (angulo*180)/np.pi

regElastica = Regiao(0, limElast, e, Tensao, "Região Elástica", "Limite de Escoamento", "orange")
regPlastica = Regiao(limElast, limRT, e, Tensao, "Região Plástica", "Limite de Resistência a Tração", "blue")
regRuptura = Regiao(limRT, Tensao[-1], e, Tensao, "Região da Ruptura", "Ruptura", "red")

limInicial_plot0 = (0,0)
limFinal_plot0 = (max(e)+0.1, max(Tensao)+0.1)

limInicial_plot1 = (0,0)
limFinal_plot1 = (regPlastica.x[4], regPlastica.y[4])

limInicial_plot2 = (regPlastica.x[6], regPlastica.y[6])
limFinal_plot2 = (regRuptura.x[1]+0.05, max(regRuptura.y)+0.01)

limInicial_plot3 = (0,0)
limFinal_plot3 = (max(regElastica.x)+0.001, max(regElastica.y)+0.01)


enquadroPlot0 = [limInicial_plot0[0], limFinal_plot0[0], limInicial_plot0[1], limFinal_plot0[1]]
enquadroPlot1 = [limInicial_plot1[0], limFinal_plot1[0], limInicial_plot1[1], limFinal_plot1[1]]
enquadroPlot2 = [limInicial_plot2[0], limFinal_plot2[0], limInicial_plot2[1], limFinal_plot2[1]]
enquadroPlot3 = [limInicial_plot3[0], limFinal_plot3[0], limInicial_plot3[1], limFinal_plot3[1]]

distanciaTextPlot0 = (0.04,0.02)
distanciaTextPlot1 = (0.001,0)
distanciaTextPlot2= (-0.02,-0.02)
distanciaTextPlot3 = (0.0001,-0.02)

lengedaLocPlot0 = "lower right"
lengedaLocPlot1 = "lower right"
lengedaLocPlot2 = "upper right"
lengedaLocPlot3 = "upper right"

plotagem.plotMosaico(fig, axs, "Tensão X Deformação",  "ε deformação [%]", "σ tensão [Pa]", "upleft", [regElastica, regPlastica, regRuptura], enquadroPlot0, distanciaTextPlot0, lengedaLocPlot0,False)
plotagem.plotMosaico(fig, axs, "Limite de Escoamento",  "", "", "upright", [regElastica, regPlastica], enquadroPlot1, distanciaTextPlot1, lengedaLocPlot1, False)
plotagem.plotMosaico(fig, axs, "Limite de Resistência a Tração",  "", "", "lowright", [regPlastica, regRuptura], enquadroPlot2, distanciaTextPlot2, lengedaLocPlot2, False)
plotagem.plotMosaico(fig, axs, "Módulo de Elasticidade",  "", "", "lowleft", [regElastica], enquadroPlot3, distanciaTextPlot3, lengedaLocPlot3)

plt.tight_layout
plt.show()
