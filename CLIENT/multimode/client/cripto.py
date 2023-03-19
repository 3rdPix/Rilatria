def encrypt(msg : bytearray) -> bytearray:
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
                int(box_1[0]) + # A box byte
                int(box_3[-1]) + # C box byte
                int(box_2[int(len(box_2) / 2)]) # B box byte
            )
        case 1:
            suma = (
                int(box_1[0]) + # A box byte
                int(box_3[-1]) + # C box byte
                int(box_2[len(box_2) // 2]) + # B box byte
                int(box_2[int(len(box_2) // 2) + 1])
                )
    match suma % 2:
        case 0: return bytearray(int(0).to_bytes(1, 'big') + box_3 + box_1 + box_2)
        case 1: return bytearray(int(1).to_bytes(1, 'big') + box_1 + box_3 + box_2)


def decrypt(msg : bytearray) -> bytearray:
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