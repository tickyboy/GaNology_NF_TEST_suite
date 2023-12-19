import math, os, time, csv
import numpy as np
from scipy import optimize
from Func_lib.Tuner_Functions import *
from Func_lib.FSV3030_Functions import *
from Func_lib.E36311A_Functions import *
from Func_lib.ZNB40_Functions import *
from Func_lib.S_paras_cal import *
from Func_lib.Plot_Functions import *

def SetFre(fre_start, fre_stop, fre_step):
    fre = []
    f = int(fre_start)
    while(f <= int(fre_stop)):
        fre.append(f)
        f = f + int(fre_step)
    return fre


def fit_noise_equation(gams_real, gams_image, nf):
    gam_s = (np.array(gams_real), np.array(gams_image))
    nf = np.array(nf)
    def noise_equation(x, rn, opt_real, opt_imag, nf_min):
        return nf_min + 4 * rn / 50 * (abs(x[0] + 1j * x[1] - opt_real - 1j * opt_imag) ** 2) / (
                    1 - abs(x[0] + 1j * x[1]) ** 2) / abs(1 + opt_real + 1j * opt_imag) ** 2

    init_paras = np.array([1000, 0.8, 0.4, 5])
    paras = optimize.curve_fit(noise_equation, gam_s, nf, p0=init_paras)
    return paras[0]




def get_Sparas_fromS2p(fre, file):
    f = open(file, 'r')
    for i in range(0, 5):
        f.readline()
    s_txt = []
    s_paras = []
    fre_num = len(fre)
    n = 0
    while True:
        line = f.readline()
        if line =='':
            break
        data = re.findall(r"\-?\d+\.?\d*E?\-?\+?\d*", line)
        if int(float(data[0])) in fre:
            s_txt.append([])
            s_paras.append([])
            data[1] = round(math.pow(10, float(data[1]) / 20), 5)
            data[3] = round(math.pow(10, float(data[3]) / 20), 5)
            data[5] = round(math.pow(10, float(data[5]) / 20), 5)
            data[7] = round(math.pow(10, float(data[7]) / 20), 5)
            data[2] = round(float(data[2]), 2)
            data[4] = round(float(data[4]), 2)
            data[6] = round(float(data[6]), 2)
            data[8] = round(float(data[8]), 2)
            s11 = complex(data[1] * math.cos(data[2] / 360 * 2 * np.pi), data[1] * math.sin(data[2] / 360 * 2 * np.pi))
            s12 = complex(data[5] * math.cos(data[6] / 360 * 2 * np.pi), data[5] * math.sin(data[6] / 360 * 2 * np.pi))
            s21 = complex(data[3] * math.cos(data[4] / 360 * 2 * np.pi), data[3] * math.sin(data[4] / 360 * 2 * np.pi))
            s22 = complex(data[7] * math.cos(data[8] / 360 * 2 * np.pi), data[7] * math.sin(data[8] / 360 * 2 * np.pi))
            s_paras[n] = [s11, s12, s21, s22]
            s_txt[n] = [str(data[1]), str(data[2]), str(data[5]), str(data[6]), str(data[3]), str(data[4]),
                        str(data[7]), str(data[8])]
            n = n + 1
        if n == fre_num:
            break
    f.close()
    return s_txt, s_paras



def create_dir(fre, file):
    folder = './ResultFile_lib/' + str(time.localtime().tm_year) + '-' + str(
        time.localtime().tm_mon) + '-' + str(time.localtime().tm_mday)
    if not os.path.exists(folder):
        os.makedirs(folder)
    file = file[:-4]
    i = -1
    while file[i] != '/':
        i = i - 1
    bias = file[i:]
    file = file[:i]
    i = -1
    while file[i] != '/':
        i = i - 1
    name = file[i:]
    folder = folder + name
    if not os.path.exists(folder):
        os.makedirs(folder)
    folder = folder + bias
    if not os.path.exists(folder):
        os.makedirs(folder)
    fre_num = len(fre)
    for i in range(0, fre_num):
        n = folder + '/' + str(fre[i] / 1000000000) + 'GHz'
        if not os.path.exists(n):
            os.makedirs(n)
    return folder + '/'


