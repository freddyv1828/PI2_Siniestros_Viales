import pandas as pd
import datetime as dt
import re
import numpy as np
from datetime import datetime
import matplotlib.pyplot as plt
import seaborn as sns

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
    

# Funcion distribucion de edades
def distribucion_edad(df):

    # Se crea una figura con un solo eje x compartido
    fig, ax = plt.subplots(2, 1, figsize=(12, 6), sharex=True)
    
    # Se grafica el histograma de la edad
    sns.histplot(df['Edad'], kde=True, ax=ax[0])
    ax[0].set_title('Histograma de Edad') ; ax[0].set_ylabel('Frecuencia')
    
    # Se grafica el boxplot de la edad
    sns.boxplot(x=df['Edad'], ax=ax[1])
    ax[1].set_title('Boxplot de Edad') ; ax[1].set_xlabel('Edad')
    
    # Se ajusta y muestra el gráfico
    plt.tight_layout()
    plt.show()
    
# Edad de las victimas por año    
def distribucion_edad_por_anio(df):
 
    # Se crea el gráfico de boxplot
    plt.figure(figsize=(12, 6))
    sns.boxplot(x='Año', y='Edad', data=df)
    
    plt.title('Boxplot de Edades de Víctimas por Año') ; plt.xlabel('Año') ; plt.ylabel('Edad de las Víctimas')
     
    # Se muestra el gráfico
    plt.show()
    
 # Distribucion por edad y rol de las victimas    
def edad_y_rol_victimas(df):
 
    plt.figure(figsize=(8, 4))
    sns.boxplot(y='Rol', x='Edad',data=df)
    plt.title('Edades por Condición')
    plt.show()

# Distribucion de esdades por victima   
def distribucion_edad_por_victima(df):
  
    # Se crea el gráfico de boxplot
    plt.figure(figsize=(14, 6))
    sns.boxplot(x='Victima', y='Edad', data=df)
    
    plt.title('Boxplot de Edades de Víctimas por tipo de vehículo que usaba') ; plt.xlabel('Tipo de vehiculo') ; plt.ylabel('Edad de las Víctimas')
     
    plt.show()
    

# Distribucion de los acceidentes mensuales
def accidentes_mensuales(df):

    # Se obtiene una lista de años únicos
    años = df['Año'].unique()

    # Se define el número de filas y columnas para la cuadrícula de subgráficos
    n_filas = 3
    n_columnas = 2

    # Se crea una figura con subgráficos en una cuadrícula de 2x3
    fig, axes = plt.subplots(n_filas, n_columnas, figsize=(14, 8))

    # Se itera a través de los años y crea un gráfico por año
    for i, year in enumerate(años):
        fila = i // n_columnas
        columna = i % n_columnas
        
        # Se filtran los datos para el año actual y agrupa por mes
        data_mensual = (df[df['Año'] == year]
                        .groupby('Mes')
                        .agg({'Cantidad_victimas':'sum'}))
        
        # Se configura el subgráfico actual
        ax = axes[fila, columna]
        data_mensual.plot(ax=ax, kind='line')
        ax.set_title('Año ' + str(year)) ; ax.set_xlabel('Mes') ; ax.set_ylabel('Cantidad de Víctimas')
        ax.legend_ = None
        
    # Se muestra y acomoda el gráfico
    plt.tight_layout()
    plt.show()

# Cantidad de victimas por mes    
def cantidad_victimas_mensuales(df):
  
    # Se agrupa por la cantidad de víctimas por mes
    data = df.groupby('Mes').agg({'Cantidad_victimas':'sum'}).reset_index()
    
    # Se grafica
    plt.figure(figsize=(6,4))
    ax = sns.barplot(x='Mes', y='Cantidad_victimas', data=data)
    ax.set_title('Cantidad de víctimas por Mes')
    ax.set_xlabel('Mes') ; ax.set_ylabel('Cantidad de Accidentes')
    
    # Se imprime resumen
    print(f'El mes con menor cantidad de víctimas tiene {data.min()[1]} víctimas')
    print(f'El mes con mayor cantidad de víctimas tiene {data.max()[1]} víctimas')
    
    # Se muestra el gráfico
    plt.show()
    
    
