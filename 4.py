# -*- coding: utf-8 -*-

import os
import hashlib
import sys

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

def encontrar_archivos_condiciones(archivo_entrada, directorio):
    archivos_cumplen_condiciones = []
    max_zeros = -1
    archivo_con_mas_zeros = None

    with open(archivo_entrada, 'r') as entrada_file:
        contenido_entrada = entrada_file.read()

    for root, _, files in os.walk(directorio):
        for filename in files:
            file_path = os.path.join(root, filename)
            with open(file_path, 'r') as candidato_file:
                contenido_candidato = candidato_file.read()
                if contenido_candidato.startswith(contenido_entrada):
                    sha256 = calcular_sha256(file_path)
                    leading_zeros = len(sha256) - len(sha256.lstrip('0'))
                    if leading_zeros > max_zeros:
                        max_zeros = leading_zeros
                        archivo_con_mas_zeros = file_path
                    archivos_cumplen_condiciones.append((file_path, leading_zeros))

    return archivos_cumplen_condiciones, archivo_con_mas_zeros

if len(sys.argv) != 3:
    print("Uso: python programa.py <nombre_del_primer_archivo> <directorio_de_candidatos>")
else:
    archivo_entrada = sys.argv[1]
    directorio_candidatos = sys.argv[2]

    archivos_cumplen_condiciones, archivo_con_mas_zeros = encontrar_archivos_condiciones(archivo_entrada, directorio_candidatos)

    if not archivos_cumplen_condiciones:
        print('Ningún archivo en el directorio cumple las condiciones.')
    else:
        print('Archivos que cumplen las condiciones:')
        for archivo, leading_zeros in archivos_cumplen_condiciones:
            print('{} - Longitud del prefijo de 0\'s en el SHA-256: {}'.format(archivo, leading_zeros))

        
        if archivo_con_mas_zeros:
            print('\nArchivo con el SHA-256 más largo de 0\'s:', archivo_con_mas_zeros)

