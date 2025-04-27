import { Link } from 'react-router-dom';
import background from '../assets/background.png';
import logo from '../assets/logo.png';
import gasPump from '../assets/gas-pump.png';
import PageWrapper from '../components/PageWrapper';

function LandingPage() {
    return (
      <div
        className="relative min-h-screen bg-cover bg-center bg-no-repeat flex flex-col"
        style={{ backgroundImage: `url(${background})` }}
      >
        {/* MAIN CONTENT AREA */}
        <div className="flex flex-col md:flex-row items-center justify-center pt-8 md:pt-4 px-8">
          
          {/* LEFT SIDE - Logo and Text */}
          <div className="flex flex-col items-start max-w-lg w-full">
            {/* Logo Image */}
            <img src={logo} alt="Kirkland Route Logo" className="w-full max-w-md mb-8" />

            {/* Heading */}
            <h1 className="text-[36px] font-extrabold font-heading text-white leading-tight mb-6">
              Costco Gas Station Based Roadtrip Planner
            </h1>

            {/* Paragraph Text */}
            <p className="text-[16px] text-white leading-relaxed mb-2">
              The Kirkland Route makes roadtripping easy with a map-first, Costco-optimized trip planner.
            </p>
            <p className="text-[16px] text-white leading-relaxed mb-2">
              Input your origin and destination, and we'll automatically calculate the best route with Costco Gas Station stops along the way.
            </p>
            <p className="text-[16px] text-white leading-relaxed mb-2">
              Customize your drive with your car’s MPG, tank size, and a fuel buffer so you're never running on empty.
            </p>
            <p className="text-[16px] text-white leading-relaxed mb-6">
              Get a trip-wide fuel cost estimate using real gas prices — and make every mile and every dollar count.
            </p>

            {/* Plan Your Trip Button */}
            <a href="#map">
              <button className="border-2 border-white text-white text-[25px] font-bold px-8 py-4 rounded-xl hover:bg-white hover:text-black transition">
                Plan Your Trip
              </button>
            </a>
          </div>

          {/* RIGHT SIDE - Gas Pump Image */}
          <div className="mt-12 md:mt-24 md:ml-32">
            <img src={gasPump} alt="Gas Pump" className="w-[410px]" />
          </div>

        </div>

        {/* Gradient Fade at Bottom */}
        <div className="absolute bottom-0 w-full h-40 bg-gradient-to-b from-transparent to-[#0f1b21] pointer-events-none"></div>

        {/* Spacer at bottom to create breathing room before MapPage */}
        <div className="h-24"></div>  
      </div>
    );
}

export default LandingPage;
