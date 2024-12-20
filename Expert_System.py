# class ExpertSystem:
#     def __init__(self, dollar):
#         self.dollar_price = dollar
#         self.dollarTopValue = 18.00
#     # Rule basis
#
#
#     def dollar(self):
#         print(self.dollar_price)
#
#
#     def rule_1(self):
#         if self.dollar_price < self.dollarTopValue:
#             return True
#         else:
#             return False
#
#     def rule_2(self):
#         pass
#
#     def rule_3(self):
#         pass


import pandas as pd
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder


class ExpertSystem:
    def __init__(self, dollar_price):
        self.dollar_price = dollar_price
        self.dollarTopValue = 18.00
        self.model = None

    def train_model(self, data_file):
        # Load the data
        df = pd.read_csv(data_file)

        # Prepare the features and target
        features = ['NoManzana', 'NoLote', 'MtsCuadrados', 'CostoMetroCuadrado', 'PrecioTotal']
        target = 'Estatus'

        # Encode categorical variables
        le = LabelEncoder()
        df[target] = le.fit_transform(df[target])

        X = df[features]
        y = df[target]

        # Split the data
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

        # Train the model
        self.model = DecisionTreeClassifier(random_state=42)
        self.model.fit(X_train, y_train)

        # Evaluate the model
        accuracy = self.model.score(X_test, y_test)
        print(f"Precisión del modelo: {accuracy:.2f}")

    def predict_purchase(self, no_manzana, no_lote, mts_cuadrados, costo_metro_cuadrado, precio_total):
        if self.model is None:
            raise ValueError("Modelo no entrenado. Llamar primero al método train_model().")

        # Prepare the input data
        input_data = [[no_manzana, no_lote, mts_cuadrados, costo_metro_cuadrado, precio_total]]

        # Make prediction
        prediction = self.model.predict(input_data)

        # Convert prediction back to original label
        status = "Comprado" if prediction[0] == 1 else "Disponible"

        return status

    def recommend_action(self, no_manzana, no_lote, mts_cuadrados, costo_metro_cuadrado, precio_total):
        
        status = self.predict_purchase(no_manzana, no_lote, mts_cuadrados, costo_metro_cuadrado, precio_total)

        if status == "Disponible":
            if self.dollar_price < self.dollarTopValue:
                return (f"El lote {no_lote} en la manzana {no_manzana} está disponible. Considere la compra mientras"
                        f" el precio del dólar (${self.dollar_price}) sea favorable.")
            else:
                return (f"El lote {no_lote} en la manzana {no_manzana} está disponible pero el precio del dólar "
                        f"(${self.dollar_price}) es alto. Que se considere esperar para un mejor precio.")
        else:
            return f"El lote {no_lote} en la manzana {no_manzana} ya está vendido. No se necesita acción."


# Usage example
if __name__ == "__main__":
    expert_system = ExpertSystem(17.50)  # Current dollar price
    expert_system.train_model("Lotes.csv")  # Train the model with your CSV data

    # Example prediction and recommendation
    recommendation = expert_system.recommend_action(6, 12, 141.24, 885.01, 124998.8124)
    print(recommendation)