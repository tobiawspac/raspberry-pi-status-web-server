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

A vlož tohle.

```python
import subprocess

def get_cpu_temperature():
    # Spuštění příkazu pro získání teploty CPU
    temp = subprocess.run(['vcgencmd', 'measure_temp'], capture_output=True, text=True)
    return temp.stdout.split('=')[1].split("'")[0]

def get_cpu_usage():
    # Spuštění příkazu pro získání využití CPU
    cpu_usage = subprocess.run(['top', '-bn1', '|', 'grep', '"Cpu(s)"', '|', 'sed', 's/.*, *\([0-9.]*\)%*id.*/\1/', '|', 'awk', '{print 100 - $1 "%"}'], capture_output=True, text=True)
    return cpu_usage.stdout.strip()

def get_ram_usage():
    # Spuštění příkazu pro získání využití RAM
    ram_usage = subprocess.run(['free', '-h', '|', 'grep', 'Mem', '|', 'awk', '{print $3 "/" $2}'], capture_output=True, text=True)
    return ram_usage.stdout.strip()

# Získání teploty CPU
cpu_temp = get_cpu_temperature()

# Získání využití CPU a RAM
cpu_usage = get_cpu_usage()
ram_usage = get_ram_usage()

# Výstup do konzole
print(f"Aktuální teplota CPU: {cpu_temp} °C")
print(f"Využití CPU: {cpu_usage}")
print(f"Využití RAM: {ram_usage}")

# Uložení informací do souboru
with open('/var/www/html/system_usage.txt', 'w', encoding='utf-8') as file:
    file.write(f"Teplota CPU: {cpu_temp} °C\n")
    file.write(f"Využití CPU: {cpu_usage}\n")
    file.write(f"Využití RAM: {ram_usage}\n")
```
Zmáčkněte 1 a vložte toto:
```bash
* * * * * python3 /var/www/html/cpu_ram_monitor.py
```
## 5. Zobrazení informací
Uložené informace o teplotě CPU a využití RAM a CPU můžete zobrazit na webové stránce. V prohlížeči otevřete adresu:

```arduino
http://<IP_adresa_Raspberry_Pi>/system_usage.txt
```
Tento soubor bude obsahovat aktuální hodnoty teploty CPU, využití CPU a využití RAM ve formátu:

```yaml
Zkopírovat kód
Teplota CPU: XX.X °C
Využití CPU: XX%
Využití RAM: X.X/X.X GB
```
