#####################################################
# Camada Física da Computação
#Carareto
#11/08/2022
#Aplicação
####################################################


#esta é a camada superior, de aplicação do seu software de comunicação serial UART.
#para acompanhar a execução e identificar erros, construa prints ao longo do código! 


import numpy as np
import time

from enlace import *
import sorteador as sort

# voce deverá descomentar e configurar a porta com através da qual ira fazer comunicaçao
#   para saber a sua porta, execute no terminal :
#   python -m serial.tools.list_ports
# se estiver usando windows, o gerenciador de dispositivos informa a porta

#use uma das 3 opcoes para atribuir à variável a porta usada
#serialName = "/dev/ttyACM0"           # Ubuntu (variacao de)
serialName = "/dev/tty.usbmodem14301" # Mac    (variacao de)
#serialName = "COM3"                  # Windows(variacao de)


def main():
    try:
        print("Iniciou o main")
        #declaramos um objeto do tipo enlace com o nome "com". Essa é a camada inferior à aplicação. Observe que um parametro
        #para declarar esse objeto é o nome da porta.
        com1 = enlace('COM5')
        # Ativa comunicacao. Inicia os threads e a comunicação seiral 
        com1.enable()
        #Se chegamos até aqui, a comunicação foi aberta com sucesso. Faça um print para informar.
        print("Abriu a comunicação")
        
        time.sleep(0.2)
        com1.sendData(b'00')
        time.sleep(1)
        
        numero_de_comandos_enviados = 0
        #isso é um array de bytes
        
        #aqui você deverá gerar os dados a serem transmitidos. 
        #seus dados a serem transmitidos são um array bytes a serem transmitidos. Gere esta lista com o 
        #nome de txBuffer. Esla sempre irá armazenar os dados a serem enviados.
        lista_comandos = sort.sorteia()
        for comando in lista_comandos:
            txBuffer = bytes([len(sort.dic_comands[comando])])
            print(txBuffer)
            # print("meu array de bytes tem tamanho {}" .format(len(txBuffer)))
            #faça aqui uma conferência do tamanho do seu txBuffer, ou seja, quantos bytes serão enviados.
            
            #finalmente vamos transmitir os todos. Para isso usamos a funçao sendData que é um método da camada enlace.
            #faça um print para avisar que a transmissão vai começar.
            #tente entender como o método send funciona!
            #Cuidado! Apenas trasmita arrays de bytes!

            com1.sendData(np.asarray(txBuffer))  #as array apenas como boa pratica para casos de ter uma outra forma de dados
            # com1.sendData(b'\x09')  #as array apenas como boa pratica para casos de ter uma outra forma de dados

            # A camada enlace possui uma camada inferior, TX possui um método para conhecermos o status da transmissão
            # O método não deve estar fincionando quando usado como abaixo. deve estar retornando zero. Tente entender como esse método funciona e faça-o funcionar.
            txSize = com1.tx.getStatus()
            # print('enviou = {}'.format(txSize))
            time.sleep(0.05)

            txBuffer = sort.dic_comands[comando]
            com1.sendData(np.asarray(txBuffer))  #as array apenas como boa pratica para casos de ter uma outra forma de dados
            numero_de_comandos_enviados += 1

            # A camada enlace possui uma camada inferior, TX possui um método para conhecermos o status da transmissão
            # O método não deve estar fincionando quando usado como abaixo. deve estar retornando zero. Tente entender como esse método funciona e faça-o funcionar.
            txSize = com1.tx.getStatus()
            print(txBuffer, end='\n\n')
            # print('enviou = {}'.format(txSize))
            time.sleep(0.05)

        txBuffer = bytes([11]) # indica o fim da transmissão
        print(txBuffer)
        com1.sendData(np.asarray(txBuffer))  #as array apenas como boa pratica para casos de ter uma outra forma de dados
        time.sleep(0.05)
        
        #Agora vamos iniciar a recepção dos dados. Se algo chegou ao RX, deve estar automaticamente guardado
        #Observe o que faz a rotina dentro do thread RX
        #print um aviso de que a recepção vai começar.
        
        
        #Será que todos os bytes enviados estão realmente guardadas? Será que conseguimos verificar?
        #Veja o que faz a funcao do enlaceRX  getBufferLen

        #acesso aos bytes recebidos
        # while True:
        rxBuffer, nRx = com1.getData(1)
        if int.from_bytes(rxBuffer, byteorder="big") == 0:
            pass
        elif int.from_bytes(rxBuffer, byteorder="big") == numero_de_comandos_enviados:
            print(f'numero de comendos enviados para o servidor: {numero_de_comandos_enviados}')
            print(f'numero de comendos recebidos pelo servidor: {int.from_bytes(rxBuffer, byteorder="big")}')
        else:
            print('\nERRO\nnumero de bytes enviados != numero de bytes recebidos\n')
            print(f'numero de comendos enviados para o servidor: {numero_de_comandos_enviados}')
            print(f'numero de comendos recebidos pelo servidor: {int.from_bytes(rxBuffer, byteorder="big")}')
        # print("recebeu {} bytes" .format(len(rxBuffer)))
        
        for i in range(len(rxBuffer)):
            pass
            # print("recebeu {}" .format(rxBuffer[i]))
        
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
