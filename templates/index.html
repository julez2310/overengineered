from fastapi import FastAPI, Request, Response
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

import psutil
import time

try:
    import docker
except Exception:
    docker = None

app = FastAPI(title="Overengineered", version="0.2.2")
templates = Jinja2Templates(directory="templates")


# -----------------------
# Middleware: Cache/Security headers
# -----------------------
@app.middleware("http")
async def add_headers(request: Request, call_next):
    response: Response = await call_next(request)

    # Cache: don't cache the dashboard/status (keeps values fresh)
    if request.url.path in ("/", "/status"):
        response.headers["Cache-Control"] = "no-store"

    # Security headers (safe defaults)
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["Referrer-Policy"] = "no-referrer"
    response.headers["Permissions-Policy"] = "geolocation=(), microphone=(), camera=()"

    return response


# -----------------------
# Collectors
# -----------------------
def get_system_stats():
    cpu_percent = psutil.cpu_percent(interval=0.5)

    vm = psutil.virtual_memory()
    ram_used_gb = vm.used / (1024**3)
    ram_total_gb = vm.total / (1024**3)
    ram_percent = vm.percent

    boot_time = psutil.boot_time()
    uptime_seconds = time.time() - boot_time
    uptime_days = int(uptime_seconds // 86400)

    cpu_cores_logical = psutil.cpu_count(logical=True) or 1

    return {
        "cpu_percent": round(cpu_percent, 1),
        "cpu_cores_logical": cpu_cores_logical,
        "ram_percent": round(ram_percent, 1),
        "ram_used_gb": round(ram_used_gb, 2),
        "ram_total_gb": round(ram_total_gb, 2),
        "uptime_days": uptime_days,
    }


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

    raw = (cpu_idle * 45 + ram_idle * 45) * (0.5 * core_factor + 0.5 * ram_factor) * container_mult
    return int(min(max(raw, 0), 100))


def status_label(score: int) -> str:
    if score >= 90:
        return "ABSOLUTELY UNNECESSARY"
    if score >= 75:
        return "OVERKILL ENERGY"
    if score >= 55:
        return "SUSPICIOUSLY CAPABLE"
    if score >= 35:
        return "REASONABLE (ARE YOU OK?)"
    return "SURPRISINGLY MODEST"


def roast(stats: dict, docker_stats: dict, score: int) -> str:
    running = docker_stats.get("containers_running", 0) if docker_stats.get("available") else 0

    if docker_stats.get("available") and running >= 25 and stats["cpu_percent"] < 5:
        return "You collect containers like Pokémon. None of them are evolving."
    if stats["ram_total_gb"] >= 128 and stats["ram_percent"] < 15:
        return "You bought enterprise RAM to host vibes. Respect."
    if stats["cpu_cores_logical"] >= 32 and stats["cpu_percent"] < 5:
        return "This CPU could run a small country. You're running... a dashboard."
    if stats["uptime_days"] >= 200:
        return "Uptime is high. Patch anxiety is higher."
    if docker_stats.get("available") and running == 0:
        return "Docker is available, but nothing is running. A calm before the compose storm."
    if score >= 90:
        return "Your homelab is a monument to ambition and underutilization."
    if score >= 75:
        return "You didn't build a server. You built an ego with fans."
    if score >= 55:
        return "Capable machine, suspiciously calm workload."
    return "Honestly? This is almost responsible. Almost."


def what_could_it_do(stats: dict):
    idle_ram_gb = max(0.0, stats["ram_total_gb"] - stats["ram_used_gb"])
    minecraft_servers = int(idle_ram_gb // 2)
    nginx_instances = int(stats["cpu_cores_logical"] * 20)

    return {
        "idle_ram_gb_est": round(idle_ram_gb, 2),
        "could_run": [
            f"{minecraft_servers} Minecraft servers (probably)",
            f"{nginx_instances} nginx instances (definitely unnecessary)",
            "one more monitoring stack (because you can)",
        ],
    }


# -----------------------
# Routes
# -----------------------
@app.get("/", response_class=HTMLResponse)
def ui(request: Request):
    # Ensure UTF-8 Content-Type for HTML
    resp = templates.TemplateResponse("index.html", {"request": request})
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
        "what_could_it_do": what_could_it_do(stats),
    }
