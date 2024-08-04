def plotMosaico(fig, axs, title, labelx, labely, pos, regioes, enquadro, posText=(0,0), legendaLoc="",textPlot=bool):
    for reg in regioes:
        axs[pos].plot(reg.x, reg.y, color=reg.cor, label=reg.label)
        axs[pos].scatter(reg.x[-1],reg.y[-1],s=20,facecolor='C0',edgecolor='k')
        axs[pos].annotate(reg.limite+f' (${reg.x[-1]:.3f},${reg.y[-1]:.4f})', xy=(reg.x[-1], reg.y[-1]), xytext=(reg.x[-1] + posText[0], reg.y[-1] + posText[1]),
                               arrowprops=dict(facecolor='black', shrink=0.1))
        if textPlot:
            axs[pos].annotate(f'{reg.anguloGraus:.4f}°', xy=(reg.x[0], reg.y[0]), xytext=(reg.x[0]+0.0001, reg.y[0]+0.001),
                           arrowprops=dict(facecolor='red', shrink=0))
            axs[pos].text(reg.x[0]+0.001, reg.y[0]+0.01, f'$\epsilon={reg.variacao:.4f}$',fontsize=15)

    axs[pos].grid(False)
    axs[pos].set_xlabel(labelx)
    axs[pos].set_ylabel(labely)
    axs[pos].set_title(title)
    axs[pos].axis(enquadro)
    axs[pos].legend(loc=legendaLoc)
