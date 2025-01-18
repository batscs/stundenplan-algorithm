# Architecture Decision Record: Server

## Kontext

Der hier entwickelte Service zum Generieren eines Stundenplans soll möglichst leicht zu verwenden sein.

Daher wurde sich entschieden diesen als Docker Container zu entwickeln damit es einfach ist diesen aufzusetzen durch ein dazugehöriges Docker Image.

Ursprünglich war dies Projekt nicht als Server aufgesetzt, was jedoch unpraktisch ist, da der Algorithmus sehr rechenintesiv ist und das Front-End der Endbenutzer nicht darunter leiden soll.

So ist der Algorithmus durch den Server jeder Zeit ansprechbar und muss nicht auf dem gleichen System laufen wie das Front-End.

## Alternativen

Alternative wäre den Algorithmus als Software anzubieten, jedoch dann performance impact auf das Spring Projekt.

Alternative umsetzbar durch Datenaustausch über shared Dateien von Spring Projekt und Python Algorithmus, oder direkt als in Java Spring implementieren.

# API Dokumentation

## Endpunkte

Ausführlich dokumentiert: [Swagger API Dokumentation /api/docs](/api/docs)

## Prozessmodellierung der Stundenplan API

### Datenbasis des Stundenplans übermitteln 
Endpunkt: POST /api/stundenplan  
![api_post](/docs/img/api/api_post.png)
### Stundenplan generieren
Endpunkt: PATCH /api/stundenplan  
![api_patch](/docs/img/api/api_patch.png)
### Stundenplan Ergebnis abrufen
Endpunkt: GET /api/stundenplan  
![api_get](/docs/img/api/api_get.png)