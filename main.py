import sys
import requests
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QComboBox, QPushButton, QMessageBox

# Predefined mapping of countries and cities to coordinates
locations = {
    "USA": {
        "New York": (40.7128, -74.0060),
        "Los Angeles": (34.0522, -118.2437),
        "Chicago": (41.8781, -87.6298),
        "Houston": (29.7604, -95.3698),
        "Phoenix": (33.4484, -112.0740)
    },
    "Canada": {
        "Toronto": (43.65107, -79.347015),
        "Vancouver": (49.2827, -123.1207),
        "Montreal": (45.5017, -73.5673),
        "Calgary": (51.0447, -114.0719),
        "Ottawa": (45.4215, -75.6972)
    },
    "UK": {
        "London": (51.5074, -0.1278),
        "Manchester": (53.4808, -2.2426),
        "Birmingham": (52.4862, -1.8904),
        "Glasgow": (55.8642, -4.2518),
        "Liverpool": (53.4084, -2.9916)
    },
    "Australia": {
        "Sydney": (33.8688, 151.2093),
        "Melbourne": (37.8136, 144.9631),
        "Brisbane": (27.4698, 153.0251),
        "Perth": (31.9505, 115.8605),
        "Adelaide": (34.9285, 138.6007)
    },
    "Germany": {
        "Berlin": (52.5200, 13.4050),
        "Munich": (48.1351, 11.5820),
        "Frankfurt": (50.1109, 8.6821),
        "Hamburg": (53.5511, 9.9937),
        "Cologne": (50.9375, 6.9603)
    },
    "France": {
        "Paris": (48.8566, 2.3522),
        "Marseille": (43.2965, 5.3698),
        "Lyon": (45.75, 4.85),
        "Toulouse": (43.6045, 1.4442),
        "Nice": (43.7102, 7.2620)
    },
    "India": {
        "Mumbai": (19.0760, 72.8777),
        "Delhi": (28.7041, 77.1025),
        "Bangalore": (12.9716, 77.5946),
        "Hyderabad": (17.3850, 78.4867),
        "Chennai": (13.0827, 80.2707)
    },
    "China": {
        "Shanghai": (31.2304, 121.4737),
        "Beijing": (39.9042, 116.4074),
        "Guangzhou": (23.1291, 113.2644),
        "Shenzhen": (22.5431, 114.0579),
        "Wuhan": (30.5928, 114.3055)
    },
    "Japan": {
        "Tokyo": (35.6895, 139.6917),
        "Osaka": (34.6937, 135.5023),
        "Nagoya": (35.1815, 136.9066),
        "Sapporo": (43.0618, 141.3545),
        "Fukuoka": (33.5904, 130.4017)
    },
    "South Korea": {
        "Seoul": (37.5665, 126.9780),
        "Busan": (35.1796, 129.0756),
        "Incheon": (37.4563, 126.7052),
        "Daegu": (35.8714, 128.6014),
        "Daejeon": (36.3504, 127.3845)
    },
    "Dominican Republic": {
        "Santo Domingo": (18.4861, -69.9312),
        "Santiago": (19.4511, -70.6970),
        "La Romana": (18.4274, -68.9720),
        "San Pedro de Macorís": (18.4310, -69.1079),
        "San Francisco de Macorís": (19.3000, -70.2500)
    },
    "Brazil": {
        "Sao Paulo": (-23.5505, -46.6333),
        "Rio de Janeiro": (-22.9068, -43.1729),
        "Brasília": (-15.8267, -47.9218),
        "Salvador": (-12.9714, -38.5014),
        "Fortaleza": (-3.7172, -38.5436)
    },
    "Mexico": {
        "Mexico City": (19.4326, -99.1332),
        "Guadalajara": (20.6597, -103.3496),
        "Monterrey": (25.6866, -100.3161),
        "Puebla": (19.0414, -98.2063),
        "Tijuana": (32.5149, -117.0382)
    },
    "Russia": {
        "Moscow": (55.7558, 37.6176),
        "Saint Petersburg": (59.9343, 30.3351),
        "Novosibirsk": (55.0084, 82.9357),
        "Yekaterinburg": (56.8389, 60.6057),
        "Nizhny Novgorod": (56.2965, 43.9361)
    },
    "Antarctica": {
        "McMurdo Station": (-77.8419, 166.6863),
        "Amundsen–Scott South Pole Station": (-90.0000, 0.0000),
        "Palmer Station": (-64.7706, -64.0527),
        "Rothera Research Station": (-67.5645, -68.1231),
        "Davis Station": (-68.7778, -78.1831),
    },
    "Italy": {
        "Rome": (41.9028, 12.4964),
        "Milan": (45.4642, 9.1900),
        "Venice": (45.4408, 12.3155)
    },
    "Spain": {
        "Madrid": (40.4168, -3.7038),
        "Barcelona": (41.3851, 2.1734),
        "Valencia": (39.4699, -0.3763)
    },
    "Argentina": {
        "Buenos Aires": (-34.6037, -58.3816),
        "Cordoba": (-31.4201, -64.1888),
        "Rosario": (-32.9468, -60.6393)
    },
    "South Africa": {
        "Cape Town": (-33.9249, 18.4241),
        "Johannesburg": (-26.2041, 28.0473),
        "Durban": (-29.8587, 31.0218)
    },
    "Egypt": {
        "Cairo": (30.0444, 31.2357),
        "Alexandria": (31.2156, 29.9553),
        "Giza": (30.0131, 31.2089)
    },
    # Add more countries and cities as needed
}

class WeatherApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Weather App")
        self.setGeometry(100, 100, 300, 200)

        layout = QVBoxLayout()

        self.country_label = QLabel("Select Country:")
        layout.addWidget(self.country_label)

        self.country_combo = QComboBox()
        self.country_combo.addItems(locations.keys())
        self.country_combo.currentTextChanged.connect(self.update_city_options)
        layout.addWidget(self.country_combo)

        self.city_label = QLabel("Select City:")
        layout.addWidget(self.city_label)

        self.city_combo = QComboBox()
        layout.addWidget(self.city_combo)

        self.fetch_button = QPushButton("Get Weather")
        self.fetch_button.clicked.connect(self.fetch_weather)
        layout.addWidget(self.fetch_button)

        self.result_label = QLabel("")
        layout.addWidget(self.result_label)

        self.setLayout(layout)

    def update_city_options(self):
        country = self.country_combo.currentText()
        self.city_combo.clear()
        self.city_combo.addItems(locations[country].keys())

    def fetch_weather(self):
        country = self.country_combo.currentText()
        city = self.city_combo.currentText()

        if country and city:
            latitude, longitude = locations[country][city]
            url = f"https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}&hourly=temperature_2m,precipitation"
            
            try:
                response = requests.get(url)
                data = response.json()
                temperature = data['hourly']['temperature_2m'][0]
                precipitation = data['hourly']['precipitation'][0]
                self.result_label.setText(f"Temperature: {temperature}°C\nPrecipitation: {precipitation}mm")
            except Exception as e:
                QMessageBox.critical(self, "Error", "Error fetching data. Please check the location.")
        else:
            QMessageBox.warning(self, "Input Error", "Please select a valid country and city.")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = WeatherApp()
    window.show()
    sys.exit(app.exec())
