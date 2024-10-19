import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor

# Cargar datos del CSV
data = pd.read_csv('compras_simuladas.csv')

# Convertir la fecha a tipo datetime
data['fecha'] = pd.to_datetime(data['fecha'])

# Crear componentes de la fecha
data['year'] = data['fecha'].dt.year
data['month'] = data['fecha'].dt.month
data['day'] = data['fecha'].dt.day
data['day_of_week'] = data['fecha'].dt.dayofweek

# Agrupar datos por fecha, producto y país
grouped_data = data.groupby(['fecha', 'producto', 'pais']).agg({'cantidad': 'sum', 'precio': 'mean'}).reset_index()

# Asegurarse de que las columnas de año, mes, día y día de la semana están presentes
grouped_data['year'] = grouped_data['fecha'].dt.year
grouped_data['month'] = grouped_data['fecha'].dt.month
grouped_data['day'] = grouped_data['fecha'].dt.day
grouped_data['day_of_week'] = grouped_data['fecha'].dt.dayofweek

# Dividir en características y etiquetas
X = grouped_data[['year', 'month', 'day', 'day_of_week', 'producto', 'pais']]
y = grouped_data['cantidad']

# Crear variables dummy para el producto y país
X = pd.get_dummies(X, columns=['producto', 'pais'])

# Dividir los datos en conjunto de entrenamiento y prueba
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Entrenar el modelo
model = RandomForestRegressor()
model.fit(X_train, y_train)

# Función para predecir ventas en un país específico para un intervalo de fechas
def predict_sales(country, start_date, periods):
    future_dates = pd.date_range(start=start_date, periods=periods)
    predictions = {}

    # Iterar sobre cada producto único
    for product in grouped_data['producto'].unique():
        # Crear un DataFrame para las fechas futuras
        future_data = pd.DataFrame({
            'year': future_dates.year,
            'month': future_dates.month,
            'day': future_dates.day,
            'day_of_week': future_dates.dayofweek,
            'producto': [product] * len(future_dates),  # Agregar el nombre del producto
            'pais': [country] * len(future_dates)       # Agregar el país
        })

        # Crear variables dummy para el producto y país
        future_data = pd.get_dummies(future_data, columns=['producto', 'pais'])

        # Asegurarse de que las columnas de entrada coincidan
        future_data = future_data.reindex(columns=X.columns, fill_value=0)

        # Predecir
        predictions[product] = model.predict(future_data)

    # Calcular las ganancias
    predicted_sales = pd.DataFrame(predictions, index=future_dates)

    # Obtener el precio promedio por producto
    average_prices = grouped_data.groupby('producto')['precio'].mean()

    # Calcular ganancias por producto
    profit = {}

    for product in predicted_sales.columns:
        total_sales = predicted_sales[product].sum()  # Sumar todas las cantidades predichas
        average_price = average_prices[product]       # Obtener el precio promedio
        profit[product] = total_sales * average_price  # Calcular las ganancias

    # Mostrar ganancias por producto
    profit_df = pd.DataFrame(list(profit.items()), columns=['Producto', 'Ganancias'])

    # Devolver los 10 productos con mayores ganancias, ordenados de mayor a menor
    top_profit_df = profit_df.sort_values(by='Ganancias', ascending=False).head(10)
    return top_profit_df

# Ejemplo de uso de la función predict_sales
country = 'Perú'
start_date = '2024-10-01'
periods = 21
result = predict_sales(country, start_date, periods)

# Imprimir los resultados
print(result)

