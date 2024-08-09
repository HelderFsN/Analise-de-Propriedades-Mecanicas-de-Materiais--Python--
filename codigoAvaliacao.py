"""
	TENSÃO X DEFORMAÇÃO
"""
from plotagem import mosaico
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

def calcularTensao_Deformacao(dados, comprimentoInicial=float, diametroInicial=float, tipoDado=int):
    dadosNumpy = dados.to_numpy()
    
    # Em Newtons
    if dados.columns[0].upper() == "KN":
        Forca = dadosNumpy[:,0]*1000
    else:
        Forca = dadosNumpy[:,0]
    
    if tipoDado == 1:
        variacaoDeComprimento = dadosNumpy[:,1] - comprimentoInicial
    else:
        variacaoDeComprimento = dadosNumpy[:,1] # Em Milímetro

    # Definindo as dimenções inicias do corpo de prova. OBS: tudo em milímetro
    area = (np.pi*diametroInicial**2.0)/4
    
    Tensao_corpo = Forca / area
    e_corpo = variacaoDeComprimento/comprimentoInicial
    
    return (e_corpo, Tensao_corpo)
        


def analisarCorpoDeProva(e, Tensao):
    # Cálculo do limite de resistência a tração
    limRT = max(Tensao)
    
    #Cálculo do limite de elasticidade
    tamanho = Tensao.size
    anguloInicial = round(np.tan(e[1] / Tensao[1]),8)
    limElast = 0
    
    for id in range(2,tamanho):
        angulo = round(np.tan(e[id]/Tensao[id]),8)
        if angulo != anguloInicial:
            limElast = Tensao[id-1]
            break
    
    
    #,definindo a posição dos limites e as regiões
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
            print(deltaX)
            print(deltaY)
            self.variacao = (deltaY)/(deltaX)                                
            self.angulo = np.arctan(self.variacao)
            self.anguloGraus = (angulo*180)/np.pi
    
    regElastica = Regiao(0, limElast, e, Tensao, "Região Elástica", "Limite de Escoamento", "orange")
    regPlastica = Regiao(limElast, limRT, e, Tensao, "Região Plástica", "Limite de Resistência a Tração", "blue")
    regRuptura = Regiao(limRT, Tensao[-1], e, Tensao, "Região da Ruptura", "Ruptura", "red")
    
    return [regElastica,regPlastica,regRuptura]

def PlotarRegioes(regioes, larguraPlot, alturaPlot, percentPos):
    #Plotagem
    regElastica = regioes[0]
    regPlastica = regioes[1]
    regRuptura = regioes[2]
    
    if len(regPlastica.x) % 2 == 0:    
        IdMeioRegPlastica = int(len(regPlastica.x)/2)
    else:
        IdMeioRegPlastica = int((len(regPlastica.x)/2) - 0.5)
        
    if len(regRuptura.x) % 2 == 0:
        idMeioRegRuptura = int(len(regRuptura.x)/2)
    else:
        idMeioRegRuptura = int((len(regRuptura.x)/2) - 0.5)
        
    
    limInicial_plot1 = (0,0)
    limFinal_plot1 = (regPlastica.x[IdMeioRegPlastica], regPlastica.y[IdMeioRegPlastica])
    
    limInicial_plot2 = (regPlastica.x[IdMeioRegPlastica], regPlastica.y[IdMeioRegPlastica])
    limFinal_plot2 = (regRuptura.x[idMeioRegRuptura]+larguraPlot, max(regRuptura.y)+alturaPlot)
    
    enquadroPlot0 = [0,regRuptura.x[-1]+larguraPlot,0,regPlastica.y[-1]+alturaPlot]
    enquadroPlot1 = [limInicial_plot1[0], limFinal_plot1[0], limInicial_plot1[1], limFinal_plot1[1]]
    enquadroPlot2 = [limInicial_plot2[0], limFinal_plot2[0], limInicial_plot2[1], limFinal_plot2[1]]
    enquadroPlot3 = [0,max(regElastica.x)+larguraPlot/10,0,max(regElastica.y)+alturaPlot]
    
    lengedaLocPlot0 = "lower right"
    lengedaLocPlot1 = "lower right"
    lengedaLocPlot2 = "lower right"
    lengedaLocPlot3 = "upper left"
    
    fig, grafico = plt.subplot_mosaic([['upleft', 'upright'],
                                   ['lowleft', 'lowright']], figsize=(15,10), gridspec_kw={'hspace': 0.5})
    
    mosaico.plotMosaicoRegioes(grafico, "Tensão X Deformação",  "ε deformação [%]", "σ tensão [MPa]", "upleft", regioes, enquadroPlot0, lengedaLocPlot0, percentPos, False)
    mosaico.plotMosaicoRegioes(grafico, "Limite de Escoamento",  "", "", "upright", regioes[0:2], enquadroPlot1, lengedaLocPlot1, 1, False)
    mosaico.plotMosaicoRegioes(grafico, "Limite de Resistência a Tração",  "", "", "lowright", regioes[1:3], enquadroPlot2, lengedaLocPlot2, 0.5, False)
    mosaico.plotMosaicoRegioes(grafico, "Módulo de Elasticidade",  "", "", "lowleft", [regElastica], enquadroPlot3, lengedaLocPlot3, percentPos, True)
     
    plt.tight_layout
    plt.show()
    
    

# Recebendo os dados do corpo de prova
dados1_N_MM = pd.read_excel("dadosEnsaioTracao.xlsx")
dados2_KN_MM = pd.read_excel("dados2.xlsx")
dados3_KSI = pd.read_excel("dados3.xlsx")

dados1 = calcularTensao_Deformacao(dados1_N_MM, 50.8, 12.8, 1)
dados2 = calcularTensao_Deformacao(dados2_KN_MM, 50, 13, 2)
dados3 = dados3_KSI.to_numpy()

regioes1 = analisarCorpoDeProva(dados1[0], dados1[1])
regioes2 = analisarCorpoDeProva(dados2[0], dados2[1])
regioes3 = analisarCorpoDeProva(dados3[:,1], dados3[:,0]*6.89476)

percentDistAteOCentro1 = 0.8
percentDistAteOCentro2 = 0.8

PlotarRegioes(regioes1, 0.03, 50, percentDistAteOCentro1)
PlotarRegioes(regioes2, 0.03, 50, percentDistAteOCentro2)
PlotarRegioes(regioes3, 0.0001, 50, percentDistAteOCentro1)