import LandingPage from './LandingPage';
import MapPage from './MapPage';

function HomePage() {
  return (
    <div className="h-screen overflow-y-scroll scroll-smooth">
      {/* Landing Section */}
      <section id="landing">
        <LandingPage />
      </section>

      {/* Map Section */}
      <section id="map" className="h-screen">
        <MapPage />
      </section>
    </div>
  );
}

export default HomePage;
