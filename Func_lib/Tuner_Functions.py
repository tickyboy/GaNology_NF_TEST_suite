import telnetlib


def SourceTuner_connect():
    global SourceTuner
    try:
        SourceTuner = telnetlib.Telnet('10.0.0.2')
        SourceTuner.read_until(b'Result')
    except Exception as e:
        print('SourceTuner connect error  ' + str(e) + '\n')
        exit(-1)

def LoadTuner_connect():
    global LoadTuner
    try:
        LoadTuner = telnetlib.Telnet('10.0.0.1')
        LoadTuner.read_until(b'Result')
    except Exception as e:
        print('LoadTuner connect error  ' + str(e) + '\n')
        exit(-1)



#Tuner初始化
def SourceTuner_RST():
    try:
        SourceTuner.write(b'INIT\n')
        SourceTuner.read_until(b'completed')
    except Exception as e:
        print('SourceTuner RST error  ' + str(e) + '\n')
        exit(-1)

def LoadTuner_RST():
    try:
        LoadTuner.write(b'INIT\n')
        LoadTuner.read_until(b'completed')
    except Exception as e:
        print('LoadTuner RST error  ' + str(e) + '\n')
        exit(-1)




#将Tuner调至某个阻抗点
def SourceTuner_ToPoint(point):
    try:
        SourceTuner.write(b'CALPOINT ' + str(point).encode('ascii') + b'\n')
        SourceTuner.read_until(b'completed')
    except Exception as e:
        print('SourceTuner ToPoint error  ' + str(e) + '\n')
        exit(-1)


def LoadTuner_ToPoint(point):
    try:
        LoadTuner.write(b'POS?\n')
        LoadTuner.read_until(b'A3=')
        pos = LoadTuner.read_very_eager().decode('UTF-8')
        i = 0
        a = ''
        while pos[i].isdigit() == True:
            a = a + pos[i]
            i = i + 1
        if a != '34000':
            LoadTuner.write(b'POS 3 34000\n')
            LoadTuner.read_until(b'completed')
        LoadTuner.write(b'CALPOINT ' + str(point).encode('ascii') + b'\n')
        LoadTuner.read_until(b'completed')
    except Exception as e:
        print('LoadTuner ToPoint error  ' + str(e) + '\n')
        exit(-1)

def SourceTuner_Toxy(x, y):
    try:
        SourceTuner.write(b'POS 1 ' + x.encode('ascii') + b' 2 ' + y.encode('ascii') + b'\n')
        SourceTuner.read_until(b'completed')
    except Exception as e:
        print('SourceTuner toxy error  ' + str(e) + '\n')
        exit(-1)



def LoadTuner_3Tomax():
    try:
        LoadTuner.write(b'POS?\n')
        LoadTuner.read_until(b'A3=')
        pos = LoadTuner.read_very_eager().decode('UTF-8')
        i = 0
        a = ''
        while pos[i].isdigit() == True:
            a = a + pos[i]
            i = i + 1
        if a != '34000':
            LoadTuner.write(b'POS 3 34000\n')
            LoadTuner.read_until(b'completed')
    except Exception as e:
        print('LoadTuner 3Tomax error  ' + str(e) + '\n')
        exit(-1)


def LoadTuner_Toxy(x, y):
    try:
        LoadTuner.write(b'POS 1 ' + x.encode('ascii') + b' 7 ' + y.encode('ascii') + b'\n')
        LoadTuner.read_until(b'completed')
    except Exception as e:
        print('LoadTuner Toxy error  ' + str(e) + '\n')
        exit(-1)