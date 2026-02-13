/* ================================
   CONTENT CONFIG (All the nonsense)
================================ */

/* Flavor lines behind the status */
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
  "If it isn't containerized, it doesn't count."
];

/* Local vibe roasts */
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
  "This dashboard exists because YAML hurt you."
];

/* Excuse generator */
const EXCUSES = [
  "I need ECC RAM because my data has feelings.",
  "It’s not a server, it’s a learning environment with fans.",
  "Backups need backups. Then those backups need backups.",
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
  "It’s a staging environment. For my next bad idea."
];

/* Horoscope base */
const HOROSCOPE_BASE = [
  "Today you will add just one more exporter.",
  "A random port will be opened. You will call it intentional.",
  "Your reverse proxy yearns for another subdomain.",
  "A container will break. You will call it maintenance.",
  "You will chase 0.1% CPU usage like it owes you money.",
  "You will reorganize labels instead of fixing the root cause.",
  "A service will be temporary. It will outlive civilizations.",
  "Logs will reveal a truth you weren’t ready for."
];

/* =================================
   PERSONA SYSTEM
================================= */

const PERSONAS = [
  {
    id: "rack_philosopher",
    name: "Rack Philosopher",
    icon: "🧠",
    description: "You contemplate airflow patterns and existential YAML questions."
  },
  {
    id: "compose_archaeologist",
    name: "Compose Archaeologist",
    icon: "🏺",
    description: "You dig through docker-compose files from 2019 like ancient scrolls."
  },
  {
    id: "uptime_maximalist",
    name: "Uptime Maximalist",
    icon: "⏳",
    description: "Reboots are weakness. The kernel remembers everything."
  },
  {
    id: "metric_mystic",
    name: "Metric Mystic",
    icon: "📊",
    description: "If it isn't graphed, it didn't happen."
  },
  {
    id: "data_monarch",
    name: "Data Monarch",
    icon: "💾",
    description: "Storage is not capacity. Storage is destiny."
  },
  {
    id: "yaml_sorcerer",
    name: "YAML Sorcerer",
    icon: "📜",
    description: "Indentation is your spellcasting medium."
  }
];