def Plot_Smith(p1_x, p1_y, p2_x, p2_y, x_match, y_match, title, file_path):
    fig, ax = plt.subplots(figsize=(10, 10))
    circle = plt.Circle((0, 0), 1, fill=False, color='black', linestyle='solid')
    ax.add_artist(circle)
    ax.plot([-1, 1], [0, 0], color='gray', linestyle='dashed')  # 实部轴
    ax.plot([0, 0], [-1, 1], color='gray', linestyle='dashed')  # 虚部轴
    ax.plot([0 - np.cos(45 / 360 * 2 * np.pi), np.cos(45 / 360 * 2 * np.pi)],
            [0 - np.sin(45 / 360 * 2 * np.pi), np.sin(45 / 360 * 2 * np.pi)], color='gray', linestyle='dashed')
    ax.plot([0 - np.cos(45 / 360 * 2 * np.pi), np.cos(45 / 360 * 2 * np.pi)],
            [np.sin(45 / 360 * 2 * np.pi), 0 - np.sin(45 / 360 * 2 * np.pi)], color='gray', linestyle='dashed')
    values = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9]
    for r_value in values:
        angle = np.linspace(0, 2 * np.pi, 100)
        x = r_value * np.cos(angle)
        y = r_value * np.sin(angle)
        text_position = (0, r_value)
        text_content = str(r_value)
        ax.text(*text_position, text_content, color='black', fontsize=16, ha='center', va='center')
        ax.plot(x, y, color='gray', linestyle='dashed')
    ax.scatter(p1_x, p1_y, color='purple', label='Instability')
    ax.scatter(p2_x, p2_y, color='gray', label='Stability')
    ax.plot(x_match, y_match, marker='*', linestyle='', markersize=10, color='red', label='Conjugate matching point')
    ax.set_xlim(-1, 1)
    ax.set_ylim(-1, 1)
    ax.set_aspect('equal', adjustable='box')
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_title(title, fontsize=20)
    ax.legend()
    plt.savefig(file_path + '.tif', format='tif')
    plt.show()




