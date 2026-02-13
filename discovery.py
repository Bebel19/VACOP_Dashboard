import paho.mqtt.client as mqtt
import subprocess
import json
import time
import re
import os

def run():
    # 1. On lance le tunnel SSH (Port UDP 5001 pour MediaMTX)
    cmd = "ssh -o StrictHostKeyChecking=no -R 0:localhost:5001 a.pinggy.io udp"
    
    print("⏳ Ouverture du tunnel Pinggy pour la vidéo...")
    process = subprocess.Popen(cmd.split(), stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)

    public_host = None
    public_port = None

    # 2. On lit la sortie pour récupérer l'adresse publique
    for line in process.stdout:
        print(f"[Tunnel Log] {line.strip()}")
        match = re.search(r'udp://([\w\.-]+):(\d+)', line)
        if match:
            public_host = match.group(1)
            public_port = int(match.group(2))
            break
    
    if public_host and public_port:
        # 3. Récupération des variables d'environnement (comme ton Backend)
        broker = os.getenv('MQTT_BROKER_URL', 'neocampus.univ-tlse3.fr')
        port = int(os.getenv('MQTT_BROKER_PORT', 10883))
        user = os.getenv('MQTT_USERNAME', 'test') # Par défaut 'test'
        pw = os.getenv('MQTT_PASSWORD', 'test')   # Par défaut 'test'
        topic = "TestTopic/VACOP/video/discovery"

        client = mqtt.Client(callback_api_version=mqtt.CallbackAPIVersion.VERSION2)
        
        if user and pw:
            client.username_pw_set(user, pw)
        
        try:
            client.connect(broker, port)
            payload = json.dumps({
                "host": public_host, 
                "port": public_port,
                "timestamp": time.time()
            })
            # On utilise retain=True pour que la Jetson l'ait même si elle démarre après
            client.publish(topic, payload, retain=True)
            print(f"🚀 SIGNAL ENVOYÉ : Jetson --> {public_host}:{public_port}")
        except Exception as e:
            print(f"❌ Erreur MQTT : {e}")

    # Garde le tunnel actif
    process.wait()

if __name__ == "__main__":
    run()