
###Gliederung
1. RasperryPi an den Start bringen
2. Python-Skript schreiben
3. Daemon auf dem RasPi einrichten
4. Logfile erstellen
5. Probleme
6. Installationshinweise


####1.Setup für das RaspberryPi2

a) Internetverbindung aufbauen
b) Updaten
c) SSH aktivieren
d) dem RaspberryPi eine feste IP vergeben (Modem)
e) Windows:
	-PUTTY
	-VNC Viewer oder RemoteDesktop
	-RaspberryPi Autostart ThightVNC hinzugefügt
   Mac:
	-braucht keine PUTTY, geht über das Terminal
	-Microsoft Remote Desktop

-Edit:
-Cheatsheet für Terminal und Nano sowie Raspberry-Befehle sind wertvoll.
-evtl. den Schlafmodus vom W-lan deaktivieren.


####2. Python-Skript:

Das Skript wird für das Raspberry Pi in Python2.X geschrieben. Tipp: sudo -> Adminrechte
Hierzu müssen alle Bibliotheken über **Pip** oder auf anderem Wege installiert werden. Bei Pip gibt es
die Möglichkeit unregistrierte/unsichere Bibliotheken zu installieren: `pip --pre install meinebib`
Für dieses Projekt war es für pyOSC nötig.

Zwei Schlagworte sind wichtig für das Skript: **OSC** und **Serial**. Diese zwei Herausforderungen mussten
gemeistert und verknüpft werden. Die ganzen Befehle für Lektrik, die bei dem Eingangssignal verarbeitet werden,
stehen im ActionHandler.

Für das Senden ist es sinnvoll sich kurz zu fassen -> **string to binary integer**
Als Empfänger muss das RasPi den binaryInt wieder decoden: `lamp_values = list(str(bin(osc_list[0]))[2:])`
Damit Python Serial senden kann, muss man mit: `struct.pack('>B', n)`.
Der OSC-Server muss auf *0.0.0.0* stehen oder man gibt eine feste Adresse an, der Port muss über das
Terminal gesucht werden, siehe Code im Skript.
*CTRL+C quit the python job in the terminal*


####3. Daemon auf dem Raspberry Pi:

Hierfür gibt es viele Lösungen. Für dieses Projekt wurde Cron verwendet und folgendes Tutorial verwendet:
*http://www.raspberrypi-spy.co.uk/2013/07/running-a-python-script-at-boot-using-cron/*

_Edit:_
_Es ist wichtig, wenn man sein Skript testen möchte, dass man es erst in der "Front" klärt. Also ganz normal
das Terminal öffnen und in das Verzeichnis navigieren und mit `python meinScript.py` das Script ausführen.
Das hat den Vorteil, dass die ganzen *prints*, ect.pp. geloggt werden, was wir ja wollen beim Testen._

_Ebenfalls sollte man das eine Script nicht multibel betreiben. Mit `ps aux | grep /../meinSkript.py` holen wir uns
alle Prozesse die das Skript betreffen. Mit dem Befehl `kill pid_to_kill` kann man den jeweiligen Vorgang beenden._


####4. Logfile in Python:
Für Ausgaben von Background-Prozessen schreiben wir alles in ein Log-File und können so testen ob es läuft:

`fpath = os.path.join(os.path.abspath(os.path.dirname(__file__)),"logs/lektrik_log.txt)`

`file = open(fpath, "w") #mit "a" wird nicht berschrieben`

`file.write("message")`

`file.close()`

Der Code ist im Loop und wird immer ausgef\'fchrt, wenn neue Daten verarbeitet werden. Hierbei muss bei Linux
der Ordern vorhanden sein, wohin das Verzeichnis gespeichert wird, das Textfile wird beim ersten Lauf erzeugt,
wenn es noch nicht vorhanden ist. **JOIN** verkn\'fcpft zwei Pfade und returnt den kompletten Pfad. **ABSPATH** ist der
Absolute Pfad und startet vom Wurzelverzeichnis. **RELPATH** ist der relative Pfad und geht vom aktuellen Heimverzeichnis aus.


####5. Probleme und Lösungsansätze:
Die größten Probleme sind die Schnittstellen. Hier müssen oft Typen geändert werden damit beide Programme die selbe
Sprache sprechen. Ebenfalls muss man das OSC-Protokoll verstehen lernen, **/print** am Anfang des Strings sendet das Signal für den richtigen ActionHandler (in unserem Fall). So ist der erste Schritt, die Schnittstellen zum Lauften zu bringen und das gewählte Übertragungsprotokoll zu verstehen. Das gelingt am besten mit kleinen DummySkripts in der Testphase. Bei Fehlermeldungen ist oft auch ein Blick in die Bibliothek bei GitHub super, denn meistens ist auch hier einfach nur der Typ des vergebenen Parameters falsch oder fehlt. 


####6. Installationshilfe
- Python27 + Pip + pyserial + pyOSC
- VVVV + addonpack

WICHTIG: VVVV MUSS IM LEKTRIKORDNER, DAMIT DIE VERKNÜPFUNG GEWÄHRLEISTET IST.
_________________________________________________________________________________
*Wissenswertes:*
* The software utility Cron is a time-based job scheduler in Unix-like computer operating systems
* Richtig herunterfahren: sudo shutdown -h now /// aber auch kill und restart des programms
* 15 Useful Commands Every Raspberry Pi User Should Know: http://www.makeuseof.com/tag/15-useful-commands-every-raspberry-pi-user-should-know/
* Für Tests: while True: time.sleep(1) und print '%s and %s' %(a,b)
* Terminal: http://www.linux-fuer-blinde.de/91-0-dateien-aufspueren-mit-find.html

*RASPI:*
* http://www.raspberrypi-spy.co.uk/2015/02/how-to-autorun-a-python-script-on-raspberry-pi-boot/
* https://www.raspberrypi.org/documentation/linux/usage/cron.md
* http://www.raspberrypi-spy.co.uk/2013/07/running-a-python-script-at-boot-using-cron/
* http://pi.bek.no/accessTerminalBoot/

*VVVV-OSC:*
* http://hexler.net/touchosc
* http://hexler.net/docs/touchosc-setup-other
* https://vvvv.org/documentation/westtricks#keep-clean-structure-in-patches
* Literatur: Interaktives Skizzieren mit VVVV
