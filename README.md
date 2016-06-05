# raspberry-led-strip
NMCT Data Communication project: talking to a LED strip with the Raspberry Pi

## Leden
- [thomastoye](https://github.com/thomastoye)
- [antonve](https://github.com/antonve)

# Planning

## Week 1

Evaluatie van bestaande libraries en experimenteren met GPIO

## Week 2

Schrijven van een Python-driver

## Week 3

Front-end en webserver

## Week 4

Interactie back-end met front-end en driver, en afwerken

# Verslag

## Week 1

![De Raspberry Pi, met ingeplugd de ribbon cable, voeding, toetsenbord en HDMI-kabel](board-setup.jpg)

Tijdens de eerste week hebben we de Raspberry Pi opgezet en klaargemaakt. We hebben de [Raspbian](http://www.raspbian.org/) image afgehaald van de [downloadpagina](http://www.raspberrypi.org/downloads/). Unzippen en een `sudo dd bs=4M if~/2015-02-16-wheezy-raspbian.img of=/dev/sdc` later stond Raspbian op het SD-kaartje. Voor de eerste boot verbonden we de Raspberry Pi met een scherm (over HDMI) en een toetsenbord. Veel hebben we niet veranderd bij de installatie, behalve dan het expanden van de image zodat het volledige kaartje gebruikt wordt, en het enablen van de SPI en I2C kernel modules.

Na het rebooten staken we een netwerkkabel in. We voegden `allow-hotplug eth0` en `auto eth0` toe aan `/etc/network/interfaces` en restartten de networkingservice met `sudo service networking restart`. Dat zorgt ervoor dat we de netwerkkabel mogen uittrekken naar believen, Raspbian zal proberen opnieuw te verbinden wanneer hij opnieuw wordt ingestoken.

`sudo ifconfig` vertelde ons alles wat we moesten weten: het IP-adres op het lokale netwerk. Even vreesden we dat we door restricties op het schoolnetwerk niet zouden kunnen SSH'en, maar dat bleek wel te lukken. Na deze stap verwijderden we het scherm en toetsenbord van de Raspberry Pi, aangezien ze weinig nut hadden. De volgende les zullen we wel het scherm moeten insteken om het IP-adres te weten te komen; dat wordt immers via DHCP verkregen. Een oplossing is een service zoals [no-ip](http://www.no-ip.com), maar dat zou ons te ver leiden.

### Soorten pinnummering

Na de set-up konden we beginnen. We sloten de LED-strip aan en bogen ons over de cryptische pinouts van de Rapsberry Pi: er zijn blijkbaar verschillende manieren om de pinnen te nummeren: *physical numbering*, *GPIO numbering* en *BCM numbering*.

#### Physical numbering

De fysieke nummering is het gemakkelijkst: de pinnen volgen een normale nummering. Linksonder begint de nummering bij 1, erboven zit 2, de onderste pin van de twee rij is 3 en zo voort. Een synoniem is board numbering.

#### GPIO numbering

GPIO numbering is hoe de computer de pinnen ziet en lijkt volledig willekeurig te zijn.

#### BCM numbering

BCM lijkt hetzelfde te zijn als GPIO-nummering. De naam komt van de BCM2835-chip op de Raspberry Pi, die gebruikt wordt om de GPIO-pinnen aan te sturen ([bron](https://projects.drogon.net/raspberry-pi/wiringpi/pins/))

### WiringPi numbering

[WiringPi](http://wiringpi.com/) is een C-bibliotheek om te interfacen met de GPIO-pinnen. Alsof er nog niet genoeg verwarring was, besloten ze om hun eigen systeem te gebruiken.

### Keuze

Wij kozen voor de BCM-nummering.

### Ribbon cable pinout

We kregen een bakje met daarin een switch, button en de kerstlichtjes aangesloten. Dit konden we verbinden met de Raspberry Pi door middel van de ribbon cable. Dit is de pinout:

Physical numbering | GPIO/BCM numbering | Component      | LED strip connection
-------------------|--------------------|----------------|---------------------
7                  | 4                  | LED            |
11                 | 17                 | Schakelaar     |
12                 | 18                 | Drukknop       |
15                 | 22                 | Groen          | Clock
16                 | 23                 | Wit            | Data

Voorbeeld van aansturen: de LED in het zwarte doosje is aangesloten op GPIO 4 en physical pin 7. We spreken deze pin aan met BCM-nummering 4.

### Aansturen vanuit Python

We besloten om Python te gebruiken als programmeertaal, vanwege het gemak (we hadden beiden niet veel zin in C) en de goede libraries. Belangrijk is om Python altijd als root te starten (`sudo python` of `sudo python xxx.py`).

#### Inputs

```
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)        # we maken gebruiken van BCM/GPIO-nummering
GPIO.setup(17, GPIO.IN)       # we gebruiken pin 17 als input
GPIO.input(17)                # we vragen de status op van pin 17 (laag of hoog)
```

#### Outputs

```
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)        # we maken gebruiken van BCM/GPIO-nummering
GPIO.setmode(4, GPIO.OUT)     # we gebruiken pin 4 als een output
GPIO.output(4, 1)             # zet pin 4 hoog
```

### Aansturen van de LED-strip

## Week 2

Deze week willen we het aansturen van de LEDs goed krijgen. We moeten continu blijven sturen: de eerste byte zet het rood van de eerste LED, de tweede byte het groen van de eeste LED, de derde byte het blauw van de eerste LED, de vierde byte het rood van de tweede LED, enzovoort. Per LED moeten er dus 24 bits (3 bytes) verstuurd worden. Er moet een pauze van meer dan 500us tussen de verschillende dataframes zitten.

We hebben ook de datasheet van de LED-strip beter bekeken. Hij staat nu [hier](https://drive.google.com/file/d/0B4tGyX3W5HcWVm5PeUJmOElaYTA/view?usp=sharing), maar ook [Adafruit](http://www.adafruit.com/datasheets/WS2801.pdf) heeft hem staan. We vonden de datasheet redelijk verwarrend en onduidelijk, maar dat komt waarschijnlijk omdat we daar niet zo veel ervaring mee hebben.

Deze week hebben we zelf een "driver" geschreven om de LEDstrip aan te sturen. Dat deden we in Python. Het is een simpele library, `led_driver.py`, met kleine functies en enkele constanten die de vaste pinnen voorstellen.

De basis is `write_data`, een functie die een enkele bit aan informatie stuurt. Dat wordt gedaan door eerst de klokpin laag te zetten, dan de data naar de datapin te schrijven en uiteindelijk de klokpin terug hoog te zetten.

Daarnaast zijn nog enkele andere functies voorzien:

* `write_byte` schrijft een volledige byte naar de Raspberry Pi
* `int_to_bit_array` maakt van een getal tussen 0 en 255 een array van bits
* `write_rgb(red, green, blue)` schrijft een kleur weg, de kleuren moeten getallen tussen 0 en 255 zijn
* `write_colors(colors)` schrijft een array van tien elementen weg. De elementen van deze array zijn opnieuw arrays in de vorm `[red, green, blue]`
* `random_color` maakt een willekeurige kleur (geeft een array van 3 getallen tussen 0 en 255 terug)
* `turn_off`, `turn_all_white`, `write_color_to_all(color)`, `turn_all_red`, `turn_all_green`, `turn_all_blue` en `turn_all_to_same_random` doen exact wat je verwacht

Om deze library te gebruiken, doe je `sudo python` en dan `import led_driver` (als die in dezelfde map staat).

## Week 3

In week 3 hebben we gepoogd om een Python daemon op te zetten. De daemon bindt een poort (10000), accepteert alle requests en probeert ze te converteren naar iets dat kan getoond worden op de LEDstrip.

Dat werkte, maar we hadden veel problemen. De LEDstrip update niet altijd alle kleuren.

## Week 4

Dit is de laatste week, vandaag werkten we alles af. Het belangrijkste was nu om de front-end mock-up werkend te krijgen. Daarvoor gebruiken we node.js als server op de Raspberry Pi, die web content serveert en XHR requests zal afleveren aan de Python server.

We begonnen met experimenteren hoe we een TCP-connectie konden maken vanuit node.js. Dat bleek erg makkelijk te zijn:

    $ node
    > var socket = require('net').Socket()
    > socket.connect(10000)
    > socket.write('data hier')
    > socket.end()

En zo zagen we meteen al data aan de Python-kant, node.js was dus een goede kandidaat om de publieke server op te bouwen.

We gebruikten [Express](http://expressjs.com/) als framework bovenop node. Enkele kleine wijzigingen waren nodig aan de Pythonserver (globale status bijhouden van de lichten).

We bleven maar problemen hebben met de Pythondriver. Daarom beslisten we om snel een C-driver te schrijven en die ook te gebruiken. Dat loste al een hoop problemen.

Nu sprak de Pythonserver dus een driver in C aan (gewoon door `os.system`), dat konden we eigenlijk ook in node.js doen, maar daar hadden we geen tijd meer voor. Occasioneel glitcht de LED-strip nog, maar meestal werkt hij perfect.

# Evaluatie

Python was een te trage taal voor dit project, jammer dat we daar zoveel tijd aan verloren hadden. Maar moest de LED-strip aangesloten zijn op de SPI-poort van de Raspberry Pi, zou het volgens ons wel gewerkt hebben.

We hebben veel problemen gehad met timing. De LED-strip glitchte veel en op rare momenten. Dit was heel erg lastig om te debuggen, vooral zonder scope.

Het was ambetant om de ganse tijd te moeten SSHen in de Raspberry Pi, we hadden beter een Sambashare of zo opgezet op de Pi.

Op de een of andere vreemde manier moeten we eerst de node.js server starten, en dan pas de Pythonserver, anders glicht de LEDstrip. Dit is heel raar, omdat die geen interactie met elkaar hebben tot er XHR-requests binnenkomen.

Qua architectuur ziet onze applicatie er zo uit:

    node.js --- XHR request ---> node.js API --- socket ---> Python server --- os.system call ---> C driver --- GPIO libraries ---> LED-strip

Niet ideaal dus. De Pythonserver kunnen we eigenlijk schrappen, en dan kunnen we de C driver aanspreken vanuit node.js. Helaas hebben we daar nu geen tijd meer voor.
