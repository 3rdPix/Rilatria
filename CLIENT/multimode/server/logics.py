from socket import socket
from cripto import encrypt, decrypt
import json


class Router:

    @staticmethod
    def receive_bytes(length: int, client_wire: socket) -> bytearray:
        """
        Receives a crypted msg and return original msg
        """
        # First part: re-groups packages by 32 bytes
        raw_received: bytearray = bytearray()
        offset = 0 if length % 32 == 0 else 1
        for _ in range((length // 32) + offset):
            block_number: int = int.from_bytes(client_wire.recv(4), 'little')
            if not block_number: break
            this_block = client_wire.recv(32)
            raw_received.extend(this_block)
        raw_received = raw_received[0:length]

        # Second part: interprets bytes
        decrypted = decrypt(raw_received)
        decoded = decrypted.decode()
        loaded = json.loads(decoded)
        return loaded

    @staticmethod
    def code_bytes(written: any) -> bytearray:
        """
        Receives an object to be sent, encrypts and codifies it
        """
        # First part: crypting
        dumped = json.dumps(written)
        coded = dumped.encode()
        crypted = encrypt(bytearray(coded))
        
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


class Instructions:

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
    def opponent_left() -> dict:
        order = {
            'cmd': 'opponent_left'
        }
        return order

    @staticmethod
    def remaining_time(time: int) -> dict:
        order = {
            'cmd': 'remaining_time',
            'time': int(time)
        }
        return order