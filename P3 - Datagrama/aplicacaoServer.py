#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#####################################################
# Camada Física da Computação
# Carareto 
####################################################

from enlace import *
import time
import numpy as np
import command_data as c

#use uma das 3 opcoes para atribuir à variável a porta usada
#serialName = "/dev/ttyACM0"           # Ubuntu (variacao de)
serialName = "/dev/tty.usbmodem14101" # Mac    (variacao de)
#serialName = "COM3"                  # Windows(variacao de)

def main():
    try:
        print("\nIniciou o main\n")

        com1 = enlace(serialName)
        
        com1.enable()
        print("esperando 1 byte de sacrifício\n")
        rxBuffer, nRx = com1.getData(1)
        com1.rx.clearBuffer()
        time.sleep(.1)  

        print("\nAbriu a comunicação\n")

        n = 1

        while True:
            head, _ = com1.getData(12)
            head_server = head
            print('Recebi o head')

            n_pacotes_total = head[3]
            n_pacote = head[4]
            n_bytes = head[5]

            # HANDSHAKE
            if head[0] == 1:
                print("Handshake iniciado")
                payload, _ = com1.getData(1)
                eof, _ = com1.getData(4)
                if payload[0] == 1:
                    if n > 0:
                        com1.sendData(head + b'\x02' + eof)
                        print("Handshake realizado com sucesso")
                        print('Esperando pacote')
                        time.sleep(1)
                        if not com1.rx.getIsEmpty():
                            break
                    else:
                        n += 1
                        print('erro simulado')
                else:
                    print("Erro no handshake")
                    break

        # PACOTES
        data = b''
        cont = 1
        print("Recebendo pacotes")
        while True:
            head, _ = com1.getData(12)

            n_pacotes_total = head[3]
            n_pacote = head[4]
            n_bytes = head[5]

            print('Recebi o pacote {}/{}'.format(n_pacote, n_pacotes_total))

            if head[0] == 2:
                time.sleep(0.1)
                if com1.rx.getBufferLen() != n_bytes + 4:
                    print("Tamanho do pacote não confere")
                    com1.sendData(head_server + b'\x06' + eof)
                    time.sleep(0.01)
                    break

                payload, _ = com1.getData(n_bytes)
                eof, _ = com1.getData(4)

                if n_pacote == n_pacotes_total:
                    print("Último pacote recebido")
                    break

                if eof == b'\xaa\xbb\xcc\xdd':
                    print("Pacote recebido com sucesso")
                    com1.sendData(head_server + b'\x04' + eof)
                    time.sleep(0.01)

                else:
                    print("Erro no pacote")
                    break
                
                if n_pacote == cont:
                    data += payload
                    cont += 1

                else:
                    print("Pacote fora de ordem")
                    com1.sendData(head_server + b'\x05' + eof)
                    time.sleep(0.01)
                    break
            
        
        img = 'img_recebida.jpg'
        with open(img, 'wb') as f:
            f.write(data)

        # Encerra comunicação
        print("-------------------------")
        print("Comunicação encerrada")
        print("-------------------------")
        com1.disable()         
        
    except Exception as erro:
        print("ops! :-\\")
        print(erro)
        com1.disable()
        

    #so roda o main quando for executado do terminal ... se for chamado dentro de outro modulo nao roda
if __name__ == "__main__":
    main()