def Display_stability_area(fre, file_dut):
    folder = create_dir(fre, file_dut)
    dut_txt, dut_s = get_Sparas_fromS2p(fre, file_dut)
    inbox_txt, inbox_s = get_Sparas_fromS2p(fre, './S-paras_lib/inbox.s2p')
    outbox_txt, outbox_s = get_Sparas_fromS2p(fre, './S-paras_lib/outbox.s2p')
    isolator_txt, isolator_s = get_Sparas_fromS2p(fre, './S-paras_lib/isolator.s2p')
    st = open('./S-paras_lib/SourceTuner.txt', 'r')
    lt = open('./S-paras_lib/LoadTuner.txt', 'r')
    gaml_x = []
    gaml_y = []
    gaml_x2 = []
    gaml_y2 = []
    line_l = []
    lt.readline()
    judge_fre = []
    fre_num = len(fre)
    for i in range(0, fre_num):
        gaml_x.append([])
        gaml_y.append([])
        gaml_x2.append([])
        gaml_y2.append([])
        line_l.append([])
        judge_fre.append(format(fre[i] / 1000000000, '.5f'))

    last_fre = '0'
    i = -1
    while True:
        line = lt.readline()
        if line == '':
            break
        data = re.findall(r"\-?\d+\.?\d*", line)
        if data[0] != '1':
            break
        if data[1] in judge_fre:
            if data[1] != last_fre:
                last_fre = data[1]
                i = i + 1
            lt_s = S_transform(data[5], data[6], data[7], data[8], data[9], data[10], data[11], data[12])
            Γin5 = outbox_s[i][0] + outbox_s[i][1] * outbox_s[i][2] * isolator_s[i][0] / (1 - outbox_s[i][3] * isolator_s[i][0])
            Γin4 = lt_s[0] + lt_s[1] * lt_s[2] * Γin5 / (1 - lt_s[3] * Γin5)
            Γin3 = dut_s[i][0] + dut_s[i][1] * dut_s[i][2] * Γin4 / (1 - dut_s[i][3] * Γin4)
            gamma_l = abs(Γin4)
            angle_l = np.angle(Γin4, False)
            gamma_in = abs(Γin3)
            angle_in = np.angle(Γin3, False)
            line_l[i].append('%-10s%-10s%-10s%-15s%-15s%-15s%-15s' % (
            data[2], data[3], data[4], str(round(gamma_l, 5)), str(round(angle_l / np.pi / 2 * 360, 5)),
            str(round(gamma_in, 5)), str(round(angle_in / np.pi / 2 * 360, 5))))
            if gamma_in < 1:
                gaml_x[i].append(gamma_l * np.cos(angle_l))
                gaml_y[i].append(gamma_l * np.sin(angle_l))
            else:
                gaml_x2[i].append(gamma_l * np.cos(angle_l))
                gaml_y2[i].append(gamma_l * np.sin(angle_l))
    lt.close()
    line_s = []
    gams_x = []
    gams_y = []
    gams_x2 = []
    gams_y2 = []
    st.readline()
    for i in range(0, fre_num):
        gams_x.append([])
        gams_y.append([])
        gams_x2.append([])
        gams_y2.append([])
        line_s.append([])
    last_fre = '0'
    i = -1
    while True:
        line = st.readline()
        if line == '':
            break
        data = re.findall(r"\-?\d+\.?\d*", line)
        if data[1] in judge_fre:
            if data[1] != last_fre:
                last_fre = data[1]
                i = i + 1
            st_s = S_transform(data[5], data[6], data[7], data[8], data[9], data[10], data[11], data[12])
            Γout1 = inbox_s[i][3]
            Γout2 = st_s[3] + st_s[1] * st_s[2] * Γout1 / (1 - st_s[0] * Γout1)
            Γout3 = dut_s[i][3] + dut_s[i][1] * dut_s[i][2] * Γout2 / (1 - dut_s[i][0] * Γout2)
            gamma_s = abs(Γout2)
            angle_s = np.angle(Γout2, False)
            gamma_out = abs(Γout3)
            angle_out = np.angle(Γout3, False)
            line_s[i].append('%-10s%-10s%-10s%-15s%-15s%-15s%-15s' % (
            data[2], data[3], data[4], str(round(gamma_s, 5)), str(round(angle_s / np.pi / 2 * 360, 5)),
            str(round(gamma_out, 5)), str(round(angle_out / np.pi / 2 * 360, 5))))
            if gamma_out < 1:
                gams_x[i].append(gamma_s * np.cos(angle_s))
                gams_y[i].append(gamma_s * np.sin(angle_s))
            else:
                gams_x2[i].append(gamma_s * np.cos(angle_s))
                gams_y2[i].append(gamma_s * np.sin(angle_s))
    st.close()
    i = 0
    while i < fre_num:
        x_match_s = abs(dut_s[i][0]) * np.cos(-1 * np.angle(dut_s[i][0], False))
        y_match_s = abs(dut_s[i][0]) * np.sin(-1 * np.angle(dut_s[i][0], False))
        x_match_l = abs(dut_s[i][3]) * np.cos(-1 * np.angle(dut_s[i][3], False))
        y_match_l = abs(dut_s[i][3]) * np.sin(-1 * np.angle(dut_s[i][3], False))
        fre_str = str(fre[i] / 1000000000)
        Plot_Smith(gams_x2[i], gams_y2[i], gams_x[i], gams_y[i], x_match_s, y_match_s, 'Γs', folder + fre_str + 'GHz/Γs')
        Plot_Smith(gaml_x2[i], gaml_y2[i], gaml_x[i], gaml_y[i], x_match_l, y_match_l, 'Γl', folder + fre_str + 'GHz/Γl')
        f = open(folder + fre_str + 'GHz/gam_s.txt', 'w')
        f.write('The S-parameters of DUT is:\n')
        f.write('%-15s%-15s%-15s%-15s%-15s%-15s%-15s%-15s\n' % (
        'gam:S11', 'ang:S11', 'gam:S12', 'ang:S12', 'gam:S21', 'ang:S21', 'gam:S22', 'ang:S22'))
        f.write('%-15s%-15s%-15s%-15s%-15s%-15s%-15s%-15s\n\n' % (
        dut_txt[i][0], dut_txt[i][1], dut_txt[i][2], dut_txt[i][3], dut_txt[i][4], dut_txt[i][5], dut_txt[i][6],
        dut_txt[i][7]))
        f.write('%-10s%-10s%-10s%-15s%-15s%-15s%-15s\n' % ('Pt', 'X', 'Y', 'gamma_s', 'angle', 'gamma_in', 'angle'))
        s = '\n'.join(line_s[i])
        f.write(s)
        f.close()
        f = open(folder + fre_str + 'GHz/gam_l.txt', 'w')
        f.write('The S-parameters of DUT is:\n')
        f.write('%-15s%-15s%-15s%-15s%-15s%-15s%-15s%-15s\n' % (
            'gam:S11', 'ang:S11', 'gam:S12', 'ang:S12', 'gam:S21', 'ang:S21', 'gam:S22', 'ang:S22'))
        f.write('%-15s%-15s%-15s%-15s%-15s%-15s%-15s%-15s\n\n' % (
            dut_txt[i][0], dut_txt[i][1], dut_txt[i][2], dut_txt[i][3], dut_txt[i][4], dut_txt[i][5], dut_txt[i][6],
            dut_txt[i][7]))
        f.write('%-10s%-10s%-10s%-15s%-15s%-15s%-15s\n' % ('Pt', 'X', 'Y', 'gamma_l', 'angle', 'gamma_out', 'angle'))
        s = '\n'.join(line_l[i])
        f.write(s)
        f.close()
        i = i + 1




