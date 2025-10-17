import { useState } from "react";

function App() {
  const [isOpen, setIsOpen] = useState(false);

  const BACKEND_URL = "http://127.0.0.1:8000";

  const handleSpotifyLogin = () => {
    window.location.href = `${BACKEND_URL}/auth/spotify/login`;
  };


  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-900 text-white">
      <div className="w-96 bg-gray-800 rounded-2xl shadow-lg p-6">



        <button
          onClick={() => setIsOpen(!isOpen)}
          className="w-full text-xl font-bold text-center hover:text-cyan-400 transition"
        >
          Menú de inicio
        </button>



        {isOpen && (
            
            <div className="mt-4 p-4 bg-gray-700 rounded-xl">
            <button
              onClick={handleSpotifyLogin}
              className="w-full text-xl font-sans text-center hover:text-cyan-400 transition"
            >
              Spotify
            </button>


            <button
              onClick={()=> console.log('youtube')}
              className="w-full text-xl font-sans text-center hover:text-cyan-400 transition"
            >
              toutube
            </button>









          </div>
        )}
      </div>
    </div>
  );
}

export default App;
