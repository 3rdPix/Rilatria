from cripto import decrypt, encrypt
from socket import socket as wire
import json

class Router:

    @staticmethod
    def recibir_bytes(leng: int, socket_de_origen: wire) -> bytearray:
        """
        Recibe un mensaje codificado y encriptado de largo determinado,
        y retorna el mensaje original
        """
        # Primera parte: reagrupa los paquetes de 32 bytes
        recibido_bruto: bytearray = bytearray()
        offset = 0 if leng % 32 == 0 else 1
        for _ in range((leng // 32) + offset):
            num_bloque: int = int.from_bytes(socket_de_origen.recv(4), 'little')
            if not num_bloque: break
            bloque_n = socket_de_origen.recv(32)
            recibido_bruto.extend(bloque_n)
        recibido_bruto = recibido_bruto[0:leng]

        # Segunda parte: interpreta los bytes del mensaje
        not_encriptado = decrypt(recibido_bruto)
        not_coded = not_encriptado.decode()
        not_dumped = json.loads(not_coded)
        return not_dumped

    @staticmethod
    def codificar_bytes(written: any) -> bytearray:
        """
        Recibe un objeto a ser enviado, lo encripta y codifica para
        ser enviado.
        """
        # Primera parte: encriptación
        dumped = json.dumps(written)
        coded = dumped.encode()
        encriptado = encrypt(bytearray(coded))
        
        # Segunda parte: construcción del mensaje
        mensaje: bytearray = bytearray()
        
        leng: bytearray = len(encriptado).to_bytes(4, 'big')
        mensaje.extend(leng)
        
        block_counter = 1
        while encriptado:
            add = min(32, len(encriptado))
            mensaje.extend(block_counter.to_bytes(4, 'little'))
            nuevo_bloque = bytearray()
            for _ in range(add): nuevo_bloque.extend(encriptado.pop(0).to_bytes(1, 'big'))
            mensaje.extend(nuevo_bloque)
            block_counter += 1
            if add % 32 != 0:
                for _ in range(32 - add):
                    mensaje.extend(int(0).to_bytes(1, 'big'))
        return mensaje

class Requests:

    @staticmethod
    def user_name(name: str) -> dict:
        order = {
            'request': 'user_name',
            'name': name
        }
        return order
    
    @staticmethod
    def finish_turn() -> dict:
        order = {
            'request': 'finish_turn'
        }
        return order
    
    @staticmethod
    def pick_card(option: int) -> dict:
        order = {
            'request': 'pick_card',
            'option': option
        }
        return order
    
    @staticmethod
    def cell_clicked(cell: tuple) -> dict:
        order = {
            'request': 'cell_clicked',
            'cell': list(cell)
        }
        return order