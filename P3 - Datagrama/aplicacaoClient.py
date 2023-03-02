#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#####################################################
# Camada Física da Computação
# Carareto
####################################################

import numpy as np
import time

from enlace import *
import command_data as c

def main():
    try:
        print("\nIniciou o main\n")
        com1 = enlace('COM5')
        i = 0
        com1.enable()
        print("\nAbriu a comunicação\n")
        
        # Byte de sacrifício
        com1.enable()
        print(i);i = 1
        time.sleep(0.2)
        print(i);i = 2
        com1.sendData(b'00')
        time.sleep(1)

        # Handshake
        head = c.d_h0['handshake'] + b'\x00\x00' + b'\x01' + b'\x01' + b'\x01'+ b'\x00\x00\x00\x00\x00\x00'
        command = c.commands[1]

        txBuffer = head + command + c.commands[-1]
        
        lista_comandos = c.sorteia()
        for comando in lista_comandos:
            txBuffer += bytes([len(c.dic_comands[comando])])
            txBuffer += c.dic_comands[comando]
            time.sleep(0.02)
        txBuffer += bytes([11])
        
        print(txBuffer)
        print("meu array de bytes tem tamanho {}" .format(len(txBuffer)))
        #faça aqui uma conferência do tamanho do seu txBuffer, ou seja, quantos bytes serão enviados.
        
        
        #finalmente vamos transmitir os todos. Para isso usamos a funçao sendData que é um método da camada enlace.
        #faça um print para avisar que a transmissão vai começar.
        #tente entender como o método send funciona!
        #Cuidado! Apenas trasmita arrays de bytes!
        
        com1.sendData(np.asarray(txBuffer))  #as array apenas como boa pratica para casos de ter uma outra forma de dados
        
        # A camada enlace possui uma camada inferior, TX possui um método para conhecermos o status da transmissão
        # O método não deve estar fincionando quando usado como abaixo. deve estar retornando zero. Tente entender como esse método funciona e faça-o funcionar.
        txSize = com1.tx.getStatus()
        print('enviou = {}' .format(txSize))
        
        #Agora vamos iniciar a recepção dos dados. Se algo chegou ao RX, deve estar automaticamente guardado
        #Observe o que faz a rotina dentro do thread RX
        #print um aviso de que a recepção vai começar.
        
        
        #Será que todos os bytes enviados estão realmente guardadas? Será que conseguimos verificar?
        #Veja o que faz a funcao do enlaceRX  getBufferLen
      
        #acesso aos bytes recebidos
        txLen = len(txBuffer)
        rxBuffer, nRx = com1.getData(txLen)
        print("recebeu {} bytes" .format(len(rxBuffer)))
        
        for i in range(len(rxBuffer)):
            print("recebeu {}" .format(rxBuffer[i]))
        

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
