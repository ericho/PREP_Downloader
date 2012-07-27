# -*- coding: utf-8 -*-

'''
Created on 26/07/2012

@author: Erich Cordoba

'''
import urllib2
import json
import csv
import time


class prep_downloader:
    ''' Clase para descargar la informacion del PREP de http://yosoyantifraude.org/json.php 
        Se conecta al servicio web y guarda la informacion en un archivo CSV.
    '''
    
    def __init__(self):
        ''' Constructor de la clase'''
        self.url = "http://yosoyantifraude.org/json.php"
        self.id_contador = '1'
        self.archivo = open("prep_antifraude.csv", "wb")
        self.archivo_csv = csv.writer(self.archivo)
        self.archivo_csv.writerow(["Fuente", "Imagen", "Entidad", "Municipio", "Distrito", "Seccion", "Tipo de casilla", "PAN", "PRI", "PRD", "VERDE", "MOV", "PANAL", "PRI_VERDE", "PRD_PT_MOV", "PRD_PT", "PRD_MOV", "PT_MOV", "No registrados", "Nulos"])
        
        
    def solicitar_datos(self, id_cont):
        ''' Realiza la consulta en el servicio web y la decodifica '''
        try:
            self.web_con = urllib2.urlopen(self.url + "?from_id=" + id_cont)
            datos = self.web_con.read()
            self.web_con.close()
            return json.loads(datos)
        except:
            print "Error de conexion con el servicio Web."
    
    def casilla_a_lista(self, casilla):
        ''' Convierte una casilla (diccionario) en una lista para ser guardada en CSV
            Formato : Fuente, Imagen, entidad, municipio, distrito, seccion, tipoCasilla, pan, pri, prd, verde, pt, mov, nuevaAlianza, pri_verde, prd_pt_mov, prd_pt, prd_mov, pt_mov, noRegistrados, nulos '''
        fila_lista = []
        fila_lista.append(casilla['fuente'])
        fila_lista.append(casilla['imagen'])
        fila_lista.append(casilla['entidad'])
        fila_lista.append(casilla['municipio'])
        fila_lista.append(casilla['distrito'])
        fila_lista.append(casilla['seccion'])
        fila_lista.append(casilla['tipoCasilla'])
        resultados = casilla['resultados']
        fila_lista.append(resultados['pan'])
        fila_lista.append(resultados['pri'])
        fila_lista.append(resultados['prd'])
        fila_lista.append(resultados['verde'])
        fila_lista.append(resultados['pt'])
        fila_lista.append(resultados['mov'])
        fila_lista.append(resultados['nuevaAlianza'])
        fila_lista.append(resultados['pri_verde'])
        fila_lista.append(resultados['prd_pt_mov'])
        fila_lista.append(resultados['prd_pt'])
        fila_lista.append(resultados['prd_mov'])
        fila_lista.append(resultados['pt_mov'])
        fila_lista.append(resultados['noRegistrados'])
        fila_lista.append(resultados['nulos'])
        fila_encode = self.encode_a_utf8(fila_lista)
        return fila_encode
        
    def encode_a_utf8(self, lista):
        ''' Decodifica UNICODE a UTF8 '''
        lista_encode = []
        for dat in lista:
            try:
                lista_encode.append(dat.encode('utf-8'))
            except:
                lista_encode.append('')
        return lista_encode
    
    def descargar_datos(self):
        ''' Realiza la iteracion en todas las casillas 
            Cuando el servicio se queda sin casillas devuelve al diccionario Sabanas vacio
        '''
        while True:
            datos_json = self.solicitar_datos(self.id_contador)            
            if len(datos_json['sabanas']) == 0: # no hay mas datos en el servicio web
                break;
            else:
                sabanas = datos_json['sabanas']
                for casilla in sabanas:
                    # Funcion donde paso un diccionario y me devuelve una lista
                    fila = self.casilla_a_lista(casilla)
                    self.id_contador = casilla['id']
                    self.archivo_csv.writerow(fila)
                    print "Escribiendo fila " + self.id_contador
                self.id_contador = str(int(self.id_contador) + 1)
                time.sleep(1)
        self.archivo.close()
        
if __name__ == "__main__":
    prog = prep_downloader()
    prog.descargar_datos()