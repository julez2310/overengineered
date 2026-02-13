/* ================================
   Overengineered content pack
   Loaded via <script src="/static/content.js"></script>
================================ */

const FLAVOR_TAGS = [
  "Almost responsible. Almost.",
  "Suspiciously calm workload.",
  "This machine could do science. You chose vibes.",
  "Uptime maximalism detected.",
  "Compose energy is building...",
  "Everything is stable. That can't be right.",
  "Your server is bored.",
  "Minimal usage, maximal potential.",
  "Quiet fans. Loud dreams.",
  "This is fine. (it never is)",
  "Patch Tuesday is a suggestion.",
  "If it isn't containerized, it doesn't count.",
  "Your dashboards are faster than your decisions.",
  "If it’s not HA, it’s just hope.",
];

const LOCAL_ROASTS = [
  "You could be doing more harm. And yet you choose peace.",
  "A monument to ambition and underutilization.",
  "Compute acquired. Purpose pending.",
  "Your docker-compose files have docker-compose files.",
  "Uptime is high. Courage is higher.",
  "You didn’t build a server. You built a philosophy.",
  "Everything is stable. This worries me.",
  "Silicon was harmed in the making of this lab.",
  "You optimized something nobody asked about.",
  "This dashboard exists because YAML hurt you.",
  "This is suspiciously reasonable. Who are you?",
  "If it works, add monitoring until it doesn't.",
];

const EXCUSES = [
  "I need ECC RAM because my data has feelings.",
  "It’s not a server, it’s a learning environment with fans.",
  "Backups need backups. Then those backups need backups.",
  "RAID isn’t backup, so I need RAID *and* backup. Twice.",
  "This is for high availability. My ego demands it.",
  "The cluster is required to validate my YAML hypotheses.",
  "I need a GPU for… thumbnails. Very important thumbnails.",
  "It’s cheaper than therapy. (debatable)",
  "I’m future-proofing. Against what? Against everything.",
  "More disks = fewer regrets. That’s just physics.",
  "It’s for Pi-hole. Obviously Pi-hole needs a cluster.",
  "I’m self-hosting because privacy. Also control issues.",
  "If I don’t do it, Jeff Bezos wins.",
  "This is a cost-saving measure. Eventually. In 2047.",
  "The SSDs are for latency. The latency is emotional.",
  "I’m practicing for when I accidentally become an SRE.",
  "It’s a staging environment. For my next bad idea.",
  "It’s for ‘resilience’. Mostly against boredom.",
  "This is an educational project. My education is expensive.",
  "It reduces cloud spend. In exchange for electricity guilt.",
  "My monitoring stack needs more RAM to remember my mistakes.",
  "I need NVMe so my graphs feel snappier when I’m sad.",
  "The UPS is for uptime. The uptime is for bragging.",
  "I’m not hoarding. I’m curating a digital museum.",
  "I need another node for failover. The failure is inevitable.",
  "If I don’t host it, it doesn’t exist.",
  "It’s not overkill if it prevents future overkill. Think about it.",
  "I’m scaling out emotionally.",
  "The disks are cheap. My time is not.",
  "This is for logs. Logs are basically historical records.",
  "It’s for Jellyfin transcoding. Totally. Definitely.",
  "I’m building a personal cloud. It rains docker-compose files.",
  "I’m running it locally to reduce latency. And to increase drama.",
];

const HOROSCOPE_BASE = [
  "Today you will add “just one more exporter”.",
  "A random port will be opened. You will call it intentional.",
  "Your reverse proxy yearns for another subdomain.",
  "A container will break. You will call it maintenance.",
  "You will chase 0.1% CPU usage like it owes you money.",
  "You will reorganize labels instead of fixing the root cause.",
  "A service will be temporary. It will outlive civilizations.",
  "Logs will reveal a truth you weren’t ready for.",
  "You will consider Kubernetes. You will survive the urge (maybe).",
  "You will ‘clean up’ containers and create 3 new ones.",
];

const PERSONAS = [
  { id:"rack_philosopher",    name:"Rack Philosopher",    icon:"🧠", desc:"You contemplate airflow patterns and existential YAML questions." },
  { id:"compose_archaeologist",name:"Compose Archaeologist",icon:"🏺", desc:"You dig through docker-compose files from 2019 like ancient scrolls." },
  { id:"uptime_maximalist",   name:"Uptime Maximalist",   icon:"⏳", desc:"Reboots are weakness. The kernel remembers everything." },
  { id:"metric_mystic",       name:"Metric Mystic",       icon:"📊", desc:"If it isn’t graphed, it didn’t happen." },
  { id:"data_monarch",        name:"Data Monarch",        icon:"💾", desc:"Storage is not capacity. Storage is destiny." },
  { id:"yaml_sorcerer",       name:"YAML Sorcerer",       icon:"📜", desc:"Indentation is your spellcasting medium." },
  { id:"idle_aesthetic",      name:"Idle Aesthetician",   icon:"🧘", desc:"Your server is calm. Too calm. Beautifully calm." },
  { id:"security_cultist",    name:"Security Cultist",    icon:"🔐", desc:"You rotate secrets to ward off cosmic threats (and yourself)." },
];
