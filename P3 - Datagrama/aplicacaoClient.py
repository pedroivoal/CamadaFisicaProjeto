#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#####################################################
# Camada Física da Computação
# Carareto
####################################################

import numpy as np
import time
from urllib.parse import unquote_plus


from enlace import *
from enlaceRx import RX
import command_data as c

def main():
    print(f"\n\n\n{'='*80}\nIniciou o main")
    com1 = enlace('COM5')
    com1.enable()
    print("Abriu a comunicação")
    
    # Byte de sacrifício
    time.sleep(0.2)
    com1.sendData(b'00')
    time.sleep(1)

    # =======================================================================================
    # ====================================== Handshake ======================================
    # =======================================================================================
    handshake_recebido = False
    while not handshake_recebido:
            
        print("\nHandshake iniciado")
        head = c.d_h0['handshake'] + b'\x00\x00' + b'\x01' + b'\x01' + b'\x01'+ b'\x00\x00\x00\x00\x00\x00'
        command = c.commands[1]
        txBuffer = head + command + c.commands[-1]
        com1.sendData(np.asarray(txBuffer))
        handshake_enviado = True
        print('Handshake eviado\n')

        t0 = time.time()
        while handshake_enviado:
            if com1.rx.getIsEmpty():
                if time.time() - t0 > 3:
                    continuar = input("TIMEOUT, deseja continuar? (s/n) ").strip().upper()
                    if continuar == 'S' or continuar == 'SIM':
                        t0 = time.time()
                        handshake_enviado = False
                    else:
                        handshake_recebido = True
                        handshake_enviado = False

            else:
                head, _ = com1.getData(12)
                if head[0] == 1:
                    payload, _ = com1.getData(1)
                    eof, _ = com1.getData(4)
                    handshake_recebido = True

                    if payload[0] == 2:
                        print("Handshake recebido")
                        print("Clinte está vivo")
                        break
                    else:
                        print("Handshake recebido")
    # =======================================================================================
    # ====================================== Handshake ======================================
    # =======================================================================================

    with open('P3 - Datagrama/Porta.jpg', 'rb') as conteudo:
        binary_image = conteudo.read()
    
    print("Imagem lida")
    print("Tamanho da imagem: {} bytes" .format(len(binary_image)))

    i = 1
    while i <= np.ceil(len(binary_image)/50):        
        
        if len(binary_image) - (i-1)*50 < 50:
            n = len(binary_image) - i*50
            payload = binary_image[(i-1)*50:i*50-n]
            head = b'\x02' + b'\x00\x00' + bytes([int(np.ceil(len(binary_image)/50))]) + bytes([i]) + bytes([50+n]) + b'\x00\x00\x00\x00\x00\x00'
            print(f'tamanho do payload: {50+n}', end=' ')
        else:
            head = b'\x02' + b'\x00\x00' + bytes([int(np.ceil(len(binary_image)/50))]) + bytes([i]) + b'\x32'+ b'\x00\x00\x00\x00\x00\x00'
            payload = binary_image[(i-1)*50:i*50]
            print(f'tamanho do payload: {50}', end=' ')

        # if i == 5:
        #     head = b'\x02' + b'\x00\x00' + bytes([int(np.ceil(len(binary_image)/50))]) + bytes([i+1]) + b'\x32'+ b'\x00\x00\x00\x00\x00\x00'
        # if i == 7:
        #     head = b'\x02' + b'\x00\x00' + bytes([int(np.ceil(len(binary_image)/50))]) + bytes([i]) + b'\x30'+ b'\x00\x00\x00\x00\x00\x00'
            
        txBuffer = head + payload + c.commands[-1]
        time.sleep(0.005)
        com1.sendData(np.asarray(txBuffer))
        print(f'numero do pacote: {i}')
        i += 1

        head, _ = com1.getData(12)
        if head[0] == 1:
            payload, _ = com1.getData(1)
            eof, _ = com1.getData(4)
            print
            if payload[0] == 4:
                print("Arquivo recebido\n")
            elif payload[0] == 5:
                print("Arquivo fora de ordem")
                break
            elif payload[0] == 6:
                print("Arquivo corrompido")
                break
            else:
                print("Arquivo não recebido")
                break


    # for i in range(len(rxBuffer)):
    #     print("recebeu {}" .format(rxBuffer[i]))

    # # Encerra comunicação
    # print("-------------------------")
    # print("Comunicação encerrada")
    # print("-------------------------")
    com1.disable()

    # except Exception as erro:
    #     print("ops! :-\\")
    #     print(erro)
    #     com1.disable()
    
    print('='*80, '\n\n\n')

    #so roda o main quando for executado do terminal ... se for chamado dentro de outro modulo nao roda
if __name__ == "__main__":
    main()
