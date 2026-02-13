from fastapi import FastAPI, Request, Response
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates

import psutil
import time
import platform
from pathlib import Path

try:
    import docker
except Exception:
    docker = None

APP_NAME = "Overengineered"
APP_VERSION = "0.4.0"
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
# Helpers
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
    """
    Prefer host OS if mounted at /host/etc/os-release.
    Falls nicht gemountet, fällt es auf Container-OS zurück.
    """
    host_path = Path("/host/etc/os-release")
    if host_path.exists():
        return _parse_os_release(host_path.read_text(errors="ignore"))

    container_path = Path("/etc/os-release")
    if container_path.exists():
        return _parse_os_release(container_path.read_text(errors="ignore"))

    return {"name": platform.system(), "version": platform.release(), "pretty": None}


def get_docker_stats():
    if docker is None:
        return {"available": False, "error": "python docker package not available"}

    try:
        client = docker.from_env()
        containers_all = client.containers.list(all=True)
        containers_running = client.containers.list()
        names_running = sorted([c.name for c in containers_running])[:15]
        return {
            "available": True,
            "containers_running": len(containers_running),
            "containers_total": len(containers_all),
            "running_names_sample": names_running,
        }
    except Exception as e:
        return {"available": False, "error": str(e)}


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
# Scoring + Memes
# -----------------------
def overkill_score(stats: dict, docker_stats: dict) -> int:
    cpu_idle = max(0.0, 100.0 - stats["cpu_percent"]) / 100.0
    ram_idle = max(0.0, 100.0 - stats["ram_percent"]) / 100.0

    core_factor = min(stats["cpu_cores_logical"] / 8.0, 3.0)
    ram_factor = min(stats["ram_total_gb"] / 16.0, 3.0)

    container_mult = 1.0
    if docker_stats.get("available"):
        running = docker_stats.get("containers_running", 0)
        container_mult = min(1.0 + (running / 10.0), 3.0)

    uptime_days = max(0, int(stats.get("uptime_days", 0)))
    uptime_mult = 1.0 + min(uptime_days / 30.0, 1.0) * 0.25  # up to +25%

    raw = (cpu_idle * 45 + ram_idle * 45) * (0.5 * core_factor + 0.5 * ram_factor) * container_mult * uptime_mult
    return int(min(max(raw, 0), 100))


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


def roast(stats: dict, docker_stats: dict, score: int) -> str:
    running = docker_stats.get("containers_running", 0) if docker_stats.get("available") else 0
    uptime_days = stats.get("uptime_days", 0)

    if uptime_days >= 30:
        return "30+ days uptime. Updates are a myth, right?"
    if docker_stats.get("available") and running == 0:
        return "Docker is available. Nothing is running. The calm before the compose storm."
    if docker_stats.get("available") and running >= 25 and stats["cpu_percent"] < 5:
        return "You collect containers like Pokémon. None of them are evolving."
    if score >= 90:
        return "A monument to ambition and underutilization."
    if score >= 75:
        return "You didn't build a server. You built an ego with fans."
    if score >= 55:
        return "Capable machine, suspiciously calm workload."
    return "Almost responsible. Almost."


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
        {
            "request": request,
            "app_name": APP_NAME,
            "app_version": APP_VERSION,
            "github_url": GITHUB_URL,
        },
    )
    resp.headers["Content-Type"] = "text/html; charset=utf-8"
    return resp


@app.get("/raw", response_class=HTMLResponse)
def raw_ui(request: Request):
    resp = templates.TemplateResponse(
        "raw.html",
        {
            "request": request,
            "app_name": APP_NAME,
            "app_version": APP_VERSION,
            "github_url": GITHUB_URL,
        },
    )
    resp.headers["Content-Type"] = "text/html; charset=utf-8"
    return resp


@app.get("/status")
def get_status():
    stats = get_system_stats()
    dstats = get_docker_stats()
    score = overkill_score(stats, dstats)

    return {
        "overkill_score": score,
        "status": status_label(score),
        "roast": roast(stats, dstats, score),
        "system": stats,
        "docker": dstats,
        "capacity": capacity_estimates(stats),
    }


@app.get("/status.json", response_class=JSONResponse)
def get_status_json():
    return get_status()
