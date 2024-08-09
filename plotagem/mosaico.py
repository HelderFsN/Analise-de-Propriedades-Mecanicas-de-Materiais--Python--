import numpy as np

def plotRegioes(axs, title, labelx, labely, pos, regioes, enquadro, legendaLoc, percentPos, plotarAnguloEModulo):
    for reg in regioes:
        axs[pos].plot(reg.x, reg.y, color=reg.cor, label=reg.label)
        axs[pos].scatter(reg.x[-1],reg.y[-1],s=20,facecolor='C0',edgecolor='k')
        xMeioGrafico = (enquadro[0] + enquadro[1])/2
        yMeioGrafico = (enquadro[2] + enquadro[3])/2
        
        MeioGrafico = np.array((xMeioGrafico,yMeioGrafico))
        pontoLimite = np.array((reg.x[-1],reg.y[-1]))
        vetorMeioGrafico = MeioGrafico-pontoLimite
        if reg.limite == "Ruptura":
            textLimitePos = pontoLimite
        else:
            textLimitePos = pontoLimite + vetorMeioGrafico*percentPos
        if plotarAnguloEModulo:
            axs[pos].annotate(f'{reg.anguloGraus:.4f}°', xy=(reg.x[0], reg.y[0]), xytext=(reg.x[0], reg.y[0]),
                           arrowprops=dict(facecolor='red', shrink=0))
            axs[pos].text(xMeioGrafico, yMeioGrafico, rf'$\epsilon={reg.variacao/1000:.4f}$ GPa',fontsize=15)
        else:
            axs[pos].annotate(reg.limite+f' (${reg.x[-1]:.3f},${reg.y[-1]:.1f})', xy=(pontoLimite[0], pontoLimite[1]), 
                              xytext=(textLimitePos[0], textLimitePos[1]),
                                   arrowprops=dict(facecolor='black', shrink=0.1))
            

    axs[pos].grid(False)
    axs[pos].set_xlabel(labelx)
    axs[pos].set_ylabel(labely)
    axs[pos].set_title(title)
    
    if enquadro:
        axs[pos].axis(enquadro)
        
    axs[pos].legend(loc=legendaLoc)
