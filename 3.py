# -*- coding: utf-8 -*-

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

def comprobar_archivos(archivo_entrada1, archivo_entrada2):
    try:
        contenido1 = open(archivo_entrada1, 'r').read()
        contenido2 = open(archivo_entrada2, 'r').read()

        if contenido2.startswith(contenido1):
            sha256 = calcular_sha256(archivo_entrada2)
            if sha256.startswith('0'):
                print('La segunda condición se cumple: El resumen SHA-256 del segundo fichero comienza con "0".')
            else:
                print('La segunda condición no se cumple: El resumen SHA-256 del segundo fichero no comienza con "0".')
        else:
            print('La primera condición no se cumple: El segundo fichero no comienza con los mismos contenidos que el primero.')

    except IOError:
        print('Error al abrir los archivos.')

if len(sys.argv) != 3:
    print("Uso: python programa.py <nombre_del_primer_archivo> <nombre_del_segundo_archivo>")
else:
    archivo_entrada1 = sys.argv[1]
    archivo_entrada2 = sys.argv[2]
    comprobar_archivos(archivo_entrada1, archivo_entrada2)
