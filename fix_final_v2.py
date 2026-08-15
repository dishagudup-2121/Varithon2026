import re

def fix(path, search, replace):
    with open(path, "r") as f:
        c = f.read()
    if search in c:
        c = c.replace(search, replace)
        with open(path, "w") as f:
            f.write(c)
    else:
        print(f"Warning: '{search}' not found in {path}")

def fix_re(path, pattern, replace):
    with open(path, "r") as f:
        c = f.read()
    c = re.sub(pattern, replace, c)
    with open(path, "w") as f:
        f.write(c)

# 1. Update types/index.ts
types_path = "frontend/src/types/index.ts"
with open(types_path, "r") as f:
    types = f.read()

types = types.replace("export interface Alert {", "export interface Alert {\n  status?: string;\n  zone?: string;\n  riskScore?: number;\n  predictedTime?: string;\n  recommendationKey?: string;")
types = types.replace("export interface AlertSummaryItem {", "export interface AlertSummaryItem {\n  id?: string;\n  title?: string;\n  trend?: string;\n  status?: string;\n  value?: string;")
types = types.replace("export interface Suggestion {", "export interface Suggestion {\n  id?: string;\n  textKey?: string;")

with open(types_path, "w") as f:
    f.write(types)

# 2. AlertCard.tsx
fix("frontend/src/components/alerts/AlertCard.tsx", "export default function AlertCard({ alert, onView }: { alert: Alert; onView?: () => void }) {", "export default function AlertCard({ alert, onView }: { alert: Alert; onView?: (alert: Alert) => void }) {")
fix("frontend/src/components/alerts/AlertCard.tsx", "export default function AlertCard({ alert, onView }: { alert: Alert, onView: () => void }) {", "export default function AlertCard({ alert, onView }: { alert: Alert, onView?: (alert: Alert) => void }) {")
# Fix config colors type
fix("frontend/src/components/alerts/AlertCard.tsx", "const config = colors[alert.severity];", "const config = colors[alert.severity as keyof typeof colors];")
fix("frontend/src/components/alerts/AlertCard.tsx", "const config = colors[alert.severity as keyof typeof colors];", "const config = colors[alert.severity as keyof typeof colors] || colors.medium;")

# 3. HowItWorks.tsx (feature is string!)
fix("frontend/src/components/common/HowItWorks.tsx", "feature: HowItWorksFeature;", "feature: string;")
# Remove unused imports if any, but it's fine.
fix("frontend/src/components/common/HowItWorks.tsx", "const Icon = icons[feature.icon as keyof typeof icons] || Play;", "")
fix("frontend/src/components/common/HowItWorks.tsx", "const Icon = icons[feature.icon] || Play;", "")
# the content is `const content = howItWorksData[feature];`
# we need to render `content.icon`
fix("frontend/src/components/common/HowItWorks.tsx", "<Icon size={24} />", "{(() => { const Icon = (icons as any)[content.icon] || Play; return <Icon size={24} />; })()}")

# 4. SuggestionButton.tsx
fix("frontend/src/components/assistant/SuggestionButton.tsx", "suggestion: string;", "suggestion: { id?: string; textKey?: string; text?: string; };")

# 5. AlertsPanel.tsx
fix_re("frontend/src/components/dashboard/AlertsPanel.tsx", r'alerts\.map\(\(alert\)\s*=>', 'alerts.map((alert: Alert) =>')
fix("frontend/src/components/dashboard/AlertsPanel.tsx", "const Icon = icons[alert.type as keyof typeof icons] || AlertTriangle", "const Icon = icons[alert.type as keyof typeof icons] || AlertTriangle")
fix("frontend/src/components/dashboard/AlertsPanel.tsx", "const Icon = icons[alert.type]", "const Icon = (icons as any)[alert.type] || AlertTriangle")

# 6. Alerts.tsx
fix("frontend/src/pages/Alerts.tsx", "selectedAlert && (", "selectedAlert !== null && (")

# 7. Dashboard.tsx
fix("frontend/src/pages/Dashboard.tsx", "const handleKPIAction = (statId) => {", "const handleKPIAction = (statId: string) => {")

# 8. Home.tsx
fix_re("frontend/src/pages/Home.tsx", r'features\.map\(\s*\(\s*\{\s*icon:\s*Icon,\s*title,\s*subtitle\s*\}\s*\)\s*=>', 'features.map(({ icon: Icon, title, subtitle }: { icon: React.ElementType, title: string, subtitle: string }) =>')
fix_re("frontend/src/pages/Home.tsx", r'stats\.map\(\s*\(\s*\{\s*icon:\s*Icon,\s*number,\s*label\s*\}\s*\)\s*=>', 'stats.map(({ icon: Icon, number, label }: { icon: React.ElementType, number: string, label: string }) =>')

# 9. Signup.tsx
fix("frontend/src/pages/Signup.tsx", "const handleLanguageChange = (language) => {", "const handleLanguageChange = (language: string) => {")

# 10. Simulation.tsx
fix("frontend/src/pages/Simulation.tsx", "selectedScenario === \"deploy_ambulance\"", "selectedScenario?.id === \"deploy_ambulance\"")

