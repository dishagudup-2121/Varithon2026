export const dashboardStats = [
  {
    id: "pilgrims",
    titleKey: "dashboard.totalPilgrims",
    value: "24,850",
    subtitleKey: "dashboard.updatedJustNow",
    icon: "users",
  },
  {
    id: "risk",
    titleKey: "dashboard.highRiskZones",
    value: "3",
    subtitleKey: "dashboard.needsAttention",
    icon: "alert",
  },
  {
    id: "medical",
    titleKey: "dashboard.medicalCases",
    value: "42",
    subtitleKey: "dashboard.currentCases",
    icon: "heart",
  },
  {
    id: "ambulance",
    titleKey: "dashboard.availableAmbulances",
    value: "7",
    subtitleKey: "dashboard.readyForDispatch",
    icon: "ambulance",
  },
  {
    id: "volunteers",
    titleKey: "dashboard.availableVolunteers",
    value: "126",
    subtitleKey: "dashboard.availableNow",
    icon: "users",
  },
];

export const alerts = [
  {
    id: 1,
    type: "high",
    titleKey: "dashboard.alerts.highRisk",
    location: "Zone 6",
    descriptionKey: "dashboard.alerts.congestion",
    time: "2 min ago",
  },
  {
    id: 2,
    type: "medium",
    titleKey: "dashboard.alerts.heatRisk",
    location: "Zone 4",
    descriptionKey: "dashboard.alerts.temperature",
    time: "5 min ago",
  },
  {
    id: 3,
    type: "resource",
    titleKey: "dashboard.alerts.resourceAlert",
    location: "Zone 2",
    descriptionKey: "dashboard.alerts.ambulance",
    time: "8 min ago",
  },
];

export const recommendations = [
  {
    icon: "ambulance",
    textKey: "dashboard.recommendations.ambulance",
    resource: "Ambulance 3",
    zone: "Zone 6",
  },
  {
    icon: "users",
    textKey: "dashboard.recommendations.volunteers",
    resource: "Volunteer Team 1",
    zone: "Zone 6",
  },
  {
    icon: "water",
    textKey: "dashboard.recommendations.water",
    resource: "Water Tanker 2",
    zone: "Zone 6",
  },
];
