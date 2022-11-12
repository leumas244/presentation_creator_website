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
- datetime
- bs4
- fuzzywuzzy
- requests
- python-pptx
- progressbar
- python-Levenshtein

```
pip3 install Django datetime bs4 fuzzywuzzy requests python-pptx progressbar python-Levenshtein
```

### 1. Datenbank initialisieren

Als Erstes, muss die Datenbank initialisiert werden. Diese bleibt durch die gitignore IMMER lokal. Mit dem Befehl:

```
python3 manage.py migrate
```

### 2. Superuser erstellen und Adminsettings setzen

Danach wird ein Admin-User gebraucht. Dieser wird mit nachfolgendem Befehl erstellt:

```
python3 manage.py createsuperuser
```

Um den Server zum laufen zu bringen, müssen initale AdminSettings gesetz werden. Um die Grundlegenden Einstellungen zu treffen reicht der folgende Befehl. Später wird dann noch im Frontend die restlichen Einstellungen eingetragen.

```
python3 manage.py initial_command
```

### 3. Server zum ersten mal starten und restliche AdminSettings einstellen

Nun kann der Server gestartet werden.

```
python3 manage.py runserver
```
Jetzt müssen die Adminsettings verfolständigt werden (unter {deinedomain}/admin/home/adminsetting/1/change/).
Vorallem der **ChurchTools Login-Token**, das **Email-Absender-Passwort** und wenn Dropbox bereits installiert ist kann auch der **Song-Pfad** geändert werden (z.B. "/home/****/Dropbox/Songs").

**Dannach muss der Server neu gestartet werden**

### 4. Rahmenbedingungen schaffen
Nun muss **Dropbox installiert** werden.
In den Admin-Einstellungen kann dannach der **Song-Pfad** angepasst werden (z.B. "/home/****/Dropbox/Songs").

Zusätzlich muss noch ein Ordner erstellt werden:
```
mkdir home/churchtools_connection_package/Gottesdienste
```

### 5. Datenbank befüllen
Nun kann die Datenbank befüllt werden. Dazu gibt es 3 Befehle.
```
python3 manage.py create_weekmottos
python3 manage.py import_agendas_from_churchtools
python3 manage.py import_sng_files_to_database
```
Um zusätzliche User hinzuzufügen kann der folgende Befehl bentzt werden. Dazu muss der Pfad zu der json-Datei in der import_user_form_json_file.py geändert werden muss.
```
python3 manage.py import_user_form_json_file
```
### 6. Cronjob erstellen
```
crontab -e

37 * * * * /usr/bin/python3 /pfad_zu_dem_ordner/presentation_creator_website/manage.py import_agendas_from_churchtools >> /pfad_zu_dem_ordner/import_agenda_log.txt 2>&1

30 12,0 * * * /usr/bin/python3 /pfad_zu_dem_ordners/presentation_creator_website/manage.py import_sng_files_to_database >> /pfad_zu_dem_ordner/import_sng_log.txt 2>&1

sudo service cron restart
```