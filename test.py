import time 
import requests
start_time = time.time()  # Startzeit

response = requests.get(url="http://nicolaicloess.pythonanywhere.com/prices")
end_time = time.time()  # Endzeit
print(f"Execution time: {end_time - start_time} seconds")  # Ausgabe der Dauer
