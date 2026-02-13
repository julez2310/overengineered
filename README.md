# Overengineered

A self-hosted dashboard that measures how unnecessary your homelab actually is.

## Run (dev)

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn main:app --host 0.0.0.0 --port 8000 --reload

Open: http://<server-ip>:8000

Endpoints

/ UI

/status JSON API


---

## 5) Start-Befehl

```bash
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
