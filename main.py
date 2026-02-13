from fastapi import FastAPI, Request, Response
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates

import psutil
import time
import platform
import random
from pathlib import Path
from typing import Dict, List, Tuple

try:
    import docker
except Exception:
    docker = None

APP_NAME = "Overengineered"
APP_VERSION = "0.5.0"
GITHUB_URL = "https://github.com/julez2310"

app = FastAPI(title=APP_NAME, version=APP_VERSION)
templates = Jinja2Templates(directory="templates")


# -----------------------
# Middleware: Cache/Security headers
# -----------------------
@app.middleware("http")
async def add_headers(request: Request, call_next):
    response: Response = await call_next(request)

    if request.url.path in ("/", "/status", "/raw", "/status.json", "/health"):
        response.headers["Cache-Control"] = "no-store"

    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["Referrer-Policy"] = "no-referrer"
    response.headers["Permissions-Policy"] = "geolocation=(), microphone=(), camera=()"

    return response


# -----------------------
# OS detection (host-aware)
# -----------------------
def _parse_os_release(text: str):
    data = {}
    for line in text.splitlines():
        if "=" not in line:
            continue
        k, v = line.split("=", 1)
        data[k.strip()] = v.strip().strip('"')
    pretty = data.get("PRETTY_NAME") or None
    name = data.get("NAME") or platform.system()
    version = data.get("VERSION_ID") or platform.release()
    return {"name": name, "version": version, "pretty": pretty}


def read_os_release():
    # Prefer host OS if mounted (see docker-compose mount /etc/os-release -> /host/etc/os-release)
    host_path = Path("/host/etc/os-release")
    if host_path.exists():
        return _parse_os_release(host_path.read_text(errors="ignore"))

    container_path = Path("/etc/os-release")
    if container_path.exists():
        return _parse_os_release(container_path.read_text(errors="ignore"))

    return {"name": platform.system(), "version": platform.release(), "pretty": None}


# -----------------------
# Collectors
# -----------------------
def get_docker_stats():
    if docker is None:
        return {"available": False, "error": "python docker package not available", "containers_running": 0, "containers_total": 0, "running_names": []}

    try:
        client = docker.from_env()
        containers_all = client.containers.list(all=True)
        containers_running = client.containers.list()
        running_names = sorted([c.name for c in containers_running])
        return {
            "available": True,
            "containers_running": len(containers_running),
            "containers_total": len(containers_all),
            "running_names": running_names,
            "running_names_sample": running_names[:15],
        }
    except Exception as e:
        return {"available": False, "error": str(e), "containers_running": 0, "containers_total": 0, "running_names": []}


