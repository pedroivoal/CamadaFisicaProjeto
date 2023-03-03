#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#####################################################
# Camada Física da Computação
# Carareto
####################################################

import numpy as np
import time

from enlace import *
from enlaceRx import RX
import command_data as c

def main():
    print(f"\n\n\n{'='*80}\nIniciou o main")
    com1 = enlace('COM4')
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
    
    head = c.d_h0['handshake'] + b'\x00\x00' + b'\x01' + b'\x01' + b'\x01'+ b'\x00\x00\x00\x00\x00\x00'
    command = c.commands[1]
    txBuffer = head + command + c.commands[-1]
    com1.sendData(np.asarray(txBuffer))
    

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
