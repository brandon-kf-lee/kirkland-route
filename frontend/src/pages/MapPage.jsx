import { useState } from 'react';
import routeIcon from '../assets/route-icon.png';
import statsIcon from '../assets/stats-icon.png';
import carpoolIcon from '../assets/carpool-icon.png';
import backgroundMap from '../assets/background-map.png';
import PageWrapper from '../components/PageWrapper';

function MapPage() {
  const [openTabs, setOpenTabs] = useState([]);

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

  return (
    <div className="relative flex min-h-screen bg-[#0f1b21] overflow-hidden pb-16">
      {/* Fixed Full Background Image */}
      <div
        className="absolute inset-0 bg-cover bg-center opacity-30 z-0"
        style={{
          backgroundImage: `url(${backgroundMap})`,
        }}
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
                      className="w-full mb-4 p-3 rounded-xl bg-white text-gray-500 placeholder-gray-500"
                    />
                    <input
                      placeholder="Destination"
                      className="w-full mb-6 p-3 rounded-xl bg-white text-gray-500 placeholder-gray-500"
                    />
                    <button className="px-8 py-2 border-2 border-white text-white rounded-xl hover:bg-white hover:text-black transition">
                      Calculate
                    </button>
                  </div>
                )}
                {tab === 'stats' && (
                <div className="w-full flex flex-col items-start">
                    <h2 className="text-xl font-bold font-heading text-white mb-6 text-center w-full">STATS</h2>

                    {/* Total Miles */}
                    <div className="w-full mb-4">
                    <p className="text-white text-sm">Total Miles</p>
                    <div className="flex items-baseline space-x-2">
                        <p className="text-2xl font-bold text-white">00000000</p>
                        <p className="text-2xl font-bold text-white">mi</p>
                    </div>
                    <div className="w-full h-px bg-white opacity-30 mt-2"></div>
                    </div>

                    {/* Estimated Cost */}
                    <div className="w-full mb-4">
                    <p className="text-white text-sm">Estimated Cost of Trip</p>
                    <div className="flex items-baseline space-x-2">
                        <p className="text-2xl font-bold text-white">00.00</p>
                        <p className="text-2xl font-bold text-white">$</p>
                    </div>
                    <div className="w-full h-px bg-white opacity-30 mt-2"></div>
                    </div>

                    {/* Estimated Gas Efficiency */}
                    <div className="w-full mb-4">
                    <p className="text-white text-sm">Estimated Gas Efficiency</p>
                    <div className="flex items-baseline space-x-2">
                        <p className="text-2xl font-bold text-white">00000000</p>
                        <p className="text-2xl font-bold text-white">gal</p>
                    </div>
                    <div className="w-full h-px bg-white opacity-30 mt-2"></div>
                    </div>

                    {/* Estimated CO2 Emissions */}
                    <div className="w-full">
                    <p className="text-white text-sm">Estimated CO2 Emissions</p>
                    <div className="flex items-baseline space-x-2">
                        <p className="text-2xl font-bold text-white">00000000</p>
                        <p className="text-2xl font-bold text-white">kg</p>
                    </div>
                    </div>
                </div>
                )}
                {tab === 'carpool' && (
                <div className="w-full flex flex-col items-start">
                    <h2 className="text-xl font-bold font-heading text-white mb-6 text-center w-full">CARPOOL</h2>

                    {/* Carpool Description Text */}
                    <p className="text-white text-sm mb-6">
                    Reduce your trip’s carbon footprint by carpooling with friends or family.<br />
                    Every extra passenger means fewer cars on the road — and more CO₂ emissions saved.
                    </p>

                    {/* CO2 Savings */}
                    <div className="w-full">
                    <p className="text-white text-sm">CO2 Emissions Savings</p>
                    <div className="flex items-baseline space-x-2">
                        <p className="text-2xl font-bold text-white">00000000 <span className="text-2xl font-bold">kg</span></p>
                    </div>
                    </div>
                </div>
                )}
              </div>
            </div>
          ))}
        </div>

        {/* Map Section */}
        <div className="flex-1 bg-transparent flex items-center justify-center transition-all duration-500">
          {/* Placeholder for the future embedded Google Map */}
          <p className="text-white text-xl">[Google Map will be here]</p>
        </div>

      </div>
    </div>
  );
}

export default MapPage;
