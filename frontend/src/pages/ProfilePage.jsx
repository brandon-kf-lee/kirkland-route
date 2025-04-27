import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import background from '../assets/background-map.png';

function ProfilePage() {
  const navigate = useNavigate();
  const [isLoggedIn, setIsLoggedIn] = useState(false);
  const [formData, setFormData] = useState({
    username: '',
    password: '',
    firstName: '',
    lastName: '',
    carMpg: '',
    tankSize: '',
    fuelBuffer: '',
  });

  useEffect(() => {
    const loggedInStatus = localStorage.getItem('loggedIn');
    setIsLoggedIn(loggedInStatus === 'true');
  }, []);

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleLogin = (e) => {
    e.preventDefault();
    localStorage.setItem('loggedIn', 'true');
    setIsLoggedIn(true);
  };

  const handleProfileSave = (e) => {
    e.preventDefault();
    localStorage.setItem('profileData', JSON.stringify(formData));
    alert('Profile saved successfully!');
  };

  return (
    <div
      className="min-h-screen bg-cover bg-center flex items-center justify-center"
      style={{ backgroundImage: `url(${background})` }}
    >
      {/* Card */}
      <div className="bg-white rounded-2xl shadow-lg p-10 w-[350px] flex flex-col items-center">
        {!isLoggedIn ? (
          <>
            {/* Login Form */}
            <h1 className="text-2xl font-bold font-heading mb-2 text-center">HI TRAVELER!</h1>
            <p className="text-gray-600 mb-8 text-center">Welcome to Kirkland Route</p>

            <form onSubmit={handleLogin} className="w-full flex flex-col items-center">
              <div className="mb-4 w-full">
                <label className="block text-gray-700 mb-2">Username</label>
                <input
                  name="username"
                  type="text"
                  value={formData.username}
                  onChange={handleChange}
                  className="w-full border-2 border-gray-300 rounded-md p-2"
                />
              </div>
              <div className="mb-6 w-full">
                <label className="block text-gray-700 mb-2">Password</label>
                <input
                  name="password"
                  type="password"
                  value={formData.password}
                  onChange={handleChange}
                  className="w-full border-2 border-gray-300 rounded-md p-2"
                />
              </div>
              <button
                type="submit"
                className="bg-[#D14433] text-white font-bold py-2 px-8 rounded-md hover:bg-red-600 transition mt-4"
              >
                Login
              </button>
            </form>
          </>
        ) : (
          <>
            {/* Profile Form */}
            <h1 className="text-2xl font-bold font-heading mb-2 text-center" style={{ color: '#0f1b21' }}>
              HI TRAVELER!
            </h1>
            <p className="text-gray-600 mb-8 text-center">Update your vehicle info</p>

            <form onSubmit={handleProfileSave} className="w-full flex flex-col items-center">
              <div className="mb-4 w-full">
                <label className="block text-gray-700 mb-2">First Name</label>
                <input
                  name="firstName"
                  type="text"
                  value={formData.firstName}
                  onChange={handleChange}
                  className="w-full border-2 border-gray-300 rounded-md p-2"
                />
              </div>

              <div className="mb-4 w-full">
                <label className="block text-gray-700 mb-2">Last Name</label>
                <input
                  name="lastName"
                  type="text"
                  value={formData.lastName}
                  onChange={handleChange}
                  className="w-full border-2 border-gray-300 rounded-md p-2"
                />
              </div>

              <div className="mb-4 w-full">
                <label className="block text-gray-700 mb-2">Car MPG</label>
                <input
                  name="carMpg"
                  type="number"
                  value={formData.carMpg}
                  onChange={handleChange}
                  className="w-full border-2 border-gray-300 rounded-md p-2"
                />
              </div>

              <div className="mb-4 w-full">
                <label className="block text-gray-700 mb-2">Tank Size</label>
                <input
                  name="tankSize"
                  type="number"
                  value={formData.tankSize}
                  onChange={handleChange}
                  className="w-full border-2 border-gray-300 rounded-md p-2"
                />
              </div>

              <div className="mb-8 w-full">
                <label className="block text-gray-700 mb-2">Fuel Buffer (%)</label>
                <input
                  name="fuelBuffer"
                  type="number"
                  value={formData.fuelBuffer}
                  onChange={handleChange}
                  className="w-full border-2 border-gray-300 rounded-md p-2"
                />
              </div>

              <button
                type="submit"
                className="bg-[#D14433] text-white font-bold py-2 px-8 rounded-md hover:bg-red-600 transition"
              >
                Save Profile
              </button>
            </form>
          </>
        )}
      </div>
    </div>
  );
}

export default ProfilePage;
