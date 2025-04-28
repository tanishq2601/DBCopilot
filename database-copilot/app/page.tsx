"use client";
import { useState } from "react";
import { Moon, Sun } from "lucide-react";

export default function Home() {
  const [userQuery, setUserQuery] = useState("");
  const [response, setResponse] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [isDarkMode, setIsDarkMode] = useState(false);

  const handleQuery = async () => {
    if (!userQuery.trim()) return;
    setLoading(true);
    setError(null);

    try {
<<<<<<< HEAD
      const res = await fetch("http://localhost:8080/databse_copilot", {
=======
      const res = await fetch("http://localhost:8085/databse_copilot", {
>>>>>>> c55302b (final changes to perfect)
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ query: userQuery }),
      });

      if (!res.ok) {
        throw new Error(`HTTP error! Status: ${res.status}`);
      }

      const data = await res.json();
      setResponse(data.response);
    } catch (error) {
      console.error("Error fetching data:", error);
      setError("Failed to fetch response. Ensure the backend is running.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className={`min-h-screen flex flex-col items-center justify-center p-6 relative overflow-hidden ${isDarkMode ? 'bg-gray-900 text-white' : 'bg-white text-black'}`}>
      {/* Theme toggle button */}
      <button
        onClick={() => setIsDarkMode(!isDarkMode)}
        className="absolute top-4 right-4 p-2 rounded-full hover:bg-opacity-20 hover:bg-gray-500 transition z-20"
        aria-label="Toggle theme"
      >
        {isDarkMode ? <Sun size={24} /> : <Moon size={24} />}
      </button>

      {/* Grid-like background */}
      <div className="absolute inset-0 grid grid-cols-12 gap-4 opacity-20 pointer-events-none">
        {[...Array(100)].map((_, i) => (
          <div 
            key={i} 
            className={`w-full h-12 border ${isDarkMode ? 'border-white' : 'border-black'}`}
          ></div>
        ))}
      </div>
      
      <h1 className="text-4xl font-extrabold mb-6 relative z-10">MoonbergGPT 🚀</h1>

      <div className="w-full max-w-xl flex space-x-2 relative z-10">
        <input
          type="text"
          value={userQuery}
          onChange={(e) => setUserQuery(e.target.value)}
          placeholder="What are the top 5 token exchanges?"
          className={`flex-1 p-3 rounded border focus:outline-none focus:ring-2 focus:ring-blue-500 ${
            isDarkMode 
              ? 'bg-gray-800 text-white placeholder-gray-400 border-gray-600' 
              : 'bg-gray-200 text-black placeholder-gray-600 border-gray-400'
          }`}
                  />
        <button
          onClick={handleQuery}
          className="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700 transition disabled:opacity-50"
          disabled={loading}
        >
          {loading ? "Loading..." : "Run Query"}
        </button>
      </div>

      {error || response ? (
        <div className={`w-full max-w-2xl mt-6 p-6 rounded-lg shadow-lg relative z-10 ${
          isDarkMode ? 'bg-gray-800' : 'bg-gray-100'
        }`}>
          {error ? (
            <p className="text-red-600">{error}</p>
          ) : (
            <pre className={`whitespace-pre-wrap break-words p-4 rounded-lg border max-h-96 overflow-auto ${
              isDarkMode 
                ? 'text-green-400 bg-gray-700 border-gray-600' 
                : 'text-green-700 bg-gray-200 border-gray-400'
            }`}>{response}</pre>
          )}
        </div>
      ) : null}
    </div>
  );
}