import { Link } from 'react-router-dom';

function Navbar() {
  return (
    <nav className="bg-gray-800 p-4 text-white flex justify-around">
      <Link to="/">Home</Link>
      <Link to="/map">Map</Link>
      <Link to="/profile">Profile</Link>
    </nav>
  );
}

export default Navbar;
