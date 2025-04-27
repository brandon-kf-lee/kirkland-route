import { Link } from 'react-router-dom';

function LandingPage() {
  return (
    <div className="flex flex-col items-center justify-center h-full text-center p-8">
      <h1 className="text-4xl font-bold mb-6">Welcome to Kirkland Route</h1>
      <p className="mb-6 text-lg">Plan your road trip with Costco gas stations along the way!</p>
      <Link to="/map">
        <button className="px-6 py-2 bg-red-600 text-white rounded hover:bg-red-700">
          Plan Your Trip
        </button>
      </Link>
    </div>
  );
}

export default LandingPage;