# Distribucion por semana y fin de semana
def cantidad_accidentes_semana_fin_de_semana(df):

    # Se valida que el DataFrame tenga al menos un registro
    if len(df) == 0:
        raise ValueError("El DataFrame debe tener al menos un registro")

    # Se convierte la columna 'fecha' a tipo de dato datetime
    df['Fecha'] = pd.to_datetime(df['Fecha'])

    # Se extrae el día de la semana (0 = lunes, 6 = domingo)
    df['Dia semana'] = df['Fecha'].dt.weekday

    # Se crea una columna 'tipo_dia' para diferenciar entre semana y fin de semana
    df['Tipo de día'] = df['Dia semana'].apply(lambda x: 'Fin de Semana' if x >= 5 else 'Semana')

    # Se cuenta la cantidad de accidentes por tipo de día
    data = df['Tipo de día'].value_counts().reset_index()
    data.columns = ['Tipo de día', 'Cantidad de accidentes']

    # Se crea el gráfico de barras
    plt.figure(figsize=(6, 4))
    ax = sns.barplot(x='Tipo de día', y='Cantidad de accidentes', data=data)

    ax.set_title('Cantidad de accidentes por tipo de día') ; ax.set_xlabel('Tipo de día') ; ax.set_ylabel('Cantidad de accidentes')

    # Se agrega las cantidades en las barras
    for index, row in data.iterrows():
        ax.annotate(f'{row["Cantidad de accidentes"]}', (index, row["Cantidad de accidentes"]), ha='center', va='bottom')

    # Se muestra el gráfico
    plt.show()
    
# Coheficiente de cohen 
def cohen(group1, group2):
  
    diff = group1.mean() - group2.mean()
    var1, var2 = group1.var(), group2.var()
    n1, n2 = len(group1), len(group2)
    pooled_var = (n1 * var1 + n2 * var2) / (n1 + n2)
    d = diff / np.sqrt(pooled_var)
    return d

def cantidades_accidentes_por_anio_y_sexo(df):
 
    # Se crea el gráfico de barras
    plt.figure(figsize=(12, 4))
    sns.barplot(x='Año', y='Edad', hue='Sexo', data=df,)
    
    plt.title('Cantidad de Accidentes por Año y Sexo')
    plt.xlabel('Año') ; plt.ylabel('Edad de las víctimas') ; plt.legend(title='Sexo')
    
    # Se muestra el gráfico
    plt.show()
    
def cohen_por_año(df):

    # Se obtienen los años del conjunto de datos
    años_unicos = df['Año'].unique()
    # Se crea una lista vacía para guardar los valores de Cohen
    cohen_lista = []
    # Se itera por los años y se guarda Cohen para cada grupo
    for a in años_unicos:
        grupo1 = df[((df['Sexo'] == 'MASCULINO') & (df['Año'] == a))]['Edad']
        grupo2 = df[((df['Sexo'] == 'FEMENINO')& (df['Año'] == a))]['Edad']
        d = cohen(grupo1, grupo2)
        cohen_lista.append(d)

    # Se crea un Dataframe
    cohen_df = pd.DataFrame()
    cohen_df['Año'] = años_unicos
    cohen_df['Estadistico de Cohen'] = cohen_lista
    cohen_df
    
    # Se grafica los valores de Cohen para los años
    plt.figure(figsize=(8, 4))
    plt.bar(cohen_df['Año'], cohen_df['Estadistico de Cohen'], color='skyblue')
    plt.xlabel('Año') ; plt.ylabel('Estadístico de Cohen') ; plt.title('Estadístico de Cohen por Año')
    plt.xticks(años_unicos)
    plt.show()
    

