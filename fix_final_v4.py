import re

def fix_re(path, pattern, replace):
    with open(path, "r") as f:
        c = f.read()
    c = re.sub(pattern, replace, c)
    with open(path, "w") as f:
        f.write(c)

def fix(path, search, replace):
    with open(path, "r") as f:
        c = f.read()
    if search in c:
        c = c.replace(search, replace)
        with open(path, "w") as f:
            f.write(c)

# Alerts.tsx mock data
alerts_path = "frontend/src/pages/Alerts.tsx"
with open(alerts_path, "r") as f:
    alerts_code = f.read()

# Replace the array with proper types
alerts_code = re.sub(r'const summaryStats = \[\s*\{[\s\S]*?\}\s*\];', 'const summaryStats: import("../types").AlertSummaryItem[] = [\n    { id: "critical", title: "Critical", count: 2, trend: "+1", status: "Requires immediate action", severity: "critical", labelKey: "alerts.summary.critical" },\n    { id: "high", title: "High", count: 5, trend: "-2", status: "Monitor closely", severity: "high", labelKey: "alerts.summary.high" },\n    { id: "medium", title: "Medium", count: 12, trend: "Stable", status: "Standard operating procedure", severity: "medium", labelKey: "alerts.summary.medium" },\n    { id: "resolved", title: "Resolved (24h)", count: 18, trend: "+5", status: "Since yesterday", severity: "resolved", labelKey: "alerts.summary.resolved" }\n  ];', alerts_code)

alerts_code = alerts_code.replace('selectedAlert && (<AlertDetails', 'selectedAlert !== null && (<AlertDetails alert={selectedAlert as import("../types").Alert}')
alerts_code = alerts_code.replace('selectedAlert && (\n          <AlertDetails\n            alert={selectedAlert}', 'selectedAlert !== null && (\n          <AlertDetails\n            alert={selectedAlert as import("../types").Alert}')

with open(alerts_path, "w") as f:
    f.write(alerts_code)

# Dashboard.tsx
fix("frontend/src/pages/Dashboard.tsx", "const handleKPIAction = (statId) => {", "const handleKPIAction = (statId: string) => {")

# Signup.tsx
fix("frontend/src/pages/Signup.tsx", "const handleLanguageChange = (language) => {", "const handleLanguageChange = (language: string) => {")

# Simulation.tsx
fix("frontend/src/pages/Simulation.tsx", 'selectedScenario === "deploy_ambulance"', 'selectedScenario?.id === "deploy_ambulance"')

# Home.tsx
home_path = "frontend/src/pages/Home.tsx"
with open(home_path, "r") as f:
    home_code = f.read()

home_code = re.sub(r'features\.map\(\s*\(\s*\{\s*icon:\s*Icon,\s*title,\s*subtitle\s*\}\s*\)\s*=>', 'features.map(({ icon: Icon, title, subtitle }: { icon: any, title: string, subtitle: string }) =>', home_code)
home_code = re.sub(r'stats\.map\(\s*\(\s*\{\s*icon:\s*Icon,\s*number,\s*label\s*\}\s*\)\s*=>', 'stats.map(({ icon: Icon, number, label }: { icon: any, number: string, label: string }) =>', home_code)
home_code = re.sub(r'features\.map\(\s*\(\{\s*icon:\s*Icon,\s*title,\s*subtitle\s*\}\s*,\s*index\s*\)\s*=>', 'features.map(({ icon: Icon, title, subtitle }: { icon: any, title: string, subtitle: string }, index: number) =>', home_code)
home_code = re.sub(r'stats\.map\(\s*\(\{\s*icon:\s*Icon,\s*number,\s*label\s*\}\s*,\s*index\s*\)\s*=>', 'stats.map(({ icon: Icon, number, label }: { icon: any, number: string, label: string }, index: number) =>', home_code)
# Let's just catch all variations without "any"
home_code = home_code.replace("features.map(({ icon: Icon, title, subtitle }) =>", "features.map(({ icon: Icon, title, subtitle }: { icon: React.ElementType, title: string, subtitle: string }) =>")
home_code = home_code.replace("stats.map(({ icon: Icon, number, label }) =>", "stats.map(({ icon: Icon, number, label }: { icon: React.ElementType, number: string, label: string }) =>")

with open(home_path, "w") as f:
    f.write(home_code)

