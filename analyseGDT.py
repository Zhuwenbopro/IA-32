arr_l = ['0x0000ffff', '0x7c0001ff', '0x7c0001ff', '0x7c00fffe']
arr_h = ['0x00cf9200', '0x00409800', '0x00409200', '0x00cf9600']


def bin2hex(bin_str, opt=0):
    res = hex(int(bin_str, 2))[2:]
    if opt == 0:
        return res
    else:
        for i in range(opt - len(res)):
            res = '0' + res
        return res


def hex2bin(hex_str, opt=0):
    res = bin(int(hex_str, 16))[2:]
    if opt == 0:
        return res
    else:
        for i in range(opt - len(res)):
            res = '0' + res
        return res


def analise(str_h, str_l):
    str_hb = hex2bin(str_h, 32)[::-1]
    str_lb = hex2bin(str_l, 32)[::-1]

    base_addr = bin2hex((str_lb[16:] + str_hb[0:8] + str_hb[24:])[::-1], 8)
    limit = bin2hex((str_lb[0:16] + str_hb[16:20])[::-1], 8)
    G = str_hb[23]
    S = str_hb[12]
    DLP = int(str_hb[13:15][::-1], 2)
    P = str_hb[15]
    TYPE = str_hb[8:12]

    print(f'基地址为: {base_addr}')
    print(f'段界限为: {limit}')
    if G == '0':
        print('颗粒的大小 1 Byte (G=0)')
    elif G == '1':
        print('颗粒的大小 4 KB   (G=0)')

    if S == '0':
        print('系统段           (S=0)')
    elif S == '1':
        print('代码段或数据段     (S=1)')
    print(f'优先级           DLP={DLP}')
    if P == '0':
        print('段不在内存中       (P=0)')
    elif P == '1':
        print('段在内存中        (P=1)')
    if S == '1':
        s_code = '如果是代码段： '
        s_data = '如果是数据段： '
        if TYPE[1] == '1':
            s_code = s_code + '执行、可读 '
            s_data = s_data + '可读、可写 '
        elif TYPE[1] == '0':
            s_code = s_code + '只执行 '
            s_data = s_data + '只读 '
        if TYPE[2] == '1':
            s_code = s_code + ''
            s_data = s_data + '段向低地址扩展'
        elif TYPE[2] == '0':
            s_code = s_code + ''
            s_data = s_data + '段向高地址扩展'
        print(s_code)
        print(s_data)


for i in range(len(arr_l)):
    str_l = arr_l[i]
    str_h = arr_h[i]
    analise(str_h, str_l)
    print()
    print()
