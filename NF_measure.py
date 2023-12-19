import math


from Func_lib.NF_mea_Functions import *
import numpy as np

if __name__ == '__main__':

    file_dut = './S-paras_lib/DUT/2023-11-27/NO1RS_3F_good/G2.0D6.txt'
    file_nf = './ResultFile_lib/2023-12-18/P-Gate/G3.0D10.0/2.0GHz/NF.txt'
    fre = SetFre(2E9, 5E9, 0.5E9)
    region = [0.5, 0.6, 0, 30]

    #Measure_DUT_Spara(1, 5, 0.5, 6, 0.04, 'NO1RS_9F')
    #Display_stability_area(fre, file_dut)
    #Tuner_ScanRegion('1', fre, region, file_dut)
    #Show_NF_smith(file_nf, 2, 0.2, 9, 15)
    