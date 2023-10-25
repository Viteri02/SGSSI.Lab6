# -*- coding: utf-8 -*-

import hashlib
import sys
import random
import time
import os

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

def agregar_datos_al_archivo(archivo_entrada, identificador_publico, mejor_codigo_hexadecimal):
    try:
        sha256_original = calcular_sha256(archivo_entrada)

        if sha256_original:
            archivo_con_ceros = archivo_entrada

            # Crear un nuevo archivo con los datos adicionales
            archivo_salida = archivo_entrada.split(".")[0] + "_con_datos.txt"
            with open(archivo_salida, 'w') as salida:
                with open(archivo_entrada, 'r') as entrada:
                    contenido = entrada.read()
                    contenido = contenido.replace(mejor_codigo_hexadecimal, generar_secuencia_hex())  # Sustituye el mejor código anterior
                    salida.write(contenido)

                salida.write('\n')
                salida.write(mejor_codigo_hexadecimal + '\t' + identificador_publico + '\t100')

            sha256_nuevo = calcular_sha256(archivo_salida)

            print('Se ha creado el archivo con los datos adicionales: {}'.format(archivo_salida))
            print('Resumen SHA-256 del archivo original: {}'.format(sha256_original))
            print('Resumen SHA-256 del nuevo archivo: {}'.format(sha256_nuevo))
            print('Código hexadecimal insertado: {}'.format(mejor_codigo_hexadecimal))

        else:
            print('No se pudo calcular el resumen SHA-256 para el archivo original.')

    except IOError:
        print('El archivo {} no se encontró.'.format(archivo_entrada))

def agregar_linea_personalizada(archivo_entrada, identificador_publico, codigo_hexadecimal):
    try:
        with open(archivo_entrada, 'r') as archivo_original:
            contenido = archivo_original.read()

        archivo_salida = archivo_entrada.split(".")[0] + "_con_datos_personalizados.txt"
        with open(archivo_salida, 'w') as salida:
            salida.write(contenido)
            nueva_linea = "{}\t{}\t100\n".format(codigo_hexadecimal, identificador_publico)
            salida.write(nueva_linea)

        print('Se ha creado el archivo con los datos personalizados: {}'.format(archivo_salida))

    except FileNotFoundError:
        print('El archivo {} no se encontró.'.format(archivo_entrada))

# Verificar si se proporcionaron suficientes argumentos en la línea de comandos
if len(sys.argv) != 4:
    print("Uso: python programa.py <nombre_del_archivo> <identificador_publico> <codigo_hexadecimal>")
else:
    archivo_entrada = sys.argv[1]
    identificador_publico = sys.argv[2]
    codigo_hexadecimal = sys.argv[3]
    agregar_linea_personalizada(archivo_entrada, identificador_publico, codigo_hexadecimal)

def encontrar_mejor_codigo_hexadecimal(archivo_entrada, identificador_publico):
    max_ceros = 0
    codigo_mejor_sha = ""

    start_time = time.time()

    while True:
        # Generar la secuencia hexadecimal
        secuencia_hex = generar_secuencia_hex()

        # Crear un nuevo archivo con los datos adicionales
        archivo_salida = archivo_entrada.split(".")[0] + "_con_datos.txt"
        with open(archivo_salida, 'w') as salida:
            with open(archivo_entrada, 'r') as entrada:
                contenido = entrada.read()
                contenido = contenido.replace(codigo_mejor_sha, secuencia_hex)  # Sustituye el mejor código anterior
                salida.write(contenido)

            salida.write('\n')
            salida.write(secuencia_hex + '\t' + identificador_publico + '\t100')

        sha256_nuevo = calcular_sha256(archivo_salida)
        ceros = 0
        while sha256_nuevo[ceros] == '0':
            ceros += 1

        if ceros > max_ceros:
            max_ceros = ceros
            codigo_mejor_sha = secuencia_hex

        if time.time() - start_time >= 60:
            break

    return codigo_mejor_sha

if len(sys.argv) != 3:
    print("Uso: python programa.py <nombre_del_archivo> <identificador_publico>")
else:
    archivo_entrada = sys.argv[1]
    identificador_publico = sys.argv[2]

    mejor_codigo_hexadecimal = encontrar_mejor_codigo_hexadecimal(archivo_entrada, identificador_publico)
    agregar_datos_al_archivo(archivo_entrada, identificador_publico, mejor_codigo_hexadecimal)
