// IMPORT LINK COMPONENT - from React Router to navigate to other pages
import { Link } from 'react-router-dom';

// IMPORT IMAGE ASSETS
import background from '../assets/background.png';
import logo from '../assets/logo.png';
import gasPump from '../assets/gas-pump.png';

function LandingPage() {
    return (
      // Outer container div for the entire page
      <div
        className="min-h-screen bg-cover bg-center bg-no-repeat flex flex-col"
        style={{ backgroundImage: `url(${background})` }} // background image
      >
  
        {/* MAIN CONTENT AREA */}
        <div className="flex flex-col md:flex-row items-center justify-center flex-grow px-8">
          
          {/* LEFT SIDE - Logo and Text */}
          <div className="flex flex-col items-start max-w-lg">
            {/* Logo Image */}
            <img src={logo} alt="Kirkland Route Logo" className="w-64 mb-8" />
  
            {/* Heading */}
            <h1 className="text-[34px] font-semibold text-white leading-tight mb-6">
              Costco Gas Station Based Roadtrip Planner
            </h1>
  
            {/* Paragraph Text */}
            <p className="text-[16px] text-white leading-relaxed mb-8">
              The Kirkland Route makes roadtripping easy with a map-first, Costco-optimized trip planner.
              <br /><br />
              Input your origin and destination, and we'll automatically calculate the best route with Costco Gas Station stops along the way.
              <br /><br />
              Customize your drive with your car’s MPG, tank size, and a fuel buffer so you're never running on empty.
              <br /><br />
              Get a trip-wide fuel cost estimate using real gas prices — and make every mile and every dollar count.
            </p>
  
            {/* Plan Your Trip Button */}
            <Link to="/map">
              <button className="border-2 border-white text-white text-[25px] font-bold px-8 py-4 rounded hover:bg-white hover:text-black transition">
                Plan Your Trip
              </button>
            </Link>
          </div>
  
          {/* RIGHT SIDE - Gas Pump Image */}
          <div className="mt-12 md:mt-0 md:ml-12">
            <img src={gasPump} alt="Gas Pump" className="w-[320px]" />
          </div>
  
        </div>
      </div>
    );
  }
  
  // Export the LandingPage component so it can be used elsewhere
  export default LandingPage;