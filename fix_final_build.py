import re

def fix(path, search, replace):
    with open(path, "r") as f:
        c = f.read()
    c = c.replace(search, replace)
    with open(path, "w") as f:
        f.write(c)

ai_path = "frontend/src/pages/AIAssistant.tsx"
with open(ai_path, "r") as f:
    ai = f.read()

# Fix imports
ai = ai.replace('import { ChatMessage } from "../types";', 'import { ChatMessage as ChatMessageType } from "../types";')
ai = ai.replace('import ChatMessage from "../components/assistant/ChatMessage";', 'import ChatMessage from "../components/assistant/ChatMessage";') # Just in case

# Fix state
ai = ai.replace('useState<ChatMessage[]>', 'useState<ChatMessageType[]>')
ai = ai.replace('id: Date.now(),', 'id: Date.now().toString(),')
ai = ai.replace('id: Date.now() + 1,', 'id: (Date.now() + 1).toString(),')
ai = ai.replace('messages.map((message: ChatMessage)', 'messages.map((message: ChatMessageType)')
ai = ai.replace('key={suggestion.id}', 'key={index}')
with open(ai_path, "w") as f:
    f.write(ai)

fix("frontend/src/components/dashboard/AlertsPanel.tsx", "icons[alert.type]", "icons[alert.type as keyof typeof icons] || AlertTriangle")

fix("frontend/src/components/dashboard/RecommendationCard.tsx", "icons[recommendation.type]", "icons[recommendation.type as keyof typeof icons] || Play")

fix("frontend/src/components/resources/ResourceSummaryCard.tsx", "resource.available / resource.total", "Number(resource.available) / Number(resource.total)")

fix("frontend/src/pages/Dashboard.tsx", "getKpiClickHandler(stat.id)", "getKpiClickHandler(stat.id) || undefined")

fix("frontend/src/pages/Resources.tsx", "...previous, resource.id", "...previous, String(resource.id)")
fix("frontend/src/pages/Resources.tsx", "id !== resource.id", "id !== String(resource.id)")

fix("frontend/src/pages/Signup.tsx", "const handleLanguageChange = (language) => {", "const handleLanguageChange = (language: string) => {")

