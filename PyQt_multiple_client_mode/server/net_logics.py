import json
from socket import socket
from entities import User

class Router:

    @staticmethod
    def receive_request(user :User) -> dict:
        len_in_bytes = user.wire.recv(4)
        content_length = int.from_bytes(len_in_bytes, byteorder='big')
        request = Router.receive_bytes(content_length, user.wire)
        return request

    @staticmethod
    def receive_bytes(length: int, user_wire: socket) -> bytearray:
        """
        Receives a crypted msg and return original msg
        """
        # First part: re-groups packages by 32 bytes
        raw_received: bytearray = bytearray()
        offset = 0 if length % 32 == 0 else 1
        for _ in range((length // 32) + offset):
            block_number: int = int.from_bytes(user_wire.recv(4), 'little')
            if not block_number: break
            this_block = user_wire.recv(32)
            raw_received.extend(this_block)
        raw_received = raw_received[0:length]

        # Second part: interprets bytes
        decrypted = Router.decrypt(raw_received)
        decoded = decrypted.decode()
        loaded = json.loads(decoded)
        return loaded

    
    def code_bytes(written: any) -> bytearray:
        """
        Receives an object to be sent, encrypts and codifies it
        """
        # First part: crypting
        dumped = json.dumps(written)
        coded = dumped.encode()
        crypted = Router.encrypt(bytearray(coded))
        
        # Second part: msg build
        message: bytearray = bytearray()
        
        length: bytearray = len(crypted).to_bytes(4, 'big')
        message.extend(length)
        
        block_counter = 1
        while crypted:
            add = min(32, len(crypted))
            message.extend(block_counter.to_bytes(4, 'little'))
            new_block = bytearray()
            for _ in range(add): new_block.extend(crypted.pop(0).to_bytes(1, 'big'))
            message.extend(new_block)
            block_counter += 1
            if add % 32 != 0:
                for _ in range(32 - add):
                    message.extend(int(0).to_bytes(1, 'big'))
        return message
    
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
    
    @staticmethod
    def starken(object, client: User) -> None:
        msg = Router.code_bytes(object)
        client.controller.acquire()
        client.wire.sendall(msg)
        client.controller.release()

class Cmd:

    @staticmethod
    def user_name_check(errors: list) -> dict:
        if errors:
            order = {
                'cmd': 'user_name_check',
                'errors': errors,
                'valid': False
            }
            return order
        else:
            order = {
                'cmd': 'user_name_check',
                'errors': errors,
                'valid': True
            }
            return order

    @staticmethod
    def opponent_name(name: str) -> dict:
        order = {
            'cmd': 'opponent_name',
            'name': name
        }
        return order
    
    @staticmethod
    def show_game() -> dict:
        return {'cmd': 'show_game'}
    
    @staticmethod
    def stat_update(stat: str, new_val: int, mine: bool) -> dict:
        order = {
            'cmd': 'stat_update',
            'stat': stat,
            'new_val': new_val,
            'mine': mine
        }
        return order
    
    @staticmethod
    def show_cards(cards: list[dict]) -> dict:
        order = {
            'cmd': 'show_cards',
            'cards': cards
        }
        return order
    
    @staticmethod
    def update_board(board: list) -> dict:
        order = {
            'cmd': 'update_board',
            'board': board
        }
        return order
    
    
    @staticmethod
    def show_legal_moves(moves: list, eats: list) -> dict:
        order = {
            'cmd': 'show_legal_moves',
            'moves': moves,
            'eats': eats
        }
        return order

    @staticmethod
    def opponent_left() -> dict:
        order = {
            'cmd': 'opponent_left'
        }
        return order

    @staticmethod
    def turn_change() -> dict:
        return {'cmd': 'turn_change'}