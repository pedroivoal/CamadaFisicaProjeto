commands = {
    -1: '\xaa\xbb\xcc\xdd', # fim do pacote

    1: b'\x01', # pergunta se está vivo
    2: b'\x02', # responde que está vivo

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
