commands = {
    -1: b'\xaa\xbb\xcc\xdd', # fim do pacote

    1: b'\x01', # pergunta se está vivo
    2: b'\x02', # responde que está vivo

    3: b'\x03', # arquivo enviado
    4: b'\x04', # responde arquivo recebido

    5: b'\x05', # arquivo fora de ordem
    6: b'\x06', # arquivo corompido

}

d_h0 = {
    1: b'\x01',
    'handshake': b'\x01',
    2: b'\x02',
    'pacote': b'\x02',
}

d_head = {
    # 'h0': b'\x01',
}
