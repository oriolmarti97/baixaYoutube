# baixaYoutube
## Descripció
Software gràfic que serveix per descarregar vídeos de YouTube i altres plataformes de vídeo

## Requeriments:
El llenguatge de programació usat per desenvolupar aquest programa és **Python 3**. Cal tenir-lo instal·lat per executar el programa
La llibreria utilitzada per crear la interfície gràfica del programa és **PyQt5**. Cal tenir-la instal·lada per executar el programa. Normalment el més fàcil és instal·lar-la fent servir pip
> pip3 install PyQt5

Per realitzar la descàrrega s'utilitza el software **[youtube-dl](https://github.com/ytdl-org/youtube-dl)**. Podeu instal·lar-lo utilitzant pip, o bé seguint els passos que explica [aquí](https://github.com/ytdl-org/youtube-dl#installation)

## Instal·lació
Un cop es té instal·lat **Python 3**, **PyQt5** i **youtube-dl** toca instal·lar baixaYoutube
### Unix-like (GNU/Linux o macOS)
Per instal·lar-lo a un sistema decent (AKA: un sistema basat en Unix) utilitzarem la terminal i les comandes següents
>sudo wget https://raw.githubusercontent.com/oriolmarti97/baixaYoutube/master/baixaYoutube.py -O /usr/local/bin/baixayoutube
sudo chmod a+rx /usr/local/bin/baixayoutube

Alternativament, si no tenim wget disponible, podem fer servir cURL
>sudo curl -L https://raw.githubusercontent.com/oriolmarti97/baixaYoutube/master/baixaYoutube.py -o /usr/local/bin/baixayoutube
sudo chmod a+rx /usr/local/bin/baixayoutube

Fet això ja podrem executar el programa des d'una terminal, amb la comanda **baixayoutube**. Per tenir-ne un accés directe, es poden utilitzar eines com gnome-desktop-item-edit o algun equivalent
### Windows
L'opció més senzilla és desinstal·lar Windows i passar a utilitzar GNU/Linux, apostant així pel Software Lliure. No obstant, es pot seguir executant el programa. Les opcions són les següents 
**-Activar el subsistema Linux**
A Windows 10 existeix el subsistema Linux, que serveix per poder executar software de Linux dins del Windows. Es pot configurar i aleshores fer els passos com si fóssim en un sistema GNU/Linux
**-Crear un .exe**
Aquesta opció consisteix en crear un .exe a partir del codi Python. Tinc previst crear-ne un en algun moment, però pel moment no està fet. Si algú ho fa i me'l vol passar, pot fer una pull request
### Altres plataformes
Per desgràcia, no sé si això pot funcionar en altres plataformes. Convido a intentar-ho a qui vulgui, i a informar-me dels progressos realitzats