def get_system_stats():
    cpu_percent = psutil.cpu_percent(interval=0.35)

    vm = psutil.virtual_memory()
    ram_used_gb = vm.used / (1024**3)
    ram_total_gb = vm.total / (1024**3)
    ram_percent = vm.percent

    boot_time = psutil.boot_time()
    uptime_seconds = time.time() - boot_time
    uptime_days = int(uptime_seconds // 86400)

    cpu_cores_logical = psutil.cpu_count(logical=True) or 1

    osr = read_os_release()

    return {
        "cpu_percent": round(cpu_percent, 1),
        "cpu_cores_logical": cpu_cores_logical,
        "ram_percent": round(ram_percent, 1),
        "ram_used_gb": round(ram_used_gb, 2),
        "ram_total_gb": round(ram_total_gb, 2),
        "uptime_days": uptime_days,
        "os": osr,
    }


# -----------------------
# Archetype Detection
# -----------------------
ARCHETYPES = {
    "Data Hoarder": {
        "desc": "You don't store data. You adopt it. Permanently.",
        "patterns": ["nextcloud", "immich", "photoprism", "syncthing", "minio", "paperless", "seafile"],
        "bonus": 6,
    },
    "Media Lord": {
        "desc": "You stream everything, including your own regret.",
        "patterns": ["plex", "jellyfin", "emby", "tdarr", "sonarr", "radarr", "lidarr", "bazarr"],
        "bonus": 6,
    },
    "Observability Addict": {
        "desc": "If it isn't graphed, it didn't happen.",
        "patterns": ["grafana", "prometheus", "loki", "influxdb", "telegraf", "victoriametrics", "alertmanager"],
        "bonus": 7,
    },
    "Automation Goblin": {
        "desc": "One more automation and your house will start filing taxes.",
        "patterns": ["homeassistant", "node-red", "zigbee2mqtt", "zwave", "mqtt", "esphome"],
        "bonus": 6,
    },
    "Reverse Proxy Purist": {
        "desc": "You route therefore you are.",
        "patterns": ["traefik", "nginx-proxy-manager", "caddy", "haproxy", "nginx"],
        "bonus": 5,
    },
    "Security Paranoid": {
        "desc": "You trust no one. Especially your future self.",
        "patterns": ["authelia", "authentik", "crowdsec", "fail2ban", "wazuh", "vaultwarden"],
        "bonus": 6,
    },
    "Database Collector": {
        "desc": "You run three databases for one todo list.",
        "patterns": ["postgres", "mariadb", "mysql", "redis", "mongodb", "influxdb", "cockroach", "elasticsearch"],
        "bonus": 5,
    },
}

EXTRA_TITLES = [
    "Selfhosted Expert",
    "Homelab Enjoyer",
    "Professional Overthinker",
    "Uptime Maximalist",
    "Compose Archaeologist",
    "Rack Philosopher",
]


def detect_archetypes(container_names: List[str]) -> Dict:
    names = [n.lower() for n in container_names]
    hits: List[Tuple[str, int]] = []
    details = []

    for name, meta in ARCHETYPES.items():
        patterns = meta["patterns"]
        match_count = sum(1 for p in patterns if any(p in cn for cn in names))
        if match_count > 0:
            strength = match_count
            hits.append((name, strength))
            details.append({
                "name": name,
                "strength": strength,
                "bonus": meta["bonus"],
                "desc": meta["desc"],
            })

    # pick primary + secondary
    details_sorted = sorted(details, key=lambda d: (d["strength"], d["bonus"]), reverse=True)
    primary = details_sorted[0] if details_sorted else None
    secondary = details_sorted[1] if len(details_sorted) > 1 else None

    title = random.choice(EXTRA_TITLES)

    # compute bonus from unique archetypes detected (capped)
    bonus = 0
    for d in details_sorted:
        bonus += d["bonus"]
    bonus = min(bonus, 20)

    return {
        "title": title,
        "primary": primary,
        "secondary": secondary,
        "all": details_sorted,
        "score_bonus": bonus,
    }


# -----------------------
# Scoring + Memes
# -----------------------
BASE_ROASTS = [
    "Almost responsible. Almost.",
    "This is suspiciously reasonable. Who are you?",
    "Your server is calm. Too calm.",
    "Everything looks stable. That can't be right.",
    "You could be doing more harm. And yet you choose peace.",
    "Minimal usage detected. Maximum potential ignored.",
    "A surprisingly adult configuration. Disturbing.",
    "Quiet fans. Quiet conscience.",
]

UPTIME_ROASTS = [
    "30+ days uptime. Updates are a myth, right?",
    "Uptime is high. Patch anxiety is higher.",
    "Reboots are lava.",
    "You haven't rebooted in a while. The kernel is emotionally attached now.",
]

DOCKER_ROASTS = [
    "Docker is available. Nothing is running. The calm before the compose storm.",
    "Zero running containers. Your CPU is bored.",
    "Your containers are either sleeping or plotting.",
]

OVERKILL_ROASTS = [
    "A monument to ambition and underutilization.",
    "You didn't build a server. You built an ego with fans.",
    "This machine could do science. You're doing vibes.",
    "You have compute. You have dreams. You run a dashboard.",
]

CONTAINER_HOARDER_ROASTS = [
    "You collect containers like Pokémon. None of them are evolving.",
    "So many containers. So little accountability.",
    "Your docker-compose files have their own docker-compose files.",
]


def pick_roast(stats: dict, docker_stats: dict, score: int, arche: dict) -> str:
    running = docker_stats.get("containers_running", 0) if docker_stats.get("available") else 0
    uptime_days = stats.get("uptime_days", 0)

    candidates = list(BASE_ROASTS)

    if uptime_days >= 30:
        candidates += UPTIME_ROASTS

    if docker_stats.get("available") and running == 0:
        candidates += DOCKER_ROASTS

    if docker_stats.get("available") and running >= 25 and stats["cpu_percent"] < 5:
        candidates += CONTAINER_HOARDER_ROASTS

    if score >= 75:
        candidates += OVERKILL_ROASTS

    # archetype flavor
    if arche.get("primary"):
        candidates.append(f'Primary archetype: {arche["primary"]["name"]}. {arche["primary"]["desc"]}')
    if arche.get("secondary"):
        candidates.append(f'Secondary: {arche["secondary"]["name"]}.')

    return random.choice(candidates)


def overkill_score(stats: dict, docker_stats: dict, arche: dict) -> int:
    cpu_idle = max(0.0, 100.0 - stats["cpu_percent"]) / 100.0
    ram_idle = max(0.0, 100.0 - stats["ram_percent"]) / 100.0

    core_factor = min(stats["cpu_cores_logical"] / 8.0, 3.0)
    ram_factor = min(stats["ram_total_gb"] / 16.0, 3.0)

    container_mult = 1.0
    if docker_stats.get("available"):
        running = docker_stats.get("containers_running", 0)
        container_mult = min(1.0 + (running / 10.0), 3.0)

    uptime_days = max(0, int(stats.get("uptime_days", 0)))
    uptime_mult = 1.0 + min(uptime_days / 30.0, 1.0) * 0.25

    raw = (cpu_idle * 45 + ram_idle * 45) * (0.5 * core_factor + 0.5 * ram_factor) * container_mult * uptime_mult
    base = int(min(max(raw, 0), 100))

    # Add archetype bonus (capped), then clamp to 100
    bonus = int(arche.get("score_bonus", 0))
    return min(100, base + bonus)


def status_label(score: int) -> str:
    if score >= 90:
        return "ABSOLUTELY UNNECESSARY"
    if score >= 75:
        return "OVERKILL ENERGY"
    if score >= 55:
        return "SUSPICIOUSLY CAPABLE"
    if score >= 35:
        return "REASONABLE"
    return "MODEST"


def capacity_estimates(stats: dict) -> dict:
    idle_ram_gb = max(0.0, stats["ram_total_gb"] - stats["ram_used_gb"])
    cores = max(1, int(stats["cpu_cores_logical"]))

    service_ram = {
        "minecraft": 2.0,
        "nginx": 0.05,
        "pihole": 0.25,
        "immich": 2.5,
        "vaultwarden": 0.2,
        "homeassistant": 0.6,
        "grafana": 0.4,
        "prometheus": 1.0,
        "jellyfin": 1.5,
        "paperless": 0.8,
        "nextcloud": 1.0,
    }

    def by_ram(key: str) -> int:
        return int(idle_ram_gb // service_ram[key]) if service_ram[key] > 0 else 0

    return {
        "idle_ram_gb_est": round(idle_ram_gb, 2),
        "services": {
            "minecraft": {"label": "Minecraft servers", "count": by_ram("minecraft")},
            "nginx": {"label": "nginx instances", "count": min(by_ram("nginx"), cores * 200)},
            "pihole": {"label": "Pi-hole instances", "count": by_ram("pihole")},
            "immich": {"label": "Immich instances", "count": min(by_ram("immich"), cores * 2)},
            "vaultwarden": {"label": "Vaultwarden instances", "count": by_ram("vaultwarden")},
            "homeassistant": {"label": "Home Assistant instances", "count": min(by_ram("homeassistant"), cores * 3)},
            "grafana": {"label": "Grafana instances", "count": by_ram("grafana")},
            "prometheus": {"label": "Prometheus instances", "count": min(by_ram("prometheus"), cores * 2)},
            "jellyfin": {"label": "Jellyfin instances", "count": min(by_ram("jellyfin"), cores * 2)},
            "paperless": {"label": "Paperless-ngx instances", "count": min(by_ram("paperless"), cores * 2)},
            "nextcloud": {"label": "Nextcloud instances", "count": min(by_ram("nextcloud"), cores * 2)},
        },
    }


# -----------------------
# Routes
# -----------------------
@app.get("/health")
def health():
    return {"ok": True, "name": APP_NAME, "version": APP_VERSION}


@app.get("/", response_class=HTMLResponse)
def ui(request: Request):
    resp = templates.TemplateResponse(
        "index.html",
        {"request": request, "app_name": APP_NAME, "app_version": APP_VERSION, "github_url": GITHUB_URL},
    )
    resp.headers["Content-Type"] = "text/html; charset=utf-8"
    return resp


@app.get("/raw", response_class=HTMLResponse)
def raw_ui(request: Request):
    resp = templates.TemplateResponse(
        "raw.html",
        {"request": request, "app_name": APP_NAME, "app_version": APP_VERSION, "github_url": GITHUB_URL},
    )
    resp.headers["Content-Type"] = "text/html; charset=utf-8"
    return resp


@app.get("/status")
def get_status():
    stats = get_system_stats()
    dstats = get_docker_stats()
    arche = detect_archetypes(dstats.get("running_names", []))
    score = overkill_score(stats, dstats, arche)

    return {
        "overkill_score": score,
        "status": status_label(score),
        "roast": pick_roast(stats, dstats, score, arche),
        "system": stats,
        "docker": {
            "available": dstats.get("available"),
            "containers_running": dstats.get("containers_running"),
            "containers_total": dstats.get("containers_total"),
            "running_names_sample": dstats.get("running_names_sample", []),
        },
        "archetype": arche,
        "capacity": capacity_estimates(stats),
    }


@app.get("/status.json", response_class=JSONResponse)
def get_status_json():
    return get_status()
