import pandas as pd
import numpy as np

# Definir marcas y productos
marcas = ['Cyzone', 'Esika', 'Lbel']
productos_cyzone = ['Ainnara Extra', 'Nitro', 'Nitro Air', 'Nitro Intensive', 'Taste Warm', 'Ainnara', 'Blue&Blue', 'Bolsa', 'Pera in Love', 'Pure', 'Blue&Blue Him', 'Sandia Shake', 'Sweet Black Intense', 'Taste Cool']
productos_esika = ['Fantasia Azul Infinito', 'Golden Vainilla', 'Azul Infinito', 'Magnant Inspire', 'Magnan select', 'Magnetic Absolute', 'Dorsay Inspire', 'LOVE!', 'Pulso Absolute', 'Red Power', 'Red Rose', 'Vibrant', 'Vibrant addiction', 'Dorsay class', 'Expression sens']
productos_lbel = ['Magnolia DAmelie', 'Movible', 'Satin nude', 'Liaison Live Adventure', 'Mon LBEL Rubi', 'Devos Magnetic', 'Homme 033', 'Satin']

# Precios fijos por país (puedes ajustar estos valores según sea necesario)
precios_por_producto_y_pais = {
    'Cyzone': {
        'Ainnara Extra': {'PE': 20.00, 'CO': 22.00, 'CL': 21.00, 'EC': 19.00},
        'Nitro': {'PE': 18.00, 'CO': 20.00, 'CL': 19.00, 'EC': 17.00},
        'Nitro Air': {'PE': 25.00, 'CO': 26.00, 'CL': 24.00, 'EC': 23.00},
        'Nitro Intensive': {'PE': 23.00, 'CO': 24.00, 'CL': 22.00, 'EC': 21.00},
        'Taste Warm': {'PE': 22.00, 'CO': 23.00, 'CL': 21.00, 'EC': 20.00},  # Agrega otros productos y precios por país aquí
        'Ainnara': {'PE': 19.00, 'CO': 20.00, 'CL': 18.00, 'EC': 17.00},
        'Blue&Blue': {'PE': 20.00, 'CO': 22.00, 'CL': 21.00, 'EC': 19.00},
        'Pera in Love': {'PE': 21.00, 'CO': 23.00, 'CL': 22.00, 'EC': 20.00},
        'Pure': {'PE': 26.00, 'CO': 28.00, 'CL': 27.00, 'EC': 25.00},
        'Blue&Blue Him': {'PE': 24.00, 'CO': 26.00, 'CL': 25.00, 'EC': 23.00},
        'Sandia Shake': {'PE': 19.00, 'CO': 20.00, 'CL': 18.00, 'EC': 17.00},
        'Sweet Black Intense': {'PE': 21.00, 'CO': 23.00, 'CL': 22.00, 'EC': 20.00},
        'Taste Cool': {'PE': 20.00, 'CO': 22.00, 'CL': 21.00, 'EC': 19.00},
    },
    'Esika': {
        'Fantasia Azul Infinito': {'PE': 30.00, 'CO': 32.00, 'CL': 31.00, 'EC': 29.00},
        'Golden Vainilla': {'PE': 28.00, 'CO': 30.00, 'CL': 29.00, 'EC': 27.00},
        'Azul Infinito': {'PE': 26.00, 'CO': 28.00, 'CL': 27.00, 'EC': 25.00},
        # Agrega otros productos y precios por país aquí
    },
    'Lbel': {
        'Magnolia DAmelie': {'PE': 25.00, 'CO': 27.00, 'CL': 26.00, 'EC': 24.00},
        'Movible': {'PE': 24.00, 'CO': 26.00, 'CL': 25.00, 'EC': 23.00},
        'Satin nude': {'PE': 29.00, 'CO': 31.00, 'CL': 30.00, 'EC': 28.00},
        # Agrega otros productos y precios por país aquí
    }
}

# Crear un DataFrame para almacenar los datos
data = []

# Ajustar pesos para cada marca
marca_weights = [0.5, 0.3, 0.2]  # Probabilidad de selección para Cyzone, Esika y Lbel
paises = ['PE', 'CO', 'CL', 'EC']  # Ejemplo de países

# Generar 100,000 datos simulados
for _ in range(100000):
    fecha = pd.to_datetime(np.random.choice(pd.date_range(start='2021-01-01', end='2023-12-31')))
    marca = np.random.choice(marcas, p=marca_weights)  # Elegir marca con pesos

    if marca == 'Cyzone':
        producto = np.random.choice(productos_cyzone)
    elif marca == 'Esika':
        producto = np.random.choice(productos_esika)
    else:
        producto = np.random.choice(productos_lbel)

    # Elegir un país al azar
    pais = np.random.choice(paises)

    # Obtener el precio del producto según el país
    # Si no hay precio específico, asigna un precio aleatorio entre 10 y 100
    if marca in precios_por_producto_y_pais and producto in precios_por_producto_y_pais[marca]:
        precio = precios_por_producto_y_pais[marca][producto].get(pais, np.round(np.random.uniform(10, 100), 2))
    else:
        precio = np.round(np.random.uniform(10, 100), 2)  # Asignar precio aleatorio si no se encuentra el producto

    cantidad = np.random.randint(1, 20)  # Cantidad comprada

    data.append([fecha, producto, cantidad, precio, pais])

# Crear DataFrame
df = pd.DataFrame(data, columns=['fecha', 'producto', 'cantidad', 'precio', 'pais'])

# Guardar a un CSV
df.to_csv('compras_simuladas.csv', index=False)

print("CSV 'compras_simuladas.csv' generado con éxito.")
