

export interface DashboardStat {
  id: string;
  titleKey: string;
  value: string | number;
  subtitleKey: string;
  icon: string;
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
  available: number | string;
  total: number | string;
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
  recommendationKey: string;
}

export interface Alert {
  status: string;
  zone: string;
  riskScore: number;
  predictedTime: string;
  recommendationKey: string;
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
  id: string;
  title: string;
  trend: string;
  status: string;
  value: string;
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
  id: string;
  textKey?: string;
  text: string;
}

export interface HowItWorksFeature {
  icon: string;
  title: string;
  description: string;
}
