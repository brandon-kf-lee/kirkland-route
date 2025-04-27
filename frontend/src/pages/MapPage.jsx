import { useState } from 'react';
import { GoogleMap, LoadScript, Polyline } from '@react-google-maps/api';
import routeIcon from '../assets/route-icon.png';
import statsIcon from '../assets/stats-icon.png';
import carpoolIcon from '../assets/carpool-icon.png';
import backgroundMap from '../assets/background-map.png';
import PageWrapper from '../components/PageWrapper';
import apiBaseUrl from '../api';


function decodePolyline(encoded) {
    let len = encoded.length;
    let index = 0;
    const path = [];
    let lat = 0;
    let lng = 0;
  
    while (index < len) {
      let b, shift = 0, result = 0;
      do {
        b = encoded.charCodeAt(index++) - 63;
        result |= (b & 0x1f) << shift;
        shift += 5;
      } while (b >= 0x20);
  
      const deltaLat = (result & 1) ? ~(result >> 1) : (result >> 1);
      lat += deltaLat;
  
      shift = 0;
      result = 0;
      do {
        b = encoded.charCodeAt(index++) - 63;
        result |= (b & 0x1f) << shift;
        shift += 5;
      } while (b >= 0x20);
  
      const deltaLng = (result & 1) ? ~(result >> 1) : (result >> 1);
      lng += deltaLng;
  
      path.push({ lat: lat / 1e5, lng: lng / 1e5 });
    }
  
    return path;
}

