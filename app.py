from flask import Flask, render_template
from flask_socketio import SocketIO
import math
import time
import threading

app = Flask(__name__)
socketio = SocketIO(app)

# Coordonnées des capteurs
sensors = [
    {"id": 1, "lat": 33.85563147149165, "lon": -5.572377739710788, "concentration": 0},  # Capteur 1
    {"id": 2, "lat": 33.85713810485788, "lon": -5.571694444520745, "concentration": 0},  # Capteur 2
    {"id": 3, "lat": 33.857751186152115, "lon": -5.5707205525246195, "concentration": 0}   # Capteur 3
]

# Taux d'augmentation et facteur de propagation
CONCENTRATION_INCREMENT = 0.1  # Augmentation lente des concentrations
PROPAGATION_RADIUS = 0.005  # Rayon de propagation (en degrés)
MAX_RADIUS = 0.01  # Rayon maximal du cercle (en degrés)
ALERT_THRESHOLD = 50  # Seuil de concentration pour déclencher une alerte

# Fonction pour simuler l'augmentation des concentrations d'ammoniac
def simulate_ammonia_propagation():
    max_concentration = 100  # Concentration maximale
    while True:
        alerts = []  # Liste pour stocker les alertes
        for sensor in sensors:
            if sensor["concentration"] < max_concentration:
                sensor["concentration"] += CONCENTRATION_INCREMENT
            
            # Vérifier si la concentration dépasse le seuil d'alerte
            if sensor["concentration"] >= ALERT_THRESHOLD:
                alerts.append(f"Capteur {sensor['id']} a détecté une fuite d'ammoniac!")

        # Calculer les cercles de concentration pour chaque capteur
        sensor_circles = []
        for sensor in sensors:
            radius = (sensor["concentration"] / max_concentration) * MAX_RADIUS
            sensor_circles.append({
                "lat": sensor["lat"],
                "lon": sensor["lon"],
                "radius": radius,
                "concentration": sensor["concentration"]
            })

        # Envoyer les données des capteurs et des cercles via WebSocket
        socketio.emit("update_data", {"sensor_circles": sensor_circles, "alerts": alerts})

        time.sleep(0.5)  # Intervalle entre les mises à jour (0.5 seconde)


@app.route('/')
def index():
    return render_template('index.html')


if __name__ == '__main__':
    threading.Thread(target=simulate_ammonia_propagation).start()
    socketio.run(app, debug=True)