# Cantidad de victimas segun el rol y el sexo    
def cantidad_victimas_sexo_rol_victima(df):

    # Se crea el gráfico
    fig, axes = plt.subplots(1, 3, figsize=(15, 4))

    # Gráfico 1: Sexo
    sns.countplot(data=df, x='Sexo', ax=axes[0])
    axes[0].set_title('Cantidad de víctimas por sexo') ; axes[0].set_ylabel('Cantidad de víctimas')

    # Se define una paleta de colores personalizada (invierte los colores)
    colores_por_defecto = sns.color_palette()
    colores_invertidos = [colores_por_defecto[1], colores_por_defecto[0]]
    
    # Gráfico 2: Rol
    df_rol = df.groupby(['Rol', 'Sexo']).size().unstack(fill_value=0)
    df_rol.plot(kind='bar', stacked=True, ax=axes[1], color=colores_invertidos)
    axes[1].set_title('Cantidad de víctimas por rol') ; axes[1].set_ylabel('Cantidad de víctimas') ; axes[1].tick_params(axis='x', rotation=45)
    axes[1].legend().set_visible(False)
    
    # Gráfico 3: Tipo de vehículo
    df_victima = df.groupby(['Victima', 'Sexo']).size().unstack(fill_value=0)
    df_victima.plot(kind='bar', stacked=True, ax=axes[2], color=colores_invertidos)
    axes[2].set_title('Cantidad de víctimas por tipo de vehículo') ; axes[2].set_ylabel('Cantidad de víctimas') ; axes[2].tick_params(axis='x', rotation=45)
    axes[2].legend().set_visible(False)

    # Se muestran los gráficos
    plt.show()
    
# Cantidad de victimas por participante
def cantidad_victimas_participantes(df):
 
    # Se ordenan los datos por 'Participantes' en orden descendente por cantidad
    ordenado = df['Participantes'].value_counts().reset_index()
    ordenado = ordenado.rename(columns={'Cantidad': 'participantes'})
    ordenado = ordenado.sort_values(by='count', ascending=False)
    
    plt.figure(figsize=(15, 4))
    
    # Se crea el gráfico de barras
    ax = sns.barplot(data=ordenado, x='Participantes', y='count', order=ordenado['Participantes'])
    ax.set_title('Cantidad de víctimas por participantes')
    ax.set_ylabel('Cantidad de víctimas')
    # Rotar las etiquetas del eje x a 45 grados
    ax.set_xticklabels(ax.get_xticklabels(), rotation=45, horizontalalignment='right')

    # Se muestra el gráfico
    plt.show()
 
# Cantidad de acusados    
def cantidad_acusados(df):
  
    # Se ordenan los datos por 'Participantes' en orden descendente por cantidad
    ordenado = df['Acusado'].value_counts().reset_index()
    ordenado = ordenado.rename(columns={'Cantidad': 'Acusado'})
    ordenado = ordenado.sort_values(by='count', ascending=False)
    
    plt.figure(figsize=(15, 4))
    
    # Crear el gráfico de barras
    ax = sns.barplot(data=ordenado, x='Acusado', y='count', order=ordenado['Acusado'])
    ax.set_title('Cantidad de acusados en los hechos') ; ax.set_ylabel('Cantidad de acusados') 
    ax.set_xticklabels(ax.get_xticklabels(), rotation=45, horizontalalignment='right')

    # Se muestra el gráfico
    plt.show()
    
# Accidente por tipo de calle
def accidentes_tipo_de_calle(df):
 
    # Se crea el gráfico
    fig, axes = plt.subplots(1, 2, figsize=(10, 4))

    sns.countplot(data=df, x='Tipo_de_calle', ax=axes[0])
    axes[0].set_title('Cantidad de víctimas por tipo de calle') ; axes[0].set_ylabel('Cantidad de víctimas')

    sns.countplot(data=df, x='Cruce', ax=axes[1])
    axes[1].set_title('Cantidad de víctimas en cruces') ; axes[1].set_ylabel('Cantidad de víctimas')
    
    # Mostramos los gráficos
    plt.show()