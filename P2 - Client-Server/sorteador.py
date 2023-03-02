from random import randint

def sorteia():
    n = randint(10, 30)
    lista_comandos = []
    for i in range(n):
        a = randint(1, 9)
        lista_comandos.append(a)
    return lista_comandos

dic_comands = {
                1: b'\xa0\x00\x00\x00',
                2: b'\x00\x00\xAA\x00',
                3: b'\xAA\x00\x00',
                4: b'\x00\xAA\x00',
                5: b'\x00\x00\xAA',
                6: b'\x00\xAA',
                7: b'\xAA\x00',
                8: b'\x00',
                9: b'\xFF'
               }