function MapPage() {
  const [openTabs, setOpenTabs] = useState([]);
  const [origin, setOrigin] = useState('');
  const [destination, setDestination] = useState('');
  const [path, setPath] = useState([]);
  const [googleMapsUrl, setGoogleMapsUrl] = useState(''); // ✅ Added

  const handleToggleTab = (tabName) => {
    if (openTabs.includes(tabName)) {
      setOpenTabs(openTabs.filter((tab) => tab !== tabName));
    } else {
      if (openTabs.length < 2) {
        setOpenTabs([...openTabs, tabName]);
      } else {
        setOpenTabs([openTabs[1], tabName]);
      }
    }
  };

  const handleCalculateRoute = async () => {
    try {
      const username = localStorage.getItem('username');
  
      // Step 1: Get user profile
      const profileResponse = await fetch(`${apiBaseUrl}/api/users/profile/${username}`, {
        method: 'GET',
      });
      const profileData = await profileResponse.json();
      console.log('Fetched profile data:', profileData);
  
      if (!profileResponse.ok) {
        alert('Failed to load profile.');
        return;
      }
  
      // Step 2: Create a trip
      const createTripResponse = await fetch(`'${apiBaseUrl}/api/trips/create-trip`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          origin: origin,
          destination: destination,
          user_id: profileData._id
        }),
      });
  
      if (!createTripResponse.ok) {
        throw new Error('Failed to create trip');
      }
  
      const createTripData = await createTripResponse.json();
      const tripId = createTripData.trip_id;
      console.log('Created trip:', tripId);
  
      // Step 3: Calculate Costco stops (JUST send trip_id!!)
      const response = await fetch(`${apiBaseUrl}/api/trips/calculate-trip-costco-stops`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          trip_id: tripId,
        }),
      });
  
      const data = await response.json();
      console.log('Backend response:', data);
  
      if (data.polyline) {
        const decodedPath = decodePolyline(data.polyline);
        setPath(decodedPath); // Set the decoded polyline path
      } else {
        console.error('No polyline received from backend');
      }

      if (data.google_maps_url) { // ✅ New: capture Google Maps URL
        setGoogleMapsUrl(data.google_maps_url);
      } else {
        console.error('No Google Maps URL received from backend');
      }

    } catch (error) {
      console.error('Error calculating trip:', error);
    }
  };
  
  return (
    <div className="relative flex min-h-screen bg-[#0f1b21] overflow-hidden pb-16">
      {/* Fixed Full Background Image */}
      <div
        className="absolute inset-0 bg-cover bg-center opacity-30 z-0"
        style={{ backgroundImage: `url(${backgroundMap})` }}
      ></div>

      {/* Sidebar */}
      <div className="relative z-10 flex flex-col items-center bg-[#20343D] w-20 py-8 space-y-8 ml-4 mt-4 rounded-2xl shadow-xl">
        {/* Route Icon */}
        <button
          onClick={() => handleToggleTab('route')}
          className={`hover:opacity-75 ${openTabs.includes('route') ? 'opacity-100' : 'opacity-50'}`}
        >
          <img src={routeIcon} alt="Route" className="w-8 h-8" />
        </button>

        {/* Stats Icon */}
        <button
          onClick={() => handleToggleTab('stats')}
          className={`hover:opacity-75 ${openTabs.includes('stats') ? 'opacity-100' : 'opacity-50'}`}
        >
          <img src={statsIcon} alt="Stats" className="w-8 h-8" />
        </button>

        {/* Carpool Icon */}
        <button
          onClick={() => handleToggleTab('carpool')}
          className={`hover:opacity-75 ${openTabs.includes('carpool') ? 'opacity-100' : 'opacity-50'}`}
        >
          <img src={carpoolIcon} alt="Carpool" className="w-8 h-8" />
        </button>
      </div>

      {/* Main Content */}
      <div className="relative z-10 flex flex-1 overflow-hidden">
        {/* Tabs Column */}
        <div className={`flex flex-col transition-all duration-500 ease-in-out overflow-hidden ${openTabs.length > 0 ? 'w-80' : 'w-0'} bg-[#1a2a32] ml-4 mt-4 rounded-2xl shadow-xl`}>
          {openTabs.map((tab) => (
            <div key={tab} className="p-4">
              <div className="bg-[#20343D] rounded-2xl shadow-lg p-6 flex flex-col items-center mb-6">
                {tab === 'route' && (
                  <div className="w-full flex flex-col items-center">
                    <h2 className="text-xl font-bold font-heading text-white mb-4 text-center w-full">Route</h2>
                    <input
                      placeholder="Origin"
                      value={origin}
                      onChange={(e) => setOrigin(e.target.value)}
                      className="w-full mb-4 p-3 rounded-xl bg-white text-gray-500 placeholder-gray-500"
                    />
                    <input
                      placeholder="Destination"
                      value={destination}
                      onChange={(e) => setDestination(e.target.value)}
                      className="w-full mb-6 p-3 rounded-xl bg-white text-gray-500 placeholder-gray-500"
                    />
                    <button
                      onClick={handleCalculateRoute}
                      className="px-8 py-2 border-2 border-white text-white rounded-xl hover:bg-white hover:text-black transition mb-4"
                    >
                      Calculate
                    </button>
                    {/* ✅ New "Open in Google Maps" Button */}
                    {googleMapsUrl && (
                      <button
                        onClick={() => window.open(googleMapsUrl, '_blank')}
                        className="px-6 py-2 bg-green-500 hover:bg-green-600 text-white font-bold rounded-xl transition"
                      >
                        Open in Google Maps
                      </button>
                    )}
                  </div>
                )}
                {tab === 'stats' && (
                  <div className="w-full flex flex-col items-start">
                    <h2 className="text-xl font-bold font-heading text-white mb-6 text-center w-full">STATS</h2>
                    {/* Stats content will go here */}
                  </div>
                )}
                {tab === 'carpool' && (
                  <div className="w-full flex flex-col items-start">
                    <h2 className="text-xl font-bold font-heading text-white mb-6 text-center w-full">CARPOOL</h2>
                    {/* Carpool content will go here */}
                  </div>
                )}
              </div>
            </div>
          ))}
        </div>

        {/* Map Section */}
        <div className="flex-1 bg-transparent flex items-center justify-center transition-all duration-500">
            <LoadScript googleMapsApiKey="AIzaSyA8O7NoxrTHH5FpjhgkUqHm0NzKbq-IC4U">
                <div className="w-[90%] h-[96%] rounded-2xl overflow-hidden shadow-2xl">
                <GoogleMap
                    mapContainerStyle={{ width: '100%', height: '100%' }}
                    center={{ lat: 34.0522, lng: -118.2437 }}
                    zoom={6}
                >
                    {/* Draw the route here */}
                    <Polyline
                    path={path}
                    options={{
                        strokeColor: '#FF0000',
                        strokeOpacity: 0.8,
                        strokeWeight: 4,
                    }}
                    />
                </GoogleMap>
                </div>
            </LoadScript>
        </div>
      </div>
    </div>
  );
}

export default MapPage;
