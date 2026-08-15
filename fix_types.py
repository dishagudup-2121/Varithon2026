import re

def replace_in_file(path, old, new):
    with open(path, "r") as f:
        content = f.read()
    content = content.replace(old, new)
    with open(path, "w") as f:
        f.write(content)

# Fix ICONS -> icons
replace_in_file("frontend/src/components/dashboard/RecommendationCard.tsx", "const ICONS: Record<string, React.ElementType> =", "const icons: Record<string, React.ElementType> =")
replace_in_file("frontend/src/components/dashboard/RecommendationCard.tsx", "const icons = {", "const icons: Record<string, React.ElementType> = {")

replace_in_file("frontend/src/components/resources/AllocationTable.tsx", "const ICONS: Record<string, React.ElementType> =", "const icons: Record<string, React.ElementType> =")
replace_in_file("frontend/src/components/resources/AllocationTable.tsx", "const icons = {", "const icons: Record<string, React.ElementType> = {")

replace_in_file("frontend/src/components/resources/ResourceSummaryCard.tsx", "const ICONS: Record<string, React.ElementType> =", "const icons: Record<string, React.ElementType> =")

replace_in_file("frontend/src/components/simulation/ScenarioCard.tsx", "const ICONS: Record<string, React.ElementType> =", "const icons: Record<string, React.ElementType> =")
replace_in_file("frontend/src/components/simulation/ScenarioCard.tsx", "const icons = {", "const icons: Record<string, React.ElementType> = {")

# Fix Home.tsx maps
home_code = open("frontend/src/pages/Home.tsx").read()
home_code = re.sub(r'\{features\.map\(\s*\(\{\s*icon:\s*Icon,\s*title,\s*subtitle\s*\},',
                   r'{features.map(({ icon: Icon, title, subtitle }: { icon: React.ElementType, title: string, subtitle: string },', home_code)
home_code = re.sub(r'\{stats\.map\(\s*\(\{\s*icon:\s*Icon,\s*number,\s*label\s*\},',
                   r'{stats.map(({ icon: Icon, number, label }: { icon: React.ElementType, number: string, label: string },', home_code)
with open("frontend/src/pages/Home.tsx", "w") as f:
    f.write(home_code)

# Fix Login.tsx
login_code = open("frontend/src/pages/Login.tsx").read()
login_code = login_code.replace("const newErrors = {};", "const newErrors: LoginErrors = {};")
login_code = login_code.replace("const newErrors = validate();", "const newErrors: LoginErrors = validate();")
with open("frontend/src/pages/Login.tsx", "w") as f:
    f.write(login_code)

# Fix Signup.tsx
signup_code = open("frontend/src/pages/Signup.tsx").read()
signup_code = signup_code.replace("const newErrors = {};", "const newErrors: SignupErrors = {};")
signup_code = signup_code.replace("const newErrors = validate();", "const newErrors: SignupErrors = validate();")
signup_code = signup_code.replace("const handleLanguageChange = (language) => {", "const handleLanguageChange = (language: string) => {")
with open("frontend/src/pages/Signup.tsx", "w") as f:
    f.write(signup_code)

# Fix Dashboard.tsx KPICard casing
dashboard_code = open("frontend/src/pages/Dashboard.tsx").read()
dashboard_code = dashboard_code.replace("import KPICard from \"../components/dashboard/KPICard\";", "import KPICard from \"../components/dashboard/KpiCard\";")
dashboard_code = dashboard_code.replace("const handleKPIAction = (statId) => {", "const handleKPIAction = (statId: string) => {")
dashboard_code = dashboard_code.replace("{dashboardStats.map((stat) => (", "{dashboardStats.map((stat: any) => (") # Wait, import the type
with open("frontend/src/pages/Dashboard.tsx", "w") as f:
    f.write(dashboard_code)
    
# Fix Simulation.tsx simulationResults
sim_code = open("frontend/src/pages/Simulation.tsx").read()
sim_code = sim_code.replace("simulationResults[selectedScenario.id]", "(simulationResults as Record<string, any>)[selectedScenario.id]")
sim_code = sim_code.replace("selectedScenario === \"deploy_ambulance\"", "selectedScenario?.id === \"deploy_ambulance\"")
with open("frontend/src/pages/Simulation.tsx", "w") as f:
    f.write(sim_code)

# Fix AIAssistant.tsx
ai_code = open("frontend/src/pages/AIAssistant.tsx").read()
ai_code = ai_code.replace("const sendQuestion = (responseKey) => {", "const sendQuestion = (responseKey: string) => {")
ai_code = ai_code.replace("const response = mockResponses[responseKey];", "const response = (mockResponses as Record<string, any>)[responseKey];")
with open("frontend/src/pages/AIAssistant.tsx", "w") as f:
    f.write(ai_code)

