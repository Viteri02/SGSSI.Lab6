# -*- coding: utf-8 -*-

import hashlib
import sys
import random

def calcular_sha256(file_path):
    sha256_hash = hashlib.sha256()
    
    try:
        with open(file_path, 'rb') as file:
            while True:
                data = file.read(65536)  # Lee el archivo en bloques de 64KB
                if not data:
                    break
                sha256_hash.update(data)
        return sha256_hash.hexdigest()
    except IOError:
        print("Error al calcular el resumen SHA-256.")
        return None

def generar_secuencia_hex():
    secuencia_hex = ''.join(random.choice('abcdef0123456789') for _ in range(8))
    return secuencia_hex

def agregar_datos_al_archivo(archivo_entrada, identificador_publico):
    try:
        sha256_original = calcular_sha256(archivo_entrada)

        if sha256_original:
            while True:
                # Generar la secuencia hexadecimal
                secuencia_hex = generar_secuencia_hex()

                # Crear un nuevo archivo con los datos adicionales
                archivo_salida = archivo_entrada.split(".")[0] + "_con_datos.txt"
                with open(archivo_salida, 'w') as salida:
                    with open(archivo_entrada, 'r') as entrada:
                        contenido = entrada.read()
                        salida.write(contenido)

                    salida.write('\n')
                    salida.write(secuencia_hex + '\t' + identificador_publico + '\t100')

                sha256_nuevo = calcular_sha256(archivo_salida)
                if sha256_nuevo.startswith('0'):
                    break

            print('Se ha creado el archivo con los datos adicionales: {}'.format(archivo_salida))
            print('Resumen SHA-256 del archivo original: {}'.format(sha256_original))
            print('Resumen SHA-256 del nuevo archivo: {}'.format(sha256_nuevo))

        else:
            print('No se pudo calcular el resumen SHA-256 para el archivo original.')

    except IOError:
        print('El archivo {} no se encontró.'.format(archivo_entrada))

if len(sys.argv) != 3:
    print("Uso: python programa.py <nombre_del_archivo> <identificador_publico>")
else:
    archivo_entrada = sys.argv[1]
    identificador_publico = sys.argv[2]
    agregar_datos_al_archivo(archivo_entrada, identificador_publico)
