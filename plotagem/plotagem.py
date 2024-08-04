
def plotMosaico(fig, axs, title, x, y, labelx, labely, pos):
    axs[pos].plot(x, y)
    axs[pos].grid(True)
    axs[pos].set_xlabel(labelx)
    axs[pos].set_ylabel(labely)
    axs[pos].set_title(title)
    pass
def plotGeral(fig, axs, title, labelx, labely, pos, regs):
    for reg in regs:
        axs[pos].plot(reg.x, reg.y, label=reg.label)
        axs[pos].scatter(reg.x[-1],reg.y[-1],s=20,facecolor='C0',edgecolor='k')
        axs[pos].annotate('Limite de Resistência a Tensão', xy=(reg.x[-1], reg.y[-1]), xytext=(reg.x[-1] + 5, reg.y[-1] - 100000),
                               arrowprops=dict(facecolor='black', shrink=0.1))
    axs[pos].grid(True)
    axs[pos].set_xlabel(labelx)
    axs[pos].set_ylabel(labely)
    axs[pos].set_title(title)
    axs[pos].legend()
