# Saurons Eye

ESPHome-Projekt für das animierte Auge von Sauron und zwei zusätzliche Uhranzeigen auf einem runden GC9A01-Display (240 × 240).

Unterstützt werden zwei Gerätevarianten:

- ESP32-C3 SuperMini
- ESP32-S3 SuperMini

Beide Varianten verwenden dieselbe Projektlogik. Die unterschiedlichen Display-Pins und Animationsparameter werden in den jeweiligen Geräte-Konfigurationen festgelegt.

## Home-Assistant-Anbindung

Das Gerät bindet die Home-Assistant-Uhrzeit ein und stellt folgende Entitäten bereit:

- **Anzeige** – Display ein- bzw. ausschalten
- **Anzeigemodus** – Auswahl zwischen „Saurons Auge“, analoger Uhr mit Datum und digitaler Uhr mit Datum
- **FPS anzeigen** – Anzeige der aktuellen Bildrate ein- bzw. ausschalten
- **Restart** – Gerät neu starten

Die Uhranzeigen verwenden die von Home Assistant bereitgestellte Zeit. Ist noch keine gültige Uhrzeit verfügbar, zeigt das Display einen entsprechenden Wartehinweis.

## Projektaufbau

Die Projektlogik liegt vollständig in diesem Verzeichnis:

- `hardware.yaml` – Home-Assistant-Entitäten, Zeiteingang, Fonts und Bedienfunktionen
- `main.yaml` – Display-Update, Feuer-/Glutsimulation, Augenanimation sowie analoge und digitale Uhr

Die gerätespezifischen Konfigurationen liegen unter `devices/`:

- `Saurons Eye c3.yaml` – ESP32-C3 SuperMini
- `Saurons Eye s3.yaml` – ESP32-S3 SuperMini

Dort sind Geräteidentität, Display-Pinbelegung und die jeweiligen Animationsparameter definiert. Beide Dateien binden die gemeinsamen Projektdateien aus diesem Verzeichnis ein.

Gemeinsam genutzte Hardware-Grundlagen liegen unter `common/`:

- `base-c3_supermini.yaml` bzw. `base-s3_supermini.yaml` – Board- und ESPHome-Grundkonfiguration
- `GC9A01.yaml` – SPI-Bus und Display-Initialisierung

Die Display-Pinbelegung wird über die jeweilige Geräte-Konfiguration an den gemeinsamen GC9A01-Baustein übergeben.

## Konfiguration und Test

Vom Repository-Root aus lassen sich beide Varianten prüfen und kompilieren:

```sh
esphome config "devices/Saurons Eye c3.yaml"
esphome compile "devices/Saurons Eye c3.yaml"

esphome config "devices/Saurons Eye s3.yaml"
esphome compile "devices/Saurons Eye s3.yaml"
```

Zum Flashen und anschließenden Starten kann statt `compile` jeweils `run` verwendet werden.

Die ESPHome-Secrets müssen lokal im von ESPHome erwarteten Verzeichnis vorhanden sein.
