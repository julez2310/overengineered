# Overengineered ⚙️
A pointless-but-funny self-hosted dashboard that judges your server and assigns it an **Overkill Score**.


---

## What is this?

Overengineered is a lightweight FastAPI dashboard that analyzes your system and Docker environment and gives you:

- 🧠 An **Overkill Score**
- 🐳 Docker container stats
- 🎭 A Homelab **Persona / Title**
- 📊 “What could it do?” capacity estimates
- ☁️ A completely fake **Cloud Delusion Calculator**
- 🔮 A daily Service Horoscope
- 🔥 Press `F` to pay respects
- 🖥 Random syslog-style footer messages
- 💸 Homelab tax calculation
- 🤡 Zero actual usefulness

It’s fast. It’s local. It’s judgmental.

---

## Features

### Core
- Real-time CPU / RAM stats
- Docker container detection (optional)
- Overkill score calculation
- Archetype detection
- JSON API endpoint

### Meme Layer
- Random roasts
- Persona system with icons
- Cloud cost hallucination
- Rationalization meter
- Service horoscope
- Respect counter (press `F`)
- Syslog-style live footer messages

---

## Quickstart (Docker)

Recommended setup (includes Docker stats):

~~~bash
docker run -d \
  --name overengineered \
  -p 8080:8000 \
  -v /var/run/docker.sock:/var/run/docker.sock:ro \
  --restart unless-stopped \
  ghcr.io/julez2310/overengineered:latest
~~~

Open:

http://localhost:8080

---

## Docker Compose

Create `docker-compose.yml`:

~~~yaml
services:
  overengineered:
    image: ghcr.io/julez2310/overengineered:latest
    container_name: overengineered
    ports:
      - "8080:8000"
    volumes:
      - /var/run/docker.sock:/var/run/docker.sock:ro
    restart: unless-stopped
~~~

Start:

~~~bash
docker compose up -d
~~~

---

## Endpoints

| Endpoint | Description |
|----------|------------|
| `/` | Main dashboard |
| `/raw` | Raw output view |
| `/status` | JSON machine-readable status |
| `/health` | Health check |

---

## Security Notice

Mounting:

~~~text
/var/run/docker.sock:/var/run/docker.sock:ro
~~~

gives read access to Docker metadata.

This is common for dashboards but should only be used on trusted systems.

---

## Reverse Proxy

Works fine behind:

- nginx
- Traefik
- Caddy
- OPNsense reverse proxy

Example:

~~~text
https://overengineered.yourdomain.tld → http://host:8080
~~~

---

## Development

~~~bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn main:app --reload --host 0.0.0.0 --port 8000
~~~

---

## Philosophy

Cloud is just someone else’s homelab.

If it’s not containerized, it doesn’t count.

If uptime > 30 days, you’re emotionally invested.

---

## License

MIT

Do whatever you want with it.
If you buy more disks because of this dashboard, that’s on you.

---

## Contributing

PRs welcome:

- More personas
- More excuses
- More syslog messages
- Worse cloud pricing math
- Better memes

---

## Author

GitHub: https://github.com/julez2310
