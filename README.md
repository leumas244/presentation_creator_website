# Stadtmission Präsentations-Erstellungs-Webseite

## Was ist das dieses Projekt?

Dieses Projekt ist eine Webseite zum automatischen Erstellen von SongBeamer Präsentationen für den Gottesdienst der
Stadtmission Grünstadt. Dafür wird der Ablaufplan (Agenda) aus ChurchTools ausgewertet und zu einer Songbeamer-Datei
umgewandelt.

Das Projekt ist Version 2.0

## Anleitung zum Nutzen des Projekts

Ab hier gibt es ein kleines HandsOn wie das Projekt lokal initialisiert wird.

### 0. Genutze Bibliotheken
- Django
- 

### 1. Datenbank initialisieren

Als Erstes, muss die Datenbank initialisiert werden. Diese bleibt durch die gitignore IMMER lokal. Mit dem Befehl:

```
python manage.py migrate
```

### 2. Superuser erstellen

Danach wird ein Admin-User gebraucht. Dieser wird mit nachfolgendem Befehl erstellt:

```
python manage.py createsuperuser
```

### 3. Server starten und betreiben

- Nun kann der Server gestartet werden.

```
python manage.py runserver
```

- Um im Nachhinein neue Datenbank Tabellen zu erstellen oder ändern, müssen während der Server ausgeschaltet ist, zwei
  weitere Befehle in dieser Reihenfolge ausgeführt werden.

```
python manage.py makemigrations
# Dann
python manage.py migrate
```