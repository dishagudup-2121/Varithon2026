import re
import os

def read_file(path):
    with open(path, "r") as f:
        return f.read()

def write_file(path, content):
    with open(path, "w") as f:
        f.write(content)

# AllocationTable.tsx and ResourceSummaryCard.tsx
f = read_file("frontend/src/components/resources/AllocationTable.tsx")
f = f.replace("HeartPulse,", "")
write_file("frontend/src/components/resources/AllocationTable.tsx", f)

f = read_file("frontend/src/components/resources/ResourceSummaryCard.tsx")
f = f.replace("HeartPulse,", "")
f = f.replace("icons[resource.type]", "icons[resource.type || \"\"]")
f = f.replace("t(resource.titleKey)", "t(resource.titleKey || \"\")")
write_file("frontend/src/components/resources/ResourceSummaryCard.tsx", f)

# ComparisonCard.tsx
f = read_file("frontend/src/components/simulation/ComparisonCard.tsx")
f = f.replace("{ result }: { result: any }", "{ result }: { result: Record<string, unknown> }")
write_file("frontend/src/components/simulation/ComparisonCard.tsx", f)

# SimulationRecommendation.tsx
f = read_file("frontend/src/components/simulation/SimulationRecommendation.tsx")
f = f.replace("result: any;", "result: Record<string, unknown>;")
write_file("frontend/src/components/simulation/SimulationRecommendation.tsx", f)

# Dashboard.tsx
f = read_file("frontend/src/pages/Dashboard.tsx")
f = f.replace("(stat: any)", "(stat: Record<string, unknown>)")
write_file("frontend/src/pages/Dashboard.tsx", f)

# Simulation.tsx
f = read_file("frontend/src/pages/Simulation.tsx")
f = f.replace("useState<any>(null)", "useState<Record<string, unknown> | null>(null)")
write_file("frontend/src/pages/Simulation.tsx", f)

# Login.tsx
f = read_file("frontend/src/pages/Login.tsx")
f = f.replace("import { useState, ChangeEvent, FormEvent } from 'react';", "import { useState } from 'react';")
write_file("frontend/src/pages/Login.tsx", f)

# Signup.tsx
f = read_file("frontend/src/pages/Signup.tsx")
f = f.replace("import { useState, ChangeEvent, FormEvent } from 'react';", "import { useState, ChangeEvent } from 'react';")
f = f.replace("import { Check, Globe } from 'lucide-react';", "import { Check } from 'lucide-react';")
write_file("frontend/src/pages/Signup.tsx", f)

# AIAssistant.tsx
f = read_file("frontend/src/pages/AIAssistant.tsx")
f = f.replace("(responseKey: any)", "(responseKey: string)")
f = re.sub(r'import\s+{\s*ChatMessage\s*}\s*from\s*"../types";\s*import\s+{\s*ChatMessage\s*}\s*from\s*"../types";', 'import { ChatMessage } from "../types";', f)
write_file("frontend/src/pages/AIAssistant.tsx", f)

