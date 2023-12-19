import math
import numpy as np

def S_transform(GammaS11, PhiS11, GammaS12, PhiS12, GammaS21, PhiS21, GammaS22, PhiS22):
    s11 = complex(float(GammaS11) * math.cos(float(PhiS11) / 360 * 2 * math.pi),
                  float(GammaS11) * math.sin(float(PhiS11) / 360 * 2 * math.pi))
    s12 = complex(float(GammaS12) * math.cos(float(PhiS12) / 360 * 2 * math.pi),
                  float(GammaS12) * math.sin(float(PhiS12) / 360 * 2 * math.pi))
    s21 = complex(float(GammaS21) * math.cos(float(PhiS21) / 360 * 2 * math.pi),
                  float(GammaS21) * math.sin(float(PhiS21) / 360 * 2 * math.pi))
    s22 = complex(float(GammaS22) * math.cos(float(PhiS22) / 360 * 2 * math.pi),
                  float(GammaS22) * math.sin(float(PhiS22) / 360 * 2 * math.pi))
    S = [s11, s12, s21, s22]
    return S


#S11 is S[0], S12 is S[1], S21 is S[2], S22 is S[3]
def Available_power_gain(Γs, S):
    Γout = S[3] + S[1] * S[2] * Γs / (1 - S[0] * Γs)
    a = abs(S[2]) * abs(S[2]) * (1 - abs(Γs) * abs(Γs))
    b = abs(1 - S[0] * Γs) * abs(1 - S[0] * Γs) * (1 - abs(Γout) * abs(Γout))
    Ga = a / b
    return Ga


def Power_gain(Γl, S):
    Γin = S[0] + S[1] * S[2] * Γl / (1 - S[3] * Γl)
    a = abs(S[2]) * abs(S[2]) * (1 - abs(Γl) * abs(Γl))
    b = (1 - abs(Γin) * abs(Γin)) * abs(1 - S[3] * Γl) * abs(1 - S[3] * Γl)
    G = a / b
    return G


def Transducer_power_gain(Γs, Γl, S):
    Γin = S[0] + S[1] * S[2] * Γl / (1 - S[3] * Γl)
    a = abs(S[2]) * abs(S[2]) * (1 - abs(Γs) * abs(Γs)) * (1 - abs(Γl) * abs(Γl))
    b = abs(1 - Γin * Γs) * abs(1 - Γin * Γs) * abs(1 - S[3] * Γl) * abs(1 - S[3] * Γl)
    Gt = a / b
    return Gt


def Gain(Γs, S):
    Γin = S[0] + S[1] * S[2] * S[3].conjugate() / (1 - S[3] * S[3].conjugate())
    Γout = S[3] + S[1] * S[2] * Γs / (1 - S[0] * Γs)
    a = abs(S[2])**2 * (1 - abs(Γout)**2)
    b = abs(1 - S[3] * Γout.conjugate())**2 * (1 - abs(Γin)**2)
    G = a / b
    return G

#calculate NF and Gain of DUT.    NF_corr, G_ins is measured by spectrum analyzer
def cal_dut_FG(NF_corr, G_ins, S_bias, S_in, S_dut, S_ou, S_line):
    G_dut = G_ins + loss_dB(S_bias) + loss_dB(S_in) + loss_dB(S_ou) + loss_dB(S_line)
    G_dut = str(round(G_dut, 5))
    F_corr = math.pow(10, NF_corr / 10)
    G_ins = math.pow(10, G_ins / 10)
    Γout1= S_bias[3]
    Gav1 = Available_power_gain(0, S_bias)
    Γout2 = S_in[3] + S_in[1] * S_in[2] * Γout1 / (1 - S_in[0] * Γout1)
    Gav2 = Available_power_gain(Γout1, S_in)
    Gav_dut = Available_power_gain(Γout2, S_dut)
    Gav_inp = Gav1 * Gav2
    F_dut = F_corr * Gav_inp - Gav_inp / G_ins + 1 / Gav_dut
    if F_dut > 0:
        F_dut = str(round(math.log10(F_dut) * 10, 5))
    else:
        F_dut = str(round(F_dut, 5))
    return F_dut, G_dut

def loss_dB(S):
    loss = -10 * math.log10(abs(S[2]) ** 2 / (1 - abs(S[0]) ** 2))
    return loss

