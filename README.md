# Inhaltsverzeichnis

1. [Introduction](#introduction)

2. [Setup (Endbenutzer)](#setup-endbenutzer)  
   1.1 [Docker Engine bereitstellen](#1-docker-engine-bereitstellen)  
   1.2 [docker login git.fh-wedel.de](#2-docker-login-gitfh-wedelde)  
   1.3 [docker-compose.yml erstellen](#3-docker-composeyml-erstellen)  
   1.4 [docker-compose up -d](#4-docker-compose-up--d)  
   1.5 [Im Browser aufrufen](#5-im-browser-aufrufen)  

3. [Endpoints](#endpoints)  

4. [Setup (Entwickler)](#setup-entwickler)  
   3.1 [Mit Docker](#mit-docker)  
       - [Git Repository Clonen](#1-git-repository-clonen)  
       - [Docker-Engine bereitstellen](#2-docker-engine-bereitstellen)  
       - [Starten](#3-starten)  
   3.2 [Ohne Docker](#ohne-docker)  
       - [Voraussetzungen](#1-voraussetzungen)  
       - [Requirements installieren](#2-requirements-installieren)  
       - [Starten](#3-starten)  

5. [Testen](#testen)  
   4.1 [Test Script ausführen](#test-script-ausführen)  

# Introduction

Diese Repository gehört zu dem Stundenplan Algorithmus, welcher ein Teil des Stundenplan25-Softwareprojekt der Fachhochschule Wedel ist.
Zu dem gesamten Projekt gibt es eine ausführlichere [Documentation](docs/documentation.pdf).

Diese Dokumentation ist für den Release 1.0.0 geschrieben, welches das Endprodukt für das Softwareprojekt dient.
Die Dokumentation wird nicht für neue Releases aktualisiert, da diese nicht im Rahmen des Softwareprojekts sind.


# Setup (Endbenutzer)

### 1. Docker Engine bereitstellen 

z.B. Docker Desktop for Windows installieren & anmelden

### 2. docker login git.fh-wedel.de

Benötigt um das genetic_algorithm image von git.fh-wedel.de zu pullen im nächsten Schritt

### 3. docker-compose.yml erstellen  

Hierbei muss nicht die gesamte git repository gecloned werden. Mit folgender docker-compose wird der neuste stable release als container aufgesetzt.

```yml
version: '2'

services:
    algorithm:
        container_name: "stundenplan_algorithm"
        image: git.fh-wedel.de/swp_stundenplan25/genetic_algorithm:1.0.0
        volumes:
            - ./resources:/app/src/python/resources
        ports:
            - "1111:1111"
```

### 4. docker-compose up -d

Muss im Terminal ausgeführt werden im Ordner wo die docker-compose.yml sich befindet

### 5. Im browser aufrufen (http://localhost:1111)

Swagger Dokumentation hier für Verwendung der API Endpunkte

# API Endpoints

url: http://localhost:1111/api/docs

![swagger_ui](https://i.gyazo.com/927fd85973de5f6aa629f4d59f63fb71.png)

# Setup (Entwickler)

## Mit Docker

### 1. Git Repository Clonen

### 2. Docker-Engine bereitstellen

### 3. Starten
Gestartet wird der Server über mit docker-compose
```sh
docker-compose up -d
```

Bei Änderungen ist es erforderlich das Docker Image neu zu bauen, erst dann kann der Container mit den Änderungen gestartet werden.
```sh
docker-compose up -d --build
```

Alternative können für PyCharm oder IntelliJ die Run-Konfigurationen aus dem `.run` Ordner importiert werden

## Ohne Docker

### 1. Voraussetzungen
Es muss mindestens python version 3.12 vorhanden sein, testen kann man das durch
```
python -V
```

### 2. Requirements installieren
Es befindet sich in der repo eine `requirements.txt` mit allen dependencies welche benötigt werden, python kann diese selbst installieren:
```
python -m pip install requirements.txt -r
```

### 3. Starten
Auf **Windows** kann der Server mit folgendem CMD einzeiler gestartet werden:
```sh
cmd /c "set PYTHONPATH=%CD%; %PYTHONPATH% && python -u src\python\server.py" 
```

Auf **Linux** kann der Server mit folgendem Shell einzeiler gestartet werden:
```sh
PYTHONPATH=$(pwd) && export PYTHONPATH && python -u src/python/server.py
```

## Testen
Die Tests können durch das script `test.py` in dem test Ordner ausgeführt werden.

Der Algorithm-Server muss laufen damit die Tests ausgeführt werden können. 

### Test Script ausführen
```sh
python test/test.py
```

Eigene Tests können entsprechend dem vorhanden Muster in `test/units.py` ergänzt werden