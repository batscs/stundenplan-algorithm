# docker-compose.yml

```yml
version: '2'

services:
    stundenplan:
        container_name: "stundenplan"
        image: git.fh-wedel.de/swp_stundenplan25/genetic_algorithm:0.0.1
        volumes:
            - ./resources:/app/src/python/resources
        ports:
            - "1111:80"
```

# Endpoints

GET /stundenplan - aktuellstes Ergebnis vom Algorithmus  
POST /stundenplan - Stundenplan Input als Body  
GET /stundenplan-run - Algorithmus ausführen mit Daten von POST/stundenplan 

GET /config  - aktuelle App Config  
POST /config - Config changes im Body