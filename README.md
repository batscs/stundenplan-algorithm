# docker-compose.yml

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

# Endpoints

Docker ausführen
 
Anleitung
1. Im Terminal 
  - docker login git.fh-wedel.de
2. Docker compose starten auch im Terminal 
  - docker-compose up -d
3. Im Browser aufrufen 
  - http://localhost:1111

GET /stundenplan - aktuellstes Ergebnis vom Algorithmus  
POST /stundenplan - Stundenplan Input als Body  
GET /stundenplan-run - Algorithmus ausführen mit Daten von POST/stundenplan 

GET /config  - aktuelle App Config  
POST /config - Config changes im Body