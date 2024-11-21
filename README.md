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
Pro ukončení zmáčkněte ctrl+x a pak y
## 4. Pravidelný běh skriptu
Pro pravidelný běh skriptu použijeme cron job, který zajistí, že skript bude spuštěn každou minutu.

Otevřete soubor pro cron úkoly:
bash
```bash
sudo crontab -e
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
Pokud chcete lepší stránku a automatickou aktualizaci dat udělejte následující:
## Lepší web
Odstraňte soubor /var/www/html/index.html:
```bash
sudo rm /var/www/html/index.html
```
Znovu ho vytvořte:
```bash
sudo nano /var/www/html/index.html
```
A vložte toto
```html
<!DOCTYPE html>
<html lang="cs">

<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Raspberry Pi Status</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            margin: 20px;
            background-color: #f0f0f0;
        }
        
        h1 {
            color: #333;
        }
        
        .status-info {
            font-size: 18px;
            margin-bottom: 10px;
            padding: 10px;
            background-color: #fff;
            border-radius: 8px;
            box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
            max-width: 600px;
            margin: auto;
        }
        
        .progress-container {
            width: 100%;
            height: 30px;
            background-color: #e0e0e0;
            border-radius: 10px;
            margin-top: 10px;
        }
        
        .progress-bar {
            height: 100%;
            border-radius: 10px;
            text-align: center;
            line-height: 30px;
            color: white;
            font-weight: bold;
        }
        
        .cpu-usage {
            background-color: #f44336;
        }
        
        .ram-usage {
            background-color: #4caf50;
        }
        
        .cpu-temp {
            background-color: #2196F3;
        }
    </style>
</head>

<body>
    <h1>Raspberry Pi Status</h1>
    <div id="status" class="status-info">
        Načítám...
    </div>

    <h2>Teplota CPU</h2>
    <div id="cpu-temp-bar" class="progress-container">
        <div id="cpu-temp" class="progress-bar cpu-temp">Načítám...</div>
    </div>

    <h2>Využití CPU</h2>
    <div id="cpu-usage-bar" class="progress-container">
        <div id="cpu-usage" class="progress-bar cpu-usage">Načítám...</div>
    </div>

    <h2>Využití RAM</h2>
    <div id="ram-usage-bar" class="progress-container">
        <div id="ram-usage" class="progress-bar ram-usage">Načítám...</div>
    </div>

    <script>
        function updateStatus() {
            fetch('status.txt')
                .then(response => response.text())
                .then(data => {
                    // Zobrazení celého statusu
                    document.getElementById('status').innerText = data;

                    // Parsování dat
                    const cpuTempMatch = data.match(/Teplota CPU: (\d+(\.\d+)?)/);
                    const cpuUsageMatch = data.match(/Využití CPU: (\d+(\.\d+)?)/);
                    const ramUsageMatch = data.match(/Využití RAM: (\d+(\.\d+)?) MB \/ (\d+(\.\d+)?) MB/);

                    if (cpuTempMatch) {
                        const cpuTemp = parseFloat(cpuTempMatch[1]);
                        updateProgressBar('cpu-temp', cpuTemp, 100, ' °C');
                    }

                    if (cpuUsageMatch) {
                        const cpuUsage = parseFloat(cpuUsageMatch[1]);
                        updateProgressBar('cpu-usage', cpuUsage, 100, ' %');
                    }

                    if (ramUsageMatch) {
                        const ramUsed = parseFloat(ramUsageMatch[1]);
                        const ramTotal = parseFloat(ramUsageMatch[3]);
                        const ramPercent = (ramUsed / ramTotal) * 100;
                        updateProgressBar('ram-usage', ramPercent, 100, ' %');
                    }
                })
                .catch(() => {
                    document.getElementById('status').innerText = "Chyba při načítání dat!";
                });
        }

        function updateProgressBar(elementId, value, max, unit) {
            const progressBar = document.getElementById(elementId);
            const percentage = Math.min((value / max) * 100, 100);
            progressBar.style.width = percentage + '%';
            progressBar.innerText = value.toFixed(1) + unit;
        }

        // Aktualizace každou sekundu
        setInterval(updateStatus, 1000);
        updateStatus();
    </script>
</body>

</html>
```
Zmáčkněte ctrl+x a pak y
## Jak zjistit ip adresu raspberry pi.
Zpustěte příkaz ipconfig
```bash
hostname -I
```
První ip adresa je vaše.


