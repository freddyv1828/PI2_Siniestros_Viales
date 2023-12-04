import pandas as pd
import datetime as dt
import re
import numpy as np
from datetime import datetime

# Verificar tipo de dtos de los dataframe
def verificar_datos(df):
    # Comprobamos que el dataframe sea valido
    if not isinstance(df, pd.DataFrame):
        raise ValueError("El parámetro df, debe ser un dataframe de pandas")
    
    # Obtenemos un resumen de tipos de datos y valores nulos 
    resume = {"columna": [], "tipo_dato": [], "datos_nulos": [],
              "porcentaje_nulos": [], "porcentaje_no_nulos": []}
    
    for colum in df.columns:
        no_nulos = (df[colum].count()/len(df)) * 100
        # Advertimos si la columna tiene valores nulos
        if df[colum].isnull().sum():
            print(f"Advertencia: la columna {colum}, tiene valores nulos")
            
        resume["columna"].append(colum)
        resume["tipo_dato"].append(df[colum].apply(lambda x: type(x)).unique())
        resume["datos_nulos"].append(df[colum].isnull().sum())
        resume["porcentaje_nulos"].append(round(100-no_nulos, 2))
        resume["porcentaje_no_nulos"].append(round(no_nulos, 2))
        
    salida = pd.DataFrame(resume)
    return salida

# Función para encontrar valores duplicados
def valores_duplicados(df, columnas):
    # Se filtran las filas duplicadas
    duplicated_rows = df[df.duplicated(subset = columnas, keep = False)]
    
    # Numero de filas duplicadas
    numero_duplicados = duplicated_rows.shape[0]
    
    return numero_duplicados

def verificar_tipo_variable(df):

    mi_dict = {"nombre_campo": [], "tipo_datos": []}

    for columna in df.columns:
        mi_dict["nombre_campo"].append(columna)
        mi_dict["tipo_datos"].append(df[columna].apply(type).unique())
    df_info = pd.DataFrame(mi_dict)
        
    return df_info

# Convierte hora a fotmato time
def convertir_time(x):

    if isinstance(x, str):
        try:
            return datetime.strptime(x, "%H:%M:%S").time()
        except ValueError:
            return None
    elif isinstance(x, datetime):
        return x.time()
    return x

# Inputar valores por la moda

def imputa_valor_frecuente(df, columna):
  
    # Se reemplaza "SD" con NaN en la columna
    df[columna] = df[columna].replace('SD', pd.NA)

    # Se calcula el valor más frecuente en la columna
    valor_mas_frecuente = df[columna].mode().iloc[0]
    print(f'El valor mas frecuente es: {valor_mas_frecuente}')

    # Se imputan los valores NaN con el valor más frecuente
    df[columna].fillna(valor_mas_frecuente, inplace=True)
    

def ver_duplicados(df, columna):
   
    # Se filtran las filas duplicadas
    duplicated_rows = df[df.duplicated(subset=columna, keep=False)]
    if duplicated_rows.empty:
        return "No hay duplicados"
    
    # se ordenan las filas duplicadas para comparar entre sí
    duplicated_rows_sorted = duplicated_rows.sort_values(by=columna)
    return duplicated_rows_sorted


# Impita por valores frecuentes
def imputa_valor_frecuente(df, columna):
    # Se reemplaza "SD" con NaN en la columna
    df[columna] = df[columna].replace('SD', pd.NA)

    # Se calcula el valor más frecuente en la columna
    valor_mas_frecuente = df[columna].mode().iloc[0]
    print(f'El valor mas frecuente es: {valor_mas_frecuente}')

    # Se imputan los valores NaN con el valor más frecuente
    df[columna].fillna(valor_mas_frecuente, inplace=True)

# Imputa valores de edad segun el sexo    
def imputa_edad_media_segun_sexo(df):
    
    # Se reemplaza "SD" con NaN en la columna 'edad'
    df['Edad'] = df['Edad'].replace('SD', pd.NA)

    # Se calcula el promedio de edad para cada grupo de género
    promedio_por_genero = df.groupby('Sexo')['Edad'].mean()
    print(f'La edad promedio de Femenino es {round(promedio_por_genero["FEMENINO"])} y de Masculino es {round(promedio_por_genero["MASCULINO"])}')

    # Se llenan los valores NaN en la columna 'edad' utilizando el promedio correspondiente al género
    df['Edad'] = df.apply(lambda row: promedio_por_genero[row['Sexo']] if pd.isna(row['Edad']) else row['Edad'], axis=1)
    # Lo convierte a entero
    df['Edad'] = df['Edad'].astype(int)
    
# Clasificar por semestre
def clasificar_semestre(mes):
    if mes <= 6:
        return 1
    else:
        return 2