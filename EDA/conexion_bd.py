import pymysql
from sqlalchemy import create_engine

# Crear conexion a bd
conexion = pymysql.connect(
    host="localhost",
    port= 3306,
    user= "root",
    passwd= "pupitre.123",
    database= "siniestros_viales_CABA",
)
# Crear cursor
cursor = conexion.cursor()

# Crear conexio con create_engine
host = "localhost"
port = 3306
user = "root"
password = "pupitre.123"
database = "siniestros_viales_CABA"

conexion_string = f"mysql+pymysql://{user}:{password}@{host}:{port}/{database}"
engine = create_engine(conexion_string)