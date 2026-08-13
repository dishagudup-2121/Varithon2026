import { MapContainer, LayersControl } from 'react-leaflet';
import { useState } from 'react';
import 'leaflet/dist/leaflet.css';
import { useTranslation } from 'react-i18next';
import BaseMapLayer from './layers/BaseMapLayer';
import RouteLayer from './layers/RouteLayer';
import ZoneLayer from './layers/ZoneLayer';
import PilgrimLayer from './layers/PilgrimLayer';
import CrowdLayer from './layers/CrowdLayer';
import { useSimulationStream } from '../../hooks/useSimulationStream';

const { Overlay } = LayersControl;

// Center around Alandi/Pune demonstration area
const CENTER: [number, number] = [18.6300, 73.8800];

export default function DigitalTwinMap() {
  const { t } = useTranslation();
  const { simulationState } = useSimulationStream();
  const [showLegend, setShowLegend] = useState(true);

  return (
    <div className="panel flex-1 min-h-[400px] relative flex flex-col">
      <div className="panel-header absolute top-0 left-0 right-0 z-[1000] bg-slate-900/80 backdrop-blur-md border-b-0 rounded-t-xl">
        <span>DIGITAL TWIN - LIVE VIEW</span>
      </div>
      
      {/* Map container fixed to take full space so it's not grey/blank */}
      <div className="flex-1 w-full h-full relative z-0">
        <MapContainer 
          center={CENTER} 
          zoom={12} 
          scrollWheelZoom={true} 
          className="absolute inset-0"
          zoomControl={true}
        >
          <BaseMapLayer />

          <LayersControl position="topright">
            <Overlay checked name="Wari Routes">
              <RouteLayer />
            </Overlay>
            
            <Overlay checked name="Operational Zones">
              <ZoneLayer />
            </Overlay>

            <Overlay checked name="Synthetic Pilgrims (Demo)">
              <PilgrimLayer state={simulationState} />
            </Overlay>

            <Overlay checked name="Simulated Pilgrim Load">
              <CrowdLayer state={simulationState} />
            </Overlay>
          </LayersControl>
        </MapContainer>
      </div>

      {/* Map Legend */}
      <div className="absolute bottom-4 left-4 z-[1000]">
        {showLegend ? (
          <div className="bg-slate-900/90 border border-slate-700 p-3 rounded-lg backdrop-blur-md">
            <div className="flex justify-between items-center mb-2">
              <h4 className="text-[10px] font-bold text-slate-400 uppercase tracking-wider">{t('legend')}</h4>
              <button 
                onClick={() => setShowLegend(false)}
                className="text-[10px] text-slate-500 hover:text-slate-300 transition-colors uppercase ml-4"
              >
                (Hide)
              </button>
            </div>
            <ul className="space-y-1.5 text-xs text-slate-300">
              <li className="flex items-center gap-2"><div className="w-2 h-2 rounded-full bg-sky-400"></div> Pilgrim Groups</li>
              <li className="flex items-center gap-2"><div className="w-2 h-2 rounded-full bg-slate-500"></div> Road Network</li>
              <li className="flex items-center gap-2"><div className="w-2 h-2 rounded-full bg-blue-500"></div> Open Route</li>
              <li className="flex items-center gap-2"><div className="w-2 h-2 rounded-full border-t-2 border-amber-500 border-dashed"></div> Restricted Route</li>
              <li className="flex items-center gap-2"><div className="w-2 h-2 rounded-full bg-red-500"></div> Closed Route</li>
              <li className="flex items-center gap-2"><div className="w-3 h-3 border-2 border-red-500 bg-red-500/20"></div> High/Critical Zone</li>
            </ul>
            <div className="mt-4 pt-3 border-t border-slate-700/50">
              <h4 className="text-[10px] font-bold text-slate-400 uppercase tracking-wider mb-2">Relative Simulated Pilgrim Load</h4>
              <div className="h-2 w-full rounded-full bg-gradient-to-r from-blue-500 via-yellow-500 to-red-500"></div>
              <div className="flex justify-between text-[10px] text-slate-400 mt-1">
                <span>Low</span>
                <span>High</span>
              </div>
            </div>
          </div>
        ) : (
          <button 
            onClick={() => setShowLegend(true)}
            className="bg-slate-900/90 border border-slate-700 px-3 py-2 rounded-lg backdrop-blur-md text-[10px] font-bold text-slate-400 uppercase tracking-wider hover:bg-slate-800 transition-colors"
          >
            Show Legend
          </button>
        )}
      </div>
    </div>
  );
}
