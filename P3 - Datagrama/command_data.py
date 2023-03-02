from random import randint

def sorteia():
    n = randint(10, 30)
    lista_comandos = []
    for i in range(n):
        a = randint(1, 9)
        lista_comandos.append(a)
    return lista_comandos

dic_comands = {
    1: b'\x01\x00',
    'handshake': b'\x01\x00',
}