export const resourceSummary = [
  {
    id: "ambulances",
    type: "ambulance",
    titleKey: "resources.ambulances",
    available: 7,
    total: 12,
  },
  {
    id: "volunteers",
    type: "volunteers",
    titleKey: "resources.volunteers",
    available: 126,
    total: 180,
  },
  {
    id: "water",
    type: "water",
    titleKey: "resources.waterTankers",
    available: 8,
    total: 12,
  },
  {
    id: "medical",
    type: "medical",
    titleKey: "resources.medicalTeams",
    available: 14,
    total: 20,
  },
];

export const resourceAllocations = [
  {
    id: 1,
    resource: "Ambulance 3",
    type: "ambulance",
    from: "Zone 2",
    to: "Zone 6",
    eta: "11 min",
    status: "recommended",
  },
  {
    id: 2,
    resource: "Volunteer Team 1",
    type: "volunteers",
    from: "Zone 1",
    to: "Zone 6",
    eta: "8 min",
    status: "recommended",
  },
  {
    id: 3,
    resource: "Water Tanker 2",
    type: "water",
    from: "Zone 3",
    to: "Zone 6",
    eta: "15 min",
    status: "recommended",
  },
  {
    id: 4,
    resource: "Medical Team 2",
    type: "medical",
    from: "Base Camp",
    to: "Zone 7",
    eta: "20 min",
    status: "recommended",
  },
];

export const allResources = [
  {
    id: 1,
    name: "Ambulance 1",
    type: "ambulance",
    location: "Zone 3",
    status: "available",
  },
  {
    id: 2,
    name: "Ambulance 2",
    type: "ambulance",
    location: "Zone 4",
    status: "busy",
  },
  {
    id: 3,
    name: "Ambulance 3",
    type: "ambulance",
    location: "Zone 2",
    status: "available",
  },
  {
    id: 4,
    name: "Volunteer Team 1",
    type: "volunteers",
    location: "Zone 1",
    status: "available",
  },
  {
    id: 5,
    name: "Water Tanker 2",
    type: "water",
    location: "Zone 3",
    status: "available",
  },
  {
    id: 6,
    name: "Medical Team 2",
    type: "medical",
    location: "Base Camp",
    status: "assigned",
  },
];
