def plotMosaico(fig, axs, title, labelx, labely, pos, regs, enquadro):
    for reg in regs:
        axs[pos].plot(reg.x, reg.y, color=reg.cor, label=reg.label)
        axs[pos].scatter(reg.x[-1],reg.y[-1],s=20,facecolor='C0',edgecolor='k')
        axs[pos].annotate(reg.limite, xy=(reg.x[-1], reg.y[-1]), xytext=(reg.x[-1] + 5, reg.y[-1] - 100000),
                               arrowprops=dict(facecolor='black', shrink=0.1))
    axs[pos].grid(True)
    axs[pos].set_xlabel(labelx)
    axs[pos].set_ylabel(labely)
    axs[pos].set_title(title)
    axs[pos].axis(enquadro)
    axs[pos].legend()
