{\rtf1\ansi\ansicpg1252\cocoartf1404\cocoasubrtf460
{\fonttbl\f0\fswiss\fcharset0 Helvetica;}
{\colortbl;\red255\green255\blue255;}
\paperw11900\paperh16840\margl1440\margr1440\vieww10800\viewh8400\viewkind0
\pard\tx566\tx1133\tx1700\tx2267\tx2834\tx3401\tx3968\tx4535\tx5102\tx5669\tx6236\tx6803\pardirnatural\partightenfactor0

\f0\fs24 \cf0 # LEKTRIK\
\
105 Gl\'fchbirnen und ein MidiController. Die Installation wird zur Musikvisualisierung verwendet und soll f\'fcr Interaktionen mit dem VJ/Dj offen sein. (http://michaelschwarz.digital/portfolio/lektrik/)\
\
###Gliederung\
1. RasperryPi an den Start bringen \
2. Python-Skript schreiben\
3. Daemon auf dem RasPi einrichten\
4. Logfile erstellen\
5. Probleme\
6. Installationshinweise\
\
\
\
####1.Setup f\'fcr das RaspberryPi2\
\
a) Internetverbindung aufbauen\
b) Updaten\
c) SSH aktivieren\
d) dem RaspberryPi eine feste IP vergeben (Modem)\
e) Windows:\
	-PUTTY \
	-VNC Viewer oder RemoteDesktop\
	-RaspberryPi Autostart ThightVNC hinzuf\'b8gen\
   Mac:\
	-braucht keine PUTTY, geht \'b8ber das Terminal\
	-Microsoft Remote Desktop\
\
_Edit:\
-Cheatsheet f\'fcr Terminal und Nano sowie Raspberry-Befehle sind wertvoll.\
-evtl. den Schlafmodus vom W-lan deaktivieren._\
\
\
\
\
####2. Python-Skript:\
\
Das Skript wird f\'fcr das Raspberry Pi in Python2.X geschrieben. Tipp: sudo -> Adminrechte\
Hierzu m\'fcssen alle Bibliotheken \'fcber **Pip** oder auf anderem Wege installiert werden. Bei Pip gibt es\
die M\'f6glichkeit unregistrierte/unsichere Bibliotheken zu installieren: `pip --pre install meinebib`\
F\'fcr dieses Projekt war es f\'fcr pyOSC n\'f6tig.\
\
Zwei Schlagworte sind wichtig f\'fcr das Skript: **OSC** und **Serial**. Diese zwei Herausforderungen mussten \
gemeistert und verkn\'fcpft werden. Die ganzen Befehle f\'fcr Lektrik, die bei dem Eingangssignal verarbeitet werden, \
stehen im ActionHandler.\
\
F\'fcr das Senden ist es sinnvoll sich kurz zu fassen -> **string to binary integer**\
Als Empf\'e4nger muss das RasPi den binaryInt wieder decoden: `lamp_values = list(str(bin(osc_list[0]))[2:])`\
Damit Python Serial senden kann, muss man mit: `struct.pack('>B', n)`.\
Der OSC-Server muss auf *0.0.0.0* stehen oder man gibt eine feste Adresse an, der Port muss \'fcber das \
Terminal gesucht werden, siehe Code im Skript. \
\
*CTRL+C quit the python job in the terminal*\
\
\
####3. Daemon auf dem Raspberry Pi:\
\
Hierf\'fcr gibt es viele L\'f6sungen. F\'fcr dieses Projekt wurde Cron verwendet und folgendes Tutorial verwendet:\
*http://www.raspberrypi-spy.co.uk/2013/07/running-a-python-script-at-boot-using-cron/*\
\
_Edit:_\
_Es ist wichtig, wenn man sein Skript testen m\'f6chte, dass man es erst in der "Front" kl\'e4rt. Also ganz normal\
das Terminal \'f6ffnen und in das Verzeichnis navigieren und mit `python meinScript.py` das Script ausf\'fchren.\
Das hat den Vorteil, dass die ganzen *prints*, ect.pp. geloggt werden, was wir ja wollen beim Testen._\
\
_Ebenfalls sollte man das eine Script nicht multibel betreiben. Mit `ps aux | grep /../meinSkript.py` holen wir uns\
alle Prozesse die das Skript betreffen. Mit dem Befehl `kill pid_to_kill` kann man den jeweiligen Vorgang beenden._\
\
\
\
\
####4. Logfile in Python:\
F\'fcr Ausgaben von Background-Prozessen schreiben wir alles in ein Log-File und k\'f6nnen so testen ob es l\'e4uft:\
\
`fpath = os.path.join(os.path.abspath(os.path.dirname(__file__)),"logs/lektrik_log.txt)`\
\
`file = open(fpath, "w") #mit "a" wird nicht berschrieben`\
\
`file.write("message")`\
\
`file.close()`\
\
\
Der Code ist im Loop und wird immer ausgef\'fchrt, wenn neue Daten verarbeitet werden. Hierbei muss bei Linux\
der Ordern vorhanden sein, wohin das Verzeichnis gespeichert wird, das Textfile wird beim ersten Lauf erzeugt, \
wenn es noch nicht vorhanden ist. **JOIN** verkn\'fcpft zwei Pfade und returnt den kompletten Pfad. **ABSPATH** ist der \
Absolute Pfad und startet vom Wurzelverzeichnis. **RELPATH** ist der relative Pfad und geht vom aktuellen Heimverzeichnis aus.\
\
\
\
####5. Probleme und L\'f6sungsans\'e4tze:\
Die gr\'f6\'dften Probleme sind die Schnittstellen. Hier m\'fcssen oft Typen ge\'e4ndert werden damit beide Programme die selbe\
Sprache sprechen. Ebenfalls muss man das OSC-Protokoll verstehen lernen, **/print** am Anfang des Strings sendet das Signal f\'fcr den richtigen ActionHandler (in unserem Fall). So ist der erste Schritt, die Schnittstellen zum Lauften zu bringen und das gew\'e4hlte \'dcbertragungsprotokoll zu verstehen. Das gelingt am besten mit kleinen DummySkripts in der Testphase. Bei Fehlermeldungen ist oft auch ein Blick in die Bibliothek bei GitHub super, denn meistens ist auch hier einfach nur der Typ des vergebenen Parameters falsch oder fehlt.  \
\
\
####6. Installationshilfe\
- Python27 + Pip + pyserial + pyOSC\
- VVVV + addonpack\
\
WICHTIG: VVVV MUSS IM LEKTRIKORDNER, DAMIT DIE VERKN\'dcPFUNG GEW\'c4HRLEISTET IST.\
_________________________________________________________________________________\
*Wissenswertes:*\
* The software utility Cron is a time-based job scheduler in Unix-like computer operating systems\
* Richtig herunterfahren: sudo shutdown -h now /// aber auch kill und restart des programms\
* 15 Useful Commands Every Raspberry Pi User Should Know: http://www.makeuseof.com/tag/15-useful-commands-every-raspberry-pi-user-should-know/\
* F\'fcr Tests: while True: time.sleep(1) und print '%s and %s' %(a,b)\
* Terminal: http://www.linux-fuer-blinde.de/91-0-dateien-aufspueren-mit-find.html \
\
*RASPI:*\
* http://www.raspberrypi-spy.co.uk/2015/02/how-to-autorun-a-python-script-on-raspberry-pi-boot/\
* https://www.raspberrypi.org/documentation/linux/usage/cron.md\
* http://www.raspberrypi-spy.co.uk/2013/07/running-a-python-script-at-boot-using-cron/\
* http://pi.bek.no/accessTerminalBoot/\
\
*VVVV-OSC:*\
* http://hexler.net/touchosc\
* http://hexler.net/docs/touchosc-setup-other\
* https://vvvv.org/documentation/westtricks#keep-clean-structure-in-patches\
* Literatur: Interaktives Skizzieren mit VVVV\
}