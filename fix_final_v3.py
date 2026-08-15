import re

def fix(path, search, replace):
    with open(path, "r") as f:
        c = f.read()
    if search in c:
        c = c.replace(search, replace)
        with open(path, "w") as f:
            f.write(c)

def fix_re(path, pattern, replace):
    with open(path, "r") as f:
        c = f.read()
    c = re.sub(pattern, replace, c)
    with open(path, "w") as f:
        f.write(c)

# Fix types/index.ts optionals
types_path = "frontend/src/types/index.ts"
with open(types_path, "r") as f:
    t = f.read()
t = t.replace("status?: string;", "status: string;")
t = t.replace("zone?: string;", "zone: string;")
t = t.replace("riskScore?: number;", "riskScore: number;")
t = t.replace("predictedTime?: string;", "predictedTime: string;")
t = t.replace("recommendationKey?: string;", "recommendationKey: string;")
t = t.replace("id?: string;", "id: string;")
t = t.replace("title?: string;", "title: string;")
t = t.replace("trend?: string;", "trend: string;")
t = t.replace("value?: string;", "value: string;")
with open(types_path, "w") as f:
    f.write(t)

# Fix SuggestionButton.tsx
fix("frontend/src/components/assistant/SuggestionButton.tsx", "suggestion: { id?: string; textKey?: string; text?: string; };", "suggestion: string;")

# Fix AlertsPanel.tsx
fix("frontend/src/components/dashboard/AlertsPanel.tsx", "const handleAlertClick = (alert) => {", "const handleAlertClick = (alert: Alert) => {")

# Fix HowItWorks.tsx
hiw_path = "frontend/src/components/common/HowItWorks.tsx"
with open(hiw_path, "r") as f:
    hiw = f.read()
hiw = hiw.replace("import { HowItWorksFeature } from '../../types';", "")
hiw = hiw.replace("feature: HowItWorksFeature;", "feature: string;")
hiw = hiw.replace("const content = howItWorksData[feature.id];", "const content = howItWorksData[feature];")
hiw = re.sub(r'const Icon = icons\[feature\.icon.*?Play;', '', hiw)
hiw = hiw.replace("<Icon size={24} />", "{(() => { const Icon = (icons as any)[content.icon] || Play; return <Icon size={24} />; })()}")
with open(hiw_path, "w") as f:
    f.write(hiw)

# Fix Alerts.tsx
fix("frontend/src/pages/Alerts.tsx", "selectedAlert && (", "selectedAlert !== null && (")
fix_re("frontend/src/pages/Alerts.tsx", r'\{ id:\s*"(.*?)",\s*title:\s*"(.*?)",\s*count:\s*"(.*?)",\s*trend:\s*"(.*?)",\s*status:\s*"(.*?)" \}', r'{ id: "\1", title: "\2", count: parseInt("\3"), trend: "\4", status: "\5", severity: "high", labelKey: "alerts.summary.\1" }')

# Fix Dashboard.tsx
fix("frontend/src/pages/Dashboard.tsx", "const handleKPIAction = (statId) => {", "const handleKPIAction = (statId: string) => {")

# Fix Signup.tsx
fix("frontend/src/pages/Signup.tsx", "const handleLanguageChange = (language) => {", "const handleLanguageChange = (language: string) => {")

# Fix Simulation.tsx
fix("frontend/src/pages/Simulation.tsx", 'selectedScenario === "deploy_ambulance"', 'selectedScenario?.id === "deploy_ambulance"')