def Measure_DUT_Spara(start, stop, step, vd, id, dut_name):
    DC_supply_connect()
    DC_supply_RST()
    ZNB40_connect()
    if step < 0 or stop > 6 or (start * stop) < 0:
        print('Vg error')
        exit(-1)
    if start < 0:
        port = '3'
    else:
        port = '1'
    folder = './S-paras_lib/DUT' + str(time.localtime().tm_year) + '-' + str(
        time.localtime().tm_mon) + '-' + str(time.localtime().tm_mday)
    if not os.path.exists(folder):
        os.makedirs(folder)
    folder = folder + '/' + dut_name
    if not os.path.exists(folder):
        os.makedirs(folder)
    DC_on(port)
    DC_on('2')
    vg = start
    while vg < (stop + 0.01):
        DC_setVI(port, str(vg), '0.003')
        DC_setVI('2', str(vd), str(id))
        time.sleep(1.5)
        ZNB40_readfile_DutSpara(folder + '/G' + str(float(vg)) + 'D' + str(vd) + '.s2p')
        vg = vg + step
    DC_off('2')
    DC_off(port)


def Tuner_ScanRegion(Pt, fre, region, file_dut):
    folder = create_dir(fre, file_dut)
    dut_txt, dut_s = get_Sparas_fromS2p(fre, file_dut)
    inbox_txt, inbox_s = get_Sparas_fromS2p(fre, './S-paras_lib/inbox.s2p')
    outbox_txt, outbox_s = get_Sparas_fromS2p(fre, './S-paras_lib/outbox.s2p')
    lt = open('./S-paras_lib/LoadTuner.txt', 'r')
    FSV3030_connect()
    SourceTuner_connect()
    LoadTuner_connect()
    LoadTuner_3Tomax()
    judge_fre = []
    fre_num = len(fre)
    for i in range(0, fre_num):
        judge_fre.append(format(fre[i] / 1000000000, '.5f'))
    lt.readline()
    lt_s = []
    while True:
        line = lt.readline()
        if line == '':
            break
        data = re.findall(r"\-?\d+\.?\d*", line)
        if data[0] != '1':
            break
        if data[2] == Pt and data[1] in judge_fre:
            pt_x = data[3]
            pt_y = data[4]
            lt_s.append(S_transform(data[5], data[6], data[7], data[8], data[9], data[10], data[11], data[12]))
    LoadTuner_Toxy(pt_x, pt_y)
    lt.close()

    points = []
    points_line = []
    f = open(folder + str(fre[0] / 1000000000) + 'GHz/gam_s.txt', 'r')
    for n in range(0, 5):
        f.readline()
    while True:
        line = f.readline()
        if line == '':
            break
        data = re.findall(r"\-?\d+\.?\d*", line)
        if region[0] < float(data[3]) < region[1] and region[2] < float(data[4]) < region[3]:
            points.append(data[0])
            points_line.append('%-10s%-10s%-10s' % (data[0], data[1], data[2]))
    f.close()
    points_num = len(points_line)

    pt_last = 0
    st = open('./S-paras_lib/SourceTuner.txt', 'r')
    st.readline()
    i = 0
    lines = [[]]
    while True:
        line = st.readline()
        if line == '':
            break
        data = re.findall(r"\-?\d+\.?\d*", line)
        if data[1] in judge_fre and data[2] in points:
            if float(data[2]) < pt_last:
                i = i + 1
                lines.append([])
            lines[i].append(
                data[5] + '&' + data[6] + '&' + data[7] + '&' + data[8] + '&' + data[9] + '&' + data[10] + '&' + data[
                    11] + '&' + data[12])
            pt_last = float(data[2])
    st.close()
    line_write = []
    for i in range(0, fre_num):
        line_write.append([])
    for j in range(0, points_num):
        data = re.findall(r"\-?\d+\.?\d*", points_line[j])
        SourceTuner_Toxy(data[1], data[2])
        FSV3030_INITsingle()
        gain = FSV3030_ReadGAIN()
        nf = FSV3030_ReadNF()

        if fre_num > 1 and len(nf) != fre_num:
            print('fre_num error!')
            exit(-1)

        for i in range(0, fre_num):
            data = re.findall(r"\-?\d+\.?\d*", lines[i][j])
            st_s = S_transform(data[0], data[1], data[2], data[3], data[4], data[5], data[6], data[7])
            NF_dut, Gain_dut = cal_dut_FG(float(nf[i]), float(gain[i]), inbox_s[i], st_s, dut_s[i], lt_s[i],
                                          outbox_s[i])
            line_write[i].append(points_line[j] + '%-15s%-15s%-15s%-15s' % (NF_dut, Gain_dut, nf[i], gain[i]))
            print(points_line[j] + '%-15s%-20s%-20s%-25s%-20s' % (
            str(fre[i] / 1000000000) + 'GHz', 'nf: ' + NF_dut, 'gain: ' + Gain_dut, 'nf_corr:' + nf[i],
            'G_ins: ' + gain[i]))

    for i in range(0, fre_num):
        f = open(folder + str(fre[i] / 1000000000) + 'GHz/gam_s.txt', 'r')
        j = 0
        for n in range(0, 5):
            f.readline()
        while True:
            line = f.readline()
            if line == '':
                break
            data = re.findall(r"\-?\d+\.?\d*", line)
            if data[0] in points:
                line_write[i][j] = line_write[i][j] + '%-15s%-15s' % (data[3], data[4])
                j = j + 1
        f.close()
        file = folder + str(fre[i] / 1000000000) + 'GHz/NF.txt'
        f = open(file, 'w')
        f.write('%-10s%-10s%-10s%-15s%-15s%-15s%-15s%-15s%-15s\n' % (
                'Pt(L' + Pt + ')', 'X', 'Y', 'NF(dB)', 'GAIN(dB)', 'NFcorr(dB)', 'Gins(dB)', 'gams', 'angle'))
        s = '\n'.join(line_write[i])
        f.write(s)
        f.close()











