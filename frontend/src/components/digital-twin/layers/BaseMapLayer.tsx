import { TileLayer } from 'react-leaflet';

export default function BaseMapLayer() {
  return (
    <TileLayer
      attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
      url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
      className="map-tiles"
    />
  );
}
