# Setup (Endbenutzer)

### 1. Docker Engine bereitstellen 

z.B. Docker Desktop for Windows installieren & anmelden

### 2. docker-compose.yml erstellen  

Hierbei muss nicht die gesamte git repository gecloned werden. Mit folgender docker-compose wird der neuste stable release als container aufgesetzt.

```yml
version: '2'

services:
    algorithm:
        container_name: "stundenplan_algorithm"
        image: git.fh-wedel.de/swp_stundenplan25/genetic_algorithm:0.0.3
        volumes:
            - ./resources:/app/src/python/resources
        ports:
            - "1111:80"
```

### 3. docker login git.fh-wedel.de

Benötigt um das genetic_algorithm image von git.fh-wedel.de zu pullen im nächsten Schritt

### 4. docker-compose up -d

Muss im Terminal ausgeführt werden im Ordner wo die docker-compose.yml sich befindet

### 5. Im browser aufrufen (http://localhost:1111)

Swagger Dokumentation hier für Verwendung der API Endpunkte

# Endpoints

url: http://localhost:1111/api/docs

![swagger_ui](https://i.gyazo.com/927fd85973de5f6aa629f4d59f63fb71.png)

# Setup (Entwickler)

### 1. Git Repository Clonen

### 2. Docker-Engine bereitstellen

### 3. Starten
Zum alleinigen Ausführen reicht das gegebene Start-Shellscript
```sh
./start.bat
```

Bei Änderungen ist es erforderlich das Docker Image neu zu bauen, erst dann kann der Container mit den Änderungen gestartet werden.
```sh
./rebuild.bat
```

Alternative können für PyCharm oder IntelliJ die Run-Konfigurationen aus dem `.run` Ordner importiert werden

### 4. Testen
Die Tests können ausgeführt werden aus der tests-Directory (Working Directory muss sich in der befinden).

Der Algorithm-Server muss laufen damit die Tests ausgeführt werden können. 

##### Test Script ausführen
```sh
python test/test.py
```

Eigene Tests können entsprechend dem vorhanden Muster in `test/units.py` ergänzt werden