def Show_NF_smith(file, gap, diff, circle_num, max_db):
    f = open(file, 'r')
    f.readline()
    nf_min = 10
    bad_points_x = []
    bad_points_y = []
    gam_s_real = []
    gam_s_image = []
    nf = []
    while True:
        line = f.readline()
        if line == '':
            break
        data = re.findall(r"\-?\d+\.?\d*", line)
        data[3] = float(data[3])
        data[7] = float(data[7])
        data[8] = float(data[8]) / 360 * 2 * np.pi
        if data[3] < 0 or data[5] == '9.9099995' or data[6] == '9.9099995':
            bad_points_x.append(data[7] * np.cos(data[8]))
            bad_points_y.append(data[7] * np.sin(data[8]))
            continue
        if 0 < data[3] < max_db:
            nf.append(math.pow(10, data[3] / 10))
            gam_s_real.append(data[7] * math.cos(data[8]))
            gam_s_image.append(data[7] * math.sin(data[8]))
        if data[3] < nf_min:
            nf_min = data[3]
    f.seek(0)
    f.readline()
    region_low = []
    region_high = []
    nf_circle_x = []
    nf_circle_y = []
    paras = fit_noise_equation(gam_s_real, gam_s_image, nf)
    j = nf_min
    center_x = []
    center_y = []
    fit_real = []
    fit_imag = []
    data_real = []
    data_imag = []
    radius = []
    for i in range(0, circle_num):
        region_low.append(j - diff)
        region_high.append(j + diff)
        nf_circle_x.append([])
        nf_circle_y.append([])
        fit_real.append([])
        fit_imag.append([])
        data_real.append([])
        data_imag.append([])
        if i == 0:
            n = 0
        else:
            n = (math.pow(10, j / 10) - paras[3]) / (4 * paras[0] / 50) * abs(1 + paras[1] + 1j * paras[2]) ** 2
        c = (paras[1] + 1j * paras[2]) / (n + 1)
        if i == 0:
            r = 0.01
        else:
            r = math.sqrt(n * (n + 1 - abs(paras[1] + 1j * paras[2]) ** 2)) / (n + 1)
        center_x.append(c.real)
        center_y.append(c.imag)
        radius.append(r)
        theta = np.linspace(0, 2*np.pi, 100)
        x = c.real + r * np.cos(theta)
        y = c.imag + r * np.sin(theta)
        gam = x + 1j * y
        z = (1 + gam) / (1 - gam)
        for a in range(0, 100):
            fit_real[i].append(z[a].real)
            fit_imag[i].append(z[a].imag)
        j = j + gap
    distance = 2


    while True:
        line = f.readline()
        if line == '':
            break
        data = re.findall(r"\-?\d+\.?\d*", line)
        real = float(data[7]) * np.cos(float(data[8]) / 360 * 2 * np.pi)
        image = float(data[7]) * np.sin(float(data[8]) / 360 * 2 * np.pi)
        dis = abs(paras[1] + 1j * paras[2] - real - 1j * image)
        if dis < distance:
            distance = dis
            G_fmin = str(round(float(data[4]), 2))
        for i in range(0, circle_num):
            if region_low[i] < float(data[3]) < region_high[i]:
                nf_circle_x[i].append(real)
                nf_circle_y[i].append(image)
                gam = real + 1j * image
                z = (1 + gam) / (1 - gam)
                data_real[i].append(z.real)
                data_imag[i].append(z.imag)
    fig, ax = plt.subplots(figsize=(10, 10))
    circle = plt.Circle((0, 0), 1, fill=False, color='black', linestyle='solid')
    ax.add_artist(circle)
    ax.plot([-1, 1], [0, 0], color='gray', linestyle='dashed')  # 实部轴
    ax.plot([0, 0], [-1, 1], color='gray', linestyle='dashed')  # 虚部轴
    ax.plot([0 - np.cos(45 / 360 * 2 * np.pi), np.cos(45 / 360 * 2 * np.pi)],
            [0 - np.sin(45 / 360 * 2 * np.pi), np.sin(45 / 360 * 2 * np.pi)], color='gray', linestyle='dashed')
    ax.plot([0 - np.cos(45 / 360 * 2 * np.pi), np.cos(45 / 360 * 2 * np.pi)],
            [np.sin(45 / 360 * 2 * np.pi), 0 - np.sin(45 / 360 * 2 * np.pi)], color='gray', linestyle='dashed')
    values = [0.2, 0.4, 0.6, 0.8]
    for r_value in values:
        angle = np.linspace(0, 2 * np.pi, 100)
        x = r_value * np.cos(angle)
        y = r_value * np.sin(angle)
        text_position = (0, r_value)
        text_content = str(r_value)
        ax.text(*text_position, text_content, color='black', fontsize=16, ha='center', va='center')
        ax.plot(x, y, color='gray', linestyle='dashed')
    # 在Smith图上绘制一系列点
    print(paras)
    text_position = (-0.2, -1.1)
    text_content = 'Rn = ' + str(round(paras[0], 2))
    ax.text(*text_position, text_content, color='red', fontsize=22)
    text_position = (0.4, -1.1)
    text_content = 'G = ' + G_fmin
    ax.text(*text_position, text_content, color='red', fontsize=22)
    text_position = (-0.9, -1.2)
    real = str(round(paras[1], 2))
    image = str(round(paras[2], 2))
    gam = str(round(abs(paras[1] + 1j * paras[2]), 2))
    angle = str(round(np.angle(paras[1] + 1j * paras[2], True), 2))
    text_content = 'gam_opt = ' + real + '+' + image + 'j' + '  /  ' + gam + ',  ' + angle + 'deg'
    ax.text(*text_position, text_content, color='red', fontsize=22)
    text_position = (-0.9, -1.1)
    text_content = 'NFmin = ' + str(round(math.log10(paras[3]) * 10, 2))
    ax.text(*text_position, text_content, color='red', fontsize=22)
    ax.scatter(bad_points_x, bad_points_y, color='purple', label='Bad points')
    x = round(nf_min, 2)
    for i in range(0, circle_num):
        ax.scatter(nf_circle_x[i], nf_circle_y[i], color='gray', label=str(x))
        x = round(x + gap, 2)
        circle = plt.Circle((center_x[i], center_y[i]), radius=radius[i], color='red', fill=False)
        ax.add_patch(circle)
    #ax.plot(min_x, min_y, marker='*', linestyle='', markersize=10, color='red', label='NFmin')
    # 设置坐标轴属性
    ax.set_xlim(-1, 1)
    ax.set_ylim(-1, 1)
    ax.set_aspect('equal', adjustable='box')
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_title('NF circle', fontsize=20)
    ax.legend()
    plt.savefig(file[:-4] + '.tif', format='tif')
    plt.show()

    nf_min = round(nf_min, 2)
    title = []
    max_len = 100
    for i in range(0, circle_num):
        title.append('Mag(' + str(nf_min) + ')')
        title.append('Angle(' + str(nf_min) + ')')
        title.append('fit_Mag(' + str(nf_min) + ')')
        title.append('fit_Angle(' + str(nf_min) + ')')
        nf_min = nf_min + gap
        if len(data_real[i]) > max_len:
            max_len = len(data_real[i])
    for i in range(0, circle_num):
        data_real[i] += [''] * (max_len - len(data_real[i]))
        data_imag[i] += [''] * (max_len - len(data_imag[i]))
        fit_real[i] += [''] * (max_len - len(fit_real[i]))
        fit_imag[i] += [''] * (max_len - len(fit_imag[i]))
    with open(file[:-6] + 'Plot datas.csv', 'w', newline='') as f:
        csv_writer = csv.writer(f)
        csv_writer.writerow(title)
        for i in range(0, max_len):
            data = []
            for j in range(0, circle_num):
                data += [data_real[j][i]]
                data += [data_imag[j][i]]
                data += [fit_real[j][i]]
                data += [fit_imag[j][i]]
            csv_writer.writerow(data)

