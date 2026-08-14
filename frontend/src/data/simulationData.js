export const scenarios = [
  {
    id: "close_route",
    titleKey: "simulation.scenarios.closeRoute.title",
    descriptionKey:
      "simulation.scenarios.closeRoute.description",
    icon: "route",
  },
  {
    id: "add_volunteers",
    titleKey:
      "simulation.scenarios.addVolunteers.title",
    descriptionKey:
      "simulation.scenarios.addVolunteers.description",
    icon: "volunteers",
  },
  {
    id: "deploy_ambulance",
    titleKey:
      "simulation.scenarios.deployAmbulance.title",
    descriptionKey:
      "simulation.scenarios.deployAmbulance.description",
    icon: "ambulance",
  },
];

export const simulationResults = {
  close_route: {
    scenario: "close_route",

    before: {
      crowd: 12800,
      risk: 82,
      eta: 24,
      affectedZones: 3,
    },

    after: {
      crowd: 10200,
      risk: 61,
      eta: 31,
      affectedZones: 2,
    },

    impact: {
      congestion: -20,
      risk: -21,
      eta: 7,
    },

    recommendationKey:
      "simulation.results.closeRouteRecommendation",
  },

  add_volunteers: {
    scenario: "add_volunteers",

    before: {
      crowd: 12800,
      risk: 82,
      eta: 24,
      affectedZones: 3,
    },

    after: {
      crowd: 12800,
      risk: 69,
      eta: 21,
      affectedZones: 2,
    },

    impact: {
      congestion: -8,
      risk: -13,
      eta: -3,
    },

    recommendationKey:
      "simulation.results.volunteerRecommendation",
  },

  deploy_ambulance: {
    scenario: "deploy_ambulance",

    before: {
      crowd: 12800,
      risk: 82,
      eta: 24,
      affectedZones: 3,
    },

    after: {
      crowd: 12800,
      risk: 73,
      eta: 20,
      affectedZones: 2,
    },

    impact: {
      congestion: -4,
      risk: -9,
      eta: -4,
    },

    recommendationKey:
      "simulation.results.ambulanceRecommendation",
  },
};
