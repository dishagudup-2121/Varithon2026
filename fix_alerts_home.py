import re

# Fix Alerts.tsx
with open("frontend/src/pages/Alerts.tsx", "r") as f:
    c = f.read()

c = re.sub(
    r'const alertSummary = \[\s*\{[\s\S]*?\}\s*\];',
    'const alertSummary: import("../types").AlertSummaryItem[] = [\n    { id: "critical", title: "Critical", count: 2, trend: "+1", status: "Requires immediate action", severity: "critical", labelKey: "alerts.summary.critical" },\n    { id: "high", title: "High", count: 5, trend: "-2", status: "Monitor closely", severity: "high", labelKey: "alerts.summary.high" },\n    { id: "medium", title: "Medium", count: 12, trend: "Stable", status: "Standard operating procedure", severity: "medium", labelKey: "alerts.summary.medium" },\n    { id: "resolved", title: "Resolved (24h)", count: 18, trend: "+5", status: "Since yesterday", severity: "resolved", labelKey: "alerts.summary.resolved" }\n  ];',
    c
)

with open("frontend/src/pages/Alerts.tsx", "w") as f:
    f.write(c)

# Fix Home.tsx
with open("frontend/src/pages/Home.tsx", "r") as f:
    h = f.read()

h = re.sub(
    r'features\.map\(\s*\(\s*\{\s*icon:\s*Icon,\s*title,\s*subtitle\s*\}\s*:\s*any\s*,\s*index\s*\)\s*=>',
    'features.map(({ icon: Icon, title, subtitle }: { icon: React.ElementType, title: string, subtitle: string }, index: number) =>',
    h
)
h = re.sub(
    r'stats\.map\(\s*\(\s*\{\s*icon:\s*Icon,\s*number,\s*label\s*\}\s*:\s*any\s*,\s*index\s*\)\s*=>',
    'stats.map(({ icon: Icon, number, label }: { icon: React.ElementType, number: string, label: string }, index: number) =>',
    h
)
h = re.sub(
    r'features\.map\(\(\{\s*icon:\s*Icon,\s*title,\s*subtitle\s*\}\s*:\s*any,\s*//\s*eslint-disable-line\s*@typescript-eslint/no-explicit-any\s*\)\s*=>',
    'features.map(({ icon: Icon, title, subtitle }: { icon: React.ElementType, title: string, subtitle: string }) =>',
    h
)
h = re.sub(
    r'stats\.map\(\(\{\s*icon:\s*Icon,\s*number,\s*label\s*\}\s*:\s*any,\s*//\s*eslint-disable-line\s*@typescript-eslint/no-explicit-any\s*\)\s*=>',
    'stats.map(({ icon: Icon, number, label }: { icon: React.ElementType, number: string, label: string }) =>',
    h
)
h = re.sub(r'features\.map\(\(\{\s*icon:\s*Icon,\s*title,\s*subtitle\s*\}\)\s*=>', 'features.map(({ icon: Icon, title, subtitle }: { icon: React.ElementType, title: string, subtitle: string }) =>', h)
h = re.sub(r'stats\.map\(\(\{\s*icon:\s*Icon,\s*number,\s*label\s*\}\)\s*=>', 'stats.map(({ icon: Icon, number, label }: { icon: React.ElementType, number: string, label: string }) =>', h)


with open("frontend/src/pages/Home.tsx", "w") as f:
    f.write(h)

