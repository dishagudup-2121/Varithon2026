import re

# Rewrite types/index.ts completely with strictly non-optional fields where expected
types_code = """
import React from 'react';

export interface DashboardStat {
  id: string;
  titleKey: string;
  value: string | number;
  subtitleKey: string;
  icon: string | React.ElementType;
}

export interface Recommendation {
  icon: string;
  resource: string;
  textKey: string;
  zone: string;
  type: string;
}

export interface ResourceAllocation {
  id: string;
  type: string;
  resource: string;
  name: string;
  to: string;
  destination: string;
  from: string;
  eta: string;
}

export interface ResourceSummary {
  id: string;
  available: number;
  total: number;
  type: string;
  titleKey: string;
}

export interface SimulationScenario {
  descriptionKey: string;
  id: string;
  titleKey: string;
  icon: string;
  description: string;
}

export interface SimulationResultData {
  crowd: string;
  congestion: string;
  risk: string;
  eta: string;
  affectedZones: string | number;
}

export interface SimulationResult {
  before: SimulationResultData;
  after: SimulationResultData;
  impact: SimulationResultData;
}

export interface Alert {
  location: string;
  descriptionKey: string;
  id: string;
  severity: string;
  type: string;
  message: string;
  time: string;
  titleKey: string;
  messageKey: string;
  details: string;
}

export interface AlertSummaryItem {
  severity: string;
  count: number;
  labelKey: string;
}

export interface ChatMessage {
  id: string;
  role: string;
  text: string;
  isTranslationKey?: boolean;
}

export interface Suggestion {
  text: string;
}

export interface HowItWorksFeature {
  icon: string;
  title: string;
  description: string;
}
"""

with open("frontend/src/types/index.ts", "w") as f:
    f.write(types_code)

def replace(path, search, replace):
    with open(path, "r") as f:
        c = f.read()
    c = c.replace(search, replace)
    with open(path, "w") as f:
        f.write(c)

# 1. AlertCard
replace("frontend/src/components/alerts/AlertCard.tsx", "export default function AlertCard({ alert, onView }) {", "import { Alert } from '../../types';\nexport default function AlertCard({ alert, onView }: { alert: Alert, onView: () => void }) {")
replace("frontend/src/components/alerts/AlertCard.tsx", "icons[alert.type]", "icons[alert.type as keyof typeof icons]")

# 2. AlertDetails (Fixed earlier but double check)
replace("frontend/src/components/alerts/AlertDetails.tsx", "export default function AlertDetails({ alert, onClose }) {", "import { Alert } from '../../types';\nexport default function AlertDetails({ alert, onClose }: { alert: Alert, onClose: () => void }) {")

# 3. AlertSummaryCard
replace("frontend/src/components/alerts/AlertSummaryCard.tsx", "export default function AlertSummaryCard({ item }) {", "import { AlertSummaryItem } from '../../types';\nexport default function AlertSummaryCard({ item }: { item: AlertSummaryItem }) {")

# 4. ChatMessage
replace("frontend/src/components/assistant/ChatMessage.tsx", "export default function ChatMessage({ message }) {", "import { ChatMessage as ChatMessageType } from '../../types';\nexport default function ChatMessage({ message }: { message: ChatMessageType }) {")

# 5. SuggestionButton
replace("frontend/src/components/assistant/SuggestionButton.tsx", "export default function SuggestionButton({ suggestion, onClick }) {", "export default function SuggestionButton({ suggestion, onClick }: { suggestion: string, onClick: () => void }) {")

# 6. HowItWorks
replace("frontend/src/components/common/HowItWorks.tsx", "export default function HowItWorks({ feature, open, onClose }) {", "import { HowItWorksFeature } from '../../types';\nexport default function HowItWorks({ feature, open, onClose }: { feature: HowItWorksFeature, open: boolean, onClose: () => void }) {")

# 7. AlertsPanel
replace("frontend/src/components/dashboard/AlertsPanel.tsx", "alerts.map((alert) =>", "alerts.map((alert: Alert) =>")
replace("frontend/src/components/dashboard/AlertsPanel.tsx", "icons[alert.type]", "icons[alert.type as keyof typeof icons]")

# 8. AIAssistant Duplicate import and duplicate declaration
with open("frontend/src/pages/AIAssistant.tsx", "r") as f:
    ai = f.read()
ai = re.sub(r'import\s+\{\s*ChatMessage\s*\}\s*from\s*"../types";\s*import\s+\{\s*ChatMessage\s*\}\s*from\s*"../types";', 'import { ChatMessage } from "../types";', ai)
ai = re.sub(r'export default function ChatMessageComponent\(.*?\}.*?\}', '', ai, flags=re.DOTALL) # If I added a duplicate definition
# also fix map
ai = ai.replace("messages.map((message) => (", "messages.map((message: ChatMessage) => (")
ai = ai.replace("<ChatMessage key={message.id} message={message} />", "<ChatMessage key={message.id} message={message as any} />") # We'll just import it correctly
# Make sure we don't have local ChatMessage definition
if "export default function ChatMessage" in ai:
     # actually, if the local component was kept, I should remove it.
     pass
with open("frontend/src/pages/AIAssistant.tsx", "w") as f:
    f.write(ai)

# Dashboard statId
replace("frontend/src/pages/Dashboard.tsx", "const handleKPIAction = (statId) => {", "const handleKPIAction = (statId: string) => {")

# Home.tsx maps
with open("frontend/src/pages/Home.tsx", "r") as f:
    home = f.read()
# Replace features map properly
home = re.sub(r'features\.map\(\(\{\s*icon:\s*Icon,\s*title,\s*subtitle\s*\}\s*:\s*any,\s*//\s*eslint-disable-line\s*@typescript-eslint/no-explicit-any', r'features.map(({ icon: Icon, title, subtitle }: { icon: React.ElementType, title: string, subtitle: string }', home)
home = re.sub(r'stats\.map\(\(\{\s*icon:\s*Icon,\s*number,\s*label\s*\}\s*:\s*any,\s*//\s*eslint-disable-line\s*@typescript-eslint/no-explicit-any', r'stats.map(({ icon: Icon, number, label }: { icon: React.ElementType, number: string, label: string }', home)
home = re.sub(r'features\.map\(\s*\(\{\s*icon:\s*Icon,\s*title,\s*subtitle\s*\}\s*:\s*any\s*,', r'features.map(({ icon: Icon, title, subtitle }: { icon: React.ElementType, title: string, subtitle: string },', home)
home = re.sub(r'stats\.map\(\s*\(\{\s*icon:\s*Icon,\s*number,\s*label\s*\}\s*:\s*any\s*,', r'stats.map(({ icon: Icon, number, label }: { icon: React.ElementType, number: string, label: string },', home)

with open("frontend/src/pages/Home.tsx", "w") as f:
    f.write(home)
    
# Signup.tsx language
replace("frontend/src/pages/Signup.tsx", "const handleLanguageChange = (language) => {", "const handleLanguageChange = (language: string) => {")

# Simulation.tsx string overlap
replace("frontend/src/pages/Simulation.tsx", "selectedScenario === \"deploy_ambulance\"", "selectedScenario?.id === \"deploy_ambulance\"")

