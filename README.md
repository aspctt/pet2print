# pet2print — Telemetry Dashboard & Demo Data Generator

> This repository is **one component** of the larger PET2Print capstone project
> (a smart desktop appliance that recycles post-consumer PET bottles into 1.75 mm
> 3D-printing filament). It contains the **real-time telemetry dashboard** that
> visualises the extruder's live data, plus a **demo data generator** for running
> the dashboard without the physical machine.

**Live demo:** https://pet2print.netlify.app/

- - -
## Description

A self-contained, browser-based dashboard that subscribes to the extruder's
telemetry over MQTT and displays it in real time. It connects to an MQTT broker
(the project uses HiveMQ Cloud) over secure WebSockets, subscribes to the
`pet2print/telemetry` topic, and renders live readouts for:

- **Temperature** (°C, hot-end)
- **Motor speed** (RPM)
- **Filament diameter** (mm, against a 1.75 mm target)

…plus a live broker connection-status indicator. Connection settings (cluster
host, port, username, password, topic, WebSocket path) are editable in an in-page
settings panel and saved to the browser's `localStorage`, so they persist between
visits.

The whole dashboard is a single `index.html` with the **MQTT.js** client bundled
inline — there is no build step and no backend.

> _This repo is the telemetry/visualisation layer only. The OpenCV optical
> measurement and the ESP32 firmware live elsewhere in the wider project; this
> dashboard simply consumes whatever is published to the telemetry topic._

## How it's used

The dashboard is deployed and ready at **https://pet2print.netlify.app/**.

1. Open the page — it connects to the configured MQTT broker automatically.
2. Open the **settings panel** to enter your own HiveMQ cluster host / port /
   username / password / topic. These save to `localStorage`.
3. Publish telemetry to the topic — from the real ESP32 firmware, or from the
   demo generator below — and the gauges update live.

> **Tip:** set your broker credentials through the settings panel rather than
> hard-coding them, and avoid committing real secrets to the repository.

## Repository layout

```
index.html                       # the dashboard (MQTT.js inlined, no build step)
demo_data_generation/
  fake_data.py                   # publishes mock telemetry to the broker
  start_data_generation.ps1      # Windows one-line launcher (uv run fake_data.py)
```

## Installation & running

### The dashboard
It's a single static file. Either:
- open `index.html` directly in a browser,
- serve the folder with any static server, e.g. `python3 -m http.server 8000`, or
- just use the hosted version at https://pet2print.netlify.app/.

### The demo data generator
`fake_data.py` publishes randomised temperature / RPM / diameter values to the
telemetry topic every 2 seconds, so you can see the dashboard working without the
physical extruder. It uses **[uv](https://docs.astral.sh/uv/)** and declares its
dependency (`paho-mqtt`) inline via PEP 723 script metadata, so uv installs it
automatically — no manual `pip install` or virtualenv needed.

```bash
# from the repo root
uv run demo_data_generation/fake_data.py
```

On Windows you can instead run the launcher:

```powershell
demo_data_generation\start_data_generation.ps1
```

### Dependencies
- A modern web browser (for the dashboard)
- **MQTT.js** — MQTT-over-WebSocket client, bundled inline in `index.html` (MIT)
- An MQTT broker reachable over WebSockets (the project uses **HiveMQ Cloud**)
- **[uv](https://docs.astral.sh/uv/)** + Python — only for the demo generator
  - **paho-mqtt** — fetched automatically by uv (declared inside the script)

Third-party components and their licenses are listed in [NOTICE](./NOTICE).

### Licensing
This work is licensed as follows:
* [GPL 3.0 or later](https://www.gnu.org/licenses/gpl-3.0.en.html). See [here](./LICENSE)
	+ You are free to:
		- Use : unpack and use the material in any computer or device
		- Redistribute : redistribute the original package in any medium
		- Adapt : Reuse, modify or incorporate source code into your works (and redistribute it!) 
	+ Under the following terms:
		- You retain any copyright notices
		- You recognise and respect any trademarks
		- You don't impersonate the authors, neither redistribute a derivative that could be misrepresented as theirs.
		- You credit the author and republish the copyright notices on your works where the code is used.
		- You relicense (and fully comply) your works using GPL 3.0 or any later version
			- This work is offered under GPL 3.0 **or (at your option) any later version**, so you may comply with the terms of GPL 3.0 or any later GPL version published by the Free Software Foundation.
		- You don't mix your work with GPL incompatible works.
Please note the copyrights and trademarks in [NOTICE](./NOTICE)
