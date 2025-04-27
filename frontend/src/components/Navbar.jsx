import { Link, useLocation, useNavigate } from 'react-router-dom';
import logo from '../assets/logo.png'; // <-- Import your logo!

function Navbar() {
  const location = useLocation();
  const navigate = useNavigate();

  const handleHomeClick = () => {
    if (location.pathname === '/') {
      const landingSection = document.getElementById('landing');
      if (landingSection) {
        landingSection.scrollIntoView({ behavior: 'smooth' });
      } else {
        // Fallback if landing section isn't found
        window.scrollTo({ top: 0, behavior: 'smooth' });
      }
    } else {
      navigate('/');
    }
  };
  

  return (
    <div className="sticky top-0 z-50 bg-[#0f1b21] flex justify-between items-center p-5 pr-20 pt-8">
      
      {/* LEFT SIDE - Logo */}
      <div className="flex items-center space-x-4 pl-8">
        <img src={logo} alt="Kirkland Route Logo" className="w-32" />
      </div>

      {/* RIGHT SIDE - Nav Links */}
      <div className="flex items-center space-x-12">
        {/* HOME - now a button */}
        <button 
          onClick={handleHomeClick}
          className="text-white font-bold text-[18px] hover:text-red-600 transition-colors duration-300"
        >
          HOME
        </button>

        {/* MAP - still a Link */}
        <Link 
          to="/map" 
          className="text-white font-bold text-[18px] hover:text-red-600 transition-colors duration-300"
        >
          MAP
        </Link>

        {/* PROFILE - still a Link */}
        <Link 
          to="/profile" 
          className="text-white font-bold text-[18px] hover:text-red-600 transition-colors duration-300"
        >
          PROFILE
        </Link>
      </div>

    </div>
  );
}

export default Navbar;
