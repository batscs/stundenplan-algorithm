# Setup

### 1. Docker Engine bereitstellen 

z.B. Docker Desktop for Windows installieren & anmelden

### 2. docker-compose.yml erstellen  

```yml
version: '2'

services:
    stundenplan:
        container_name: "stundenplan"
        image: git.fh-wedel.de/swp_stundenplan25/genetic_algorithm:0.0.2
        volumes:
            - ./resources:/app/src/python/resources
        ports:
            - "1111:80"
```

### 3. docker login git.fh-wedel.de

Benötigt um das genetic_algorithm image von git.fh-wedel.de zu pullen im nächsten Schritt

### 4. docker-compose up -d

Muss im Terminal ausgewählt werden im Ordner wo die docker-compose.yml sich befindet

### 5. Im browser aufrufen (https://localhost:1111)

Swagger Dokumentation hier für Verwendung der API Endpunkte

# Endpoints

GET /stundenplan - aktuellstes Ergebnis vom Algorithmus  
POST /stundenplan - Stundenplan Input als Body  
GET /stundenplan-run - Algorithmus ausführen mit Daten von POST/stundenplan 

GET /config  - aktuelle App Config  
POST /config - Config changes im Body