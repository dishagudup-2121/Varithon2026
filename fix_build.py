import re

types_path = "frontend/src/types/index.ts"
with open(types_path, "r") as f:
    types = f.read()

types = types.replace("export interface ResourceAllocation {", "export interface ResourceAllocation {\n  id?: string | number;\n  type?: string;")
types = types.replace("export interface ResourceSummary {", "export interface ResourceSummary {\n  id?: string | number;\n  available?: number | string;\n  total?: number | string;")
types = types.replace("export interface Alert {", "export interface Alert {\n  location?: string;\n  descriptionKey?: string;")
types = types.replace("export interface SimulationScenario {", "export interface SimulationScenario {\n  descriptionKey?: string;")

with open(types_path, "w") as f:
    f.write(types)

# Fix KPICard icon
k_path = "frontend/src/components/dashboard/KpiCard.tsx"
with open(k_path, "r") as f:
    k = f.read()
k = k.replace("icon: string;", "icon: any;")
with open(k_path, "w") as f:
    f.write(k)

# Fix Dashboard.tsx getKpiClickHandler
d_path = "frontend/src/pages/Dashboard.tsx"
with open(d_path, "r") as f:
    d = f.read()
d = d.replace("getKpiClickHandler(stat.id)", "getKpiClickHandler(stat.id) || (() => {})")
with open(d_path, "w") as f:
    f.write(d)

# Fix AIAssistant duplicate
ai_path = "frontend/src/pages/AIAssistant.tsx"
with open(ai_path, "r") as f:
    ai = f.read()
ai = re.sub(r'import\s+{\s*ChatMessage\s*}\s*from\s*"../types";\s*import\s+{\s*ChatMessage\s*}\s*from\s*"../types";', 'import { ChatMessage } from "../types";', ai)
ai = re.sub(r'import\s+{\s*ChatMessage\s*,\s*ChatMessage\s*}\s*from\s*"../types";', 'import { ChatMessage } from "../types";', ai)
ai = ai.replace("export default function ChatMessage({ message }) {", "export default function ChatMessageComponent({ message }) {")
with open(ai_path, "w") as f:
    f.write(ai)

