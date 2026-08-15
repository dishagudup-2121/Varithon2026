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

export default function DigitalTwinMap({ previewMode = false }: { previewMode?: boolean }) {
  const { t } = useTranslation();
  const { simulationState } = useSimulationStream();
  const [showLegend, setShowLegend] = useState(true);

  return (
    <div className={`flex-1 relative flex flex-col ${previewMode ? 'h-full min-h-[300px]' : 'min-h-[400px] rounded-2xl overflow-hidden shadow-sm'}`}>
      {/* Map container fixed to take full space so it's not grey/blank */}
      <div className="flex-1 w-full h-full relative z-0">
        <MapContainer 
          center={CENTER} 
          zoom={12} 
          scrollWheelZoom={!previewMode} 
          dragging={!previewMode}
          className="absolute inset-0 z-0"
          zoomControl={!previewMode}
        >
          <BaseMapLayer />

          {!previewMode && (
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
          )}
          {previewMode && (
            <>
              <RouteLayer />
              <ZoneLayer />
              <PilgrimLayer state={simulationState} />
              <CrowdLayer state={simulationState} />
            </>
          )}
        </MapContainer>
      </div>

      {/* Map Legend */}
      {!previewMode && (
        <div className="absolute bottom-4 left-4 z-[1000]">
          {showLegend ? (
            <div className="bg-white/95 border border-[#EDE2D0] p-4 rounded-xl shadow-md backdrop-blur-md">
              <div className="flex justify-between items-center mb-3">
                <h4 className="text-[10px] font-bold text-[#8B735D] uppercase tracking-wider">{t('legend')}</h4>
                <button 
                  onClick={() => setShowLegend(false)}
                  className="text-[10px] text-[#A68F7B] hover:text-[#D96F00] transition-colors uppercase ml-4 cursor-pointer font-semibold"
                >
                  (Hide)
                </button>
              </div>
              <ul className="space-y-2 text-xs font-medium text-[#6B421F]">
                <li className="flex items-center gap-2"><div className="w-2 h-2 rounded-full bg-sky-400"></div> Pilgrim Groups</li>
                <li className="flex items-center gap-2"><div className="w-2 h-2 rounded-full bg-slate-500"></div> Road Network</li>
                <li className="flex items-center gap-2"><div className="w-2 h-2 rounded-full bg-blue-500"></div> Open Route</li>
                <li className="flex items-center gap-2"><div className="w-2 h-2 rounded-full border-t-2 border-amber-500 border-dashed"></div> Restricted Route</li>
                <li className="flex items-center gap-2"><div className="w-2 h-2 rounded-full bg-red-500"></div> Closed Route</li>
                <li className="flex items-center gap-2"><div className="w-3 h-3 border border-slate-600 bg-slate-500/10 border-dashed"></div> Administrative / Operational Zone</li>
              </ul>
              <div className="mt-4 pt-3 border-t border-[#F1DEC8]">
                <h4 className="text-[10px] font-bold text-[#8B735D] uppercase tracking-wider mb-2">Relative Simulated Load</h4>
                <div className="h-2 w-full rounded-full bg-gradient-to-r from-blue-500 via-yellow-500 to-red-500"></div>
                <div className="flex justify-between text-[10px] font-semibold text-[#8B735D] mt-1.5">
                  <span>Low</span>
                  <span>High</span>
                </div>
              </div>
            </div>
          ) : (
            <button 
              onClick={() => setShowLegend(true)}
              className="bg-white/95 border border-[#EDE2D0] shadow-sm px-4 py-2 rounded-xl backdrop-blur-md text-xs font-bold text-[#8B735D] uppercase tracking-wider hover:text-[#D96F00] transition-colors cursor-pointer"
            >
              Show Legend
            </button>
          )}
        </div>
      )}
    </div>
  );
}
