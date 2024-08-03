"""
	TENSÃO X DEFORMAÇÃO
"""

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

dados = pd.read_excel("dadosEnsaioTracao.xlsx").to_numpy()
F = dados[:,0]
dl = dados[:,1]

Lo = 0.0508
Do = 0.0127
#Teste
A = (np.pi*Do**2.0)/4

Tensao = F / A
limRT = max(Tensao)
e = dl/Lo

tamanho = Tensao.size
antAngulo = round(np.tan(e[2] / Tensao[2]),8)
limElast = 0

for id in range(3,tamanho):
    angulo = round(np.tan(e[id]/Tensao[id]),8)
    if angulo != antAngulo and limElast == 0:
        limElast = Tensao[id-1]

fig, axs = plt.subplot_mosaic([['upleft', 'right'],
                               ['lowleft', 'right']], layout='constrained')
xLimRT = e[Tensao == limRT]
yLimRT = limRT

xLimElast = e[Tensao == limElast]
yLimElast = limElast

regPlastica = (e >= xLimElast) & (e <= xLimRT)
regElastica = (e <= xLimElast)

axs["right"].plot(e, Tensao, label='Região da Ruptura')
axs["right"].plot(e[regPlastica], Tensao[regPlastica], label='Região Plástica')
axs["right"].plot(e[regElastica], Tensao[regElastica], label='Região Elástica')
#axs[1].scatter([x for x in vetorTensao if x == limRT],limRT,s=20,facecolor='C0',edgecolor='k')
axs["right"].annotate('Limite de Resistência a Tensão', xy=(e[Tensao == limRT], limRT), xytext=(e[Tensao == limRT], limRT - 100000),
                   arrowprops=dict(facecolor='black', shrink=0.1))
axs["right"].annotate('Limite de Escoamento', xy=(e[Tensao == limElast], limElast), xytext=(e[Tensao == limElast]+10, limElast - 5000),
                   arrowprops=dict(facecolor='black', shrink=0.1))
axs["right"].grid(True)
axs["right"].set_xlabel('e [m]')
axs["right"].set_ylabel('Tensão [Pa]')
axs["right"].set_title('Deformação')
axs["right"].legend()

axs["upleft"].plot(e, Tensao)
axs["upleft"].grid(True)
axs["upleft"].set_xlabel('e [m]')
axs["upleft"].set_ylabel('Tensão [Pa]')
axs["upleft"].set_title('Limite de Resistência a Tracao')

axs["lowleft"].plot(e, Tensao)
axs["lowleft"].grid(True)
axs["lowleft"].set_xlabel('e [m]')
axs["lowleft"].set_ylabel('Tensão [Pa]')
axs["lowleft"].set_title('Deformação')

plt.tight_layout
plt.show()
