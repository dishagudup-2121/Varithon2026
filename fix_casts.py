import re

def fix(path, search, replace):
    with open(path, "r") as f:
        c = f.read()
    c = c.replace(search, replace)
    with open(path, "w") as f:
        f.write(c)

fix("frontend/src/components/dashboard/RecommendationCard.tsx", "icons[(recommendation.type || '') as keyof typeof icons]", "icons[recommendation.type as keyof typeof icons]")
fix("frontend/src/components/dashboard/RecommendationCard.tsx", "t(recommendation.textKey || '')", "t(recommendation.textKey)")

fix("frontend/src/components/resources/ResourceSummaryCard.tsx", "icons[(resource.type || '') as keyof typeof icons]", "icons[resource.type as keyof typeof icons]")
fix("frontend/src/components/resources/ResourceSummaryCard.tsx", "t(resource.titleKey || '')", "t(resource.titleKey)")

fix("frontend/src/components/simulation/ScenarioCard.tsx", "icons[(scenario.icon || '') as keyof typeof icons]", "icons[scenario.icon as keyof typeof icons]")
fix("frontend/src/components/simulation/ScenarioCard.tsx", "t(scenario.titleKey || '')", "t(scenario.titleKey)")

fix("frontend/src/components/alerts/AlertSummaryCard.tsx", "icons[(item.severity || '') as keyof typeof icons]", "icons[item.severity as keyof typeof icons]")
fix("frontend/src/components/alerts/AlertSummaryCard.tsx", "colors[(item.severity || '') as keyof typeof colors]", "colors[item.severity as keyof typeof colors]")

fix("frontend/src/components/common/HowItWorks.tsx", "icons[(feature.icon || '') as keyof typeof icons]", "icons[feature.icon as keyof typeof icons]")

