import re

# 1. Update types/index.ts
types_path = "frontend/src/types/index.ts"
with open(types_path, "r") as f:
    types_code = f.read()

types_code = types_code.replace("export interface Recommendation {", "export interface Recommendation {\n  icon?: string;\n  resource?: string;\n  textKey?: string;\n  zone?: string;")
types_code = types_code.replace("export interface ResourceAllocation {", "export interface ResourceAllocation {\n  resource?: string;\n  name?: string;\n  to?: string;\n  destination?: string;\n  from?: string;\n  eta?: string;")
types_code = types_code.replace("export interface ResourceSummary {", "export interface ResourceSummary {\n  type?: string;\n  titleKey?: string;")
types_code = types_code.replace("export interface SimulationScenario {", "export interface SimulationScenario {\n  titleKey?: string;")

with open(types_path, "w") as f:
    f.write(types_code)


# 2. Fix AIAssistant
ai_path = "frontend/src/pages/AIAssistant.tsx"
with open(ai_path, "r") as f:
    ai_code = f.read()
if "import { ChatMessage }" not in ai_code:
    ai_code = ai_code.replace("import { useTranslation } from \"react-i18next\";", "import { useTranslation } from \"react-i18next\";\nimport { ChatMessage } from \"../types\";")
# Remove setHelpOpen if unused
ai_code = ai_code.replace("const [helpOpen, setHelpOpen] = useState(false);", "")
ai_code = ai_code.replace("setHelpOpen(true);", "")
ai_code = ai_code.replace("setHelpOpen(false);", "")
with open(ai_path, "w") as f:
    f.write(ai_code)

# 3. Fix Dashboard
db_path = "frontend/src/pages/Dashboard.tsx"
with open(db_path, "r") as f:
    db_code = f.read()
db_code = db_code.replace("const handleKPIAction = (statId) => {", "const handleKPIAction = (statId: string) => {")
with open(db_path, "w") as f:
    f.write(db_code)

# 4. Fix Signup
su_path = "frontend/src/pages/Signup.tsx"
with open(su_path, "r") as f:
    su_code = f.read()
su_code = su_code.replace("const handleLanguageChange = (language) => {", "const handleLanguageChange = (language: string) => {")
with open(su_path, "w") as f:
    f.write(su_code)

# 5. Fix Home
home_path = "frontend/src/pages/Home.tsx"
with open(home_path, "r") as f:
    home_code = f.read()
home_code = re.sub(r'\{features\.map\(\s*\(\{\s*icon:\s*Icon,\s*title,\s*subtitle\s*\},', r'{features.map(({ icon: Icon, title, subtitle }: { icon: React.ElementType, title: string, subtitle: string },', home_code)
home_code = re.sub(r'\{stats\.map\(\s*\(\{\s*icon:\s*Icon,\s*number,\s*label\s*\},', r'{stats.map(({ icon: Icon, number, label }: { icon: React.ElementType, number: string, label: string },', home_code)
with open(home_path, "w") as f:
    f.write(home_code)

