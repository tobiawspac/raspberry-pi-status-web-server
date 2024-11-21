# Raspberry Pi CPU Temperature Monitor

Tento projekt slouží k monitorování teploty CPU na Raspberry Pi. Program získává aktuální teplotu CPU a ukládá ji do souboru, který je následně dostupný přes webový server.

## Funkce
- Získávání aktuální teploty CPU z Raspberry Pi.
- Ukládání teploty do textového souboru (`teplota.txt`).
- Zobrazení teploty na webové stránce pomocí Apache web serveru.

## Požadavky
- Raspberry Pi s Raspbian OS (nebo kompatibilní distribuce).
- Apache web server.
- Python 3.
- Program `vcgencmd` pro získávání teploty CPU (standardně dostupný na Raspberry Pi).

## Instalace

### 1. Instalace Apache
Nejprve je potřeba nainstalovat Apache web server:

```bash
sudo apt update
sudo apt install apache2
```
## 2. Instalace Pythonu
Pokud nemáš nainstalovaný Python 3, nainstaluj ho pomocí:

```bash
sudo apt install python3
```
## 3. Skript pro monitorování teploty
Stáhni nebo vytvoř soubor `cpu_temperature_monitor.py` do složky `/var/www/html/`:

```bash
sudo nano /var/www/html/cpu_temperature_monitor.py
```

