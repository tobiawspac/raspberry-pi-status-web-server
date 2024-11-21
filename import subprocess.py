import subprocess
import psutil
import time

def get_cpu_temperature():
    # Spuštění příkazu pro získání teploty CPU
    temp = subprocess.run(['vcgencmd', 'measure_temp'], capture_output=True>    return temp.stdout.split('=')[1].split("'")[0]

def get_cpu_usage():
    # Získání využití CPU v procentech
    return psutil.cpu_percent(interval=1)

def get_ram_usage():
    # Získání informací o RAM
    ram = psutil.virtual_memory()
    used_ram = ram.used / 1024 / 1024  # Použitá RAM v MB
    total_ram = ram.total / 1024 / 1024  # Celková RAM v MB
    ram_percentage = ram.percent  # Využití RAM v procentech
    return used_ram, total_ram, ram_percentage

while True:
    # Získání teploty CPU
    cpu_temp = get_cpu_temperature()

    # Získání využití CPU
    cpu_usage = get_cpu_usage()

    # Získání využití RAM
    used_ram, total_ram, ram_percentage = get_ram_usage()

    # Výstup do souboru
    with open('/var/www/html/status.txt', 'w', encoding='utf-8') as file:
        file.write(f"Teplota CPU: {cpu_temp} °C\n")
        file.write(f"Využití CPU: {cpu_usage}%\n")
        file.write(f"Využitá RAM: {used_ram:.2f} MB / {total_ram:.2f} MB ({>

   # Zpoždění 1 sekundu
    time.sleep(1)