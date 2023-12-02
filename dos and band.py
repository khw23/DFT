import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.pyplot import MultipleLocator

def plot_dos():
    data_Mo = np.loadtxt('path')
    data_S = np.loadtxt('path')
    #data_* = np.loadtxt('path')
    data = np.loadtxt('path')
    plt.figure(figsize=(7, 7), dpi=100)
    plt.plot(data_O[:, 0], data_O[:, 4])
    plt.plot(data_K[:, 0], data_K[:, 4])
    plt.plot(data_Cr[:, 0], data_Cr[:, 4])
    plt.plot(data[:, 0], data[:, 1], c='black', linewidth=1.5)
    plt.show()

def x_set():
    file = open('E:/雁栖湖国科大/DFT上机/能带/xiao/KLABELS')
    f1 = file.readline()
    x_label = []
    x_loca = []
    for i in range(4):
        f2 = file.readline()
        t1, t2 = [str(x) for x in f2.strip().split()]
        x_label.append(t1)
        x_loca.append(float(t2))
    print(x_label)
    print(x_loca)
    return x_label, x_loca


def dos_data():
    file = open('E:/雁栖湖国科大/DFT上机/dos/DOSCAR')
    f1 = file.readline()
    f2 = file.readline()
    f3 = file.readline()
    f4 = file.readline()
    f5 = file.readline()
    f6 = file.readline()
    f6 = [float(x) for x in f6.strip().split()]  # 存储第六行信息(Emin,Emax,n_dos,E-fermi）
    val = np.zeros((int(f6[2]), 2), dtype=float)  # 存储dos值
    efermi = f6[3]
    print(efermi)

    for i in range(val.shape[0]):  # 读取所有k点
        temp1 = file.readline()
        temp2 = [float(x) for x in temp1.strip().split()]
        for j in range(2):
            if j == 0:
                val[i, j] = temp2[j] - efermi
            else: val[i, j] = temp2[j]
    return val, efermi


def plot_band():
    file = open('E:/雁栖湖国科大/DFT上机/能带/xiao/EIGENVAL')
    f1 = file.readline()
    f2 = file.readline()
    f3 = file.readline()
    f4 = file.readline()
    system = file.readline()
    f6 = file.readline()
    f6 = [int(x) for x in f6.strip().split()] #存储第六行信息(价电子数，k点数，能带数）

    val = np.zeros((f6[1], f6[2]), dtype=float) #存储k点上每条能带本征值
    klist = []

    for i in range(f6[1]): #读取所有k点
        f7 = file.readline()
        f8 = file.readline()
        klist.append(f8)
        for j in range(f6[2]):
            temp1 = file.readline()
            temp1 = [float(x) for x in temp1.strip().split()]
            val[i, j] = temp1[1]

    dos, efermi = dos_data()

    for i in range(0, f6[2]):
        val[:, i] = val[:, i]-efermi

    x_num = np.arange(0, len(val[:, 0]), 1)
    label, loca = x_set()
    x_label = []
    for i in range(len(loca)-1):
        x_label.append(np.linspace(loca[i], loca[i+1], 20))

    for i in range(len(label)):
        if label[i] == 'GAMMA':
            label[i] = chr(915)

    

    plt.figure(figsize=(7, 7), dpi=100)
    plt.rcParams['ytick.direction'] = 'in'
    plt.rcParams['xtick.direction'] = 'in'
    rext1 = [0.1, 0.1, 0.6, 0.8]
    rext2 = [0.73, 0.1, 0.17, 0.8]
    ax1 = plt.axes(rext1)
    ax2 = plt.axes(rext2)

    for i in range(len(loca)):
        flag = np.zeros([2, 2])
        flag[0, 0], flag[1, 0] = loca[i], loca[i]
        flag[0, 1] = -5
        flag[1, 1] = 8
        ax1.plot(flag[:, 0], flag[:, 1], c='lightgrey', linewidth=1)

    for i in range(0, 3):
        a = i*20
        for j in range(0, f6[2]):
            ax1.plot(x_label[i], val[a:a+20, j], c='black', linewidth=1.5)
    y = [-8,-6,-4, -2, 0, 2, 4, 6,8,10,12]
    ax1.set_xticks(loca, label, fontsize=15)
    ax1.plot([0, 3.068], [0, 0], c='lightgrey', linewidth=1)
    #ax1.set_ylabel("E-E$_f$$_e$$_r$$_m$$_i$(eV)", fontsize=25)
    font_dict = {'family': 'Times New Roman', 'size': 22, 'weight':5}
    ax1.set_ylabel("Energy(eV)", fontdict=font_dict)
    ax1.set_yticks(y, y, fontsize=15)
    ax1.set_ylim([-4, 6])
    ax1.set_xlim([np.min(np.array(loca)), np.max(np.array(loca))])
    ax1.set_title('K$_2$CrO$_4$ Band structure', loc='left', fontdict=font_dict)
    #ax1.set_xlabel('Wave Vector')
    #ax1.patch.set_facecolor('gainsboro')

    '''ax2.plot(data[:, 1], data[:, 0], c='black', linewidth=1.5)
    ax2.plot(data_O[:, 4], data[:, 0], c='lightgrey', linewidth=1.5)
    ax2.plot(data_K[:, 4], data_K[:, 0], c='lightblue', linewidth=1.5)
    ax2.plot(data_Cr[:, 4], data_Cr[:, 0], c='orange', linewidth=1.5)'''
    ax2.plot(dos[:, 1], dos[:, 0], c='black', linewidth=1.5)
    ax2.set_ylim([-4, 6])
    ax2.set_xlim([0, 10])
    ax2.plot([0, 120], [0, 0], c='lightgrey', linewidth=1)
    ax2.yaxis.set_major_locator(MultipleLocator(60))
    font_dict = {'family':'Times New Roman', 'size':22, 'weight':5}
    ax2.set_title('DOS', fontdict=font_dict)
    ax2.set_yticks([])
    #ax2.set_xticks([])
    #ax2.patch.set_facecolor('gainsboro')
    #ax2.set_xlabel('Density of States')
    #plt.subplots_adjust(wspace=0)
    plt.show()

plot_band()