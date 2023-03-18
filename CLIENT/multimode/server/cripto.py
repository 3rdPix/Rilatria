def encriptar(msg : bytearray) -> bytearray:
    box_1: bytearray = bytearray()
    box_2: bytearray = bytearray()
    box_3: bytearray = bytearray()
    for indice, trozo in enumerate(msg):
        match indice % 3:
            case 0: box_1.extend(trozo.to_bytes(1, 'big'))
            case 1: box_2.extend(trozo.to_bytes(1, 'big'))
            case 2: box_3.extend(trozo.to_bytes(1, 'big'))
    match len(box_2) % 2:
        case 0:
            suma = (
                int(box_1[0]) + # byte de arreglo A
                int(box_3[-1]) + # byte de arreglo C
                int(box_2[int(len(box_2) / 2)]) # byte central de B
            )
        case 1:
            suma = (
                int(box_1[0]) + # byte de arreglo A
                int(box_3[-1]) + # byte de arreglo C
                int(box_2[len(box_2) // 2]) + # bytes centrales de B
                int(box_2[int(len(box_2) // 2) + 1])
                )
    match suma % 2:
        case 0: return bytearray(int(0).to_bytes(1, 'big') + box_3 + box_1 + box_2)
        case 1: return bytearray(int(1).to_bytes(1, 'big') + box_1 + box_3 + box_2)


def desencriptar(msg : bytearray) -> bytearray:
    order: int = msg.pop(0)
    min_size: int = len(msg) // 3
    fix: int = 0 if len(msg) % 3 == 0 else 1
    
    # Determine the boxes
    match order:
        case 0:
            box_3: bytearray = msg[0:min_size]
            box_1: bytearray = msg[min_size:(min_size * 2) + fix]
            box_2: bytearray = msg[(min_size * 2) + fix::]
        case 1:
            box_1: bytearray = msg[0:(min_size + fix)]
            box_3: bytearray = msg[(min_size + fix):(min_size * 2) + fix]
            box_2: bytearray = msg[(min_size * 2) + fix::]
    
    # Create the message
    message: bytearray = bytearray()
    for index in range(len(msg)):
        match index % 3:
            case 0: message.extend(box_1.pop(0).to_bytes(1, 'big'))
            case 1: message.extend(box_2.pop(0).to_bytes(1, 'big'))
            case 2: message.extend(box_3.pop(0).to_bytes(1, 'big'))
    return message


if __name__ == "__main__":
    # Testear encriptar
    msg_original = bytearray(b'\x05\x08\x03\x02\x04\x03\x05\x09\x05\x09\x01')
    msg_esperado = bytearray(b'\x01\x05\x02\x05\x09\x03\x03\x05\x08\x04\x09\x01')

    msg_encriptado = encriptar(msg_original)
    if msg_encriptado != msg_esperado:
        print("[ERROR] Mensaje escriptado erroneamente")
    else:
        print("[SUCCESSFUL] Mensaje escriptado correctamente")
    
    # Testear desencriptar
    msg_desencriptado = desencriptar(msg_esperado)
    if msg_desencriptado != msg_original:
        print("[ERROR] Mensaje descencriptado erroneamente")
    else:
        print("[SUCCESSFUL] Mensaje descencriptado correctamente")
