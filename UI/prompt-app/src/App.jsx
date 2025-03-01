// import React, { useState } from "react";
// import axios from "axios";

// function App() {
//   const [prompt, setPrompt] = useState("");
//   const [response, setResponse] = useState("");
//   const [loading, setLoading] = useState(false);

//   const handleSubmit = async (e) => {
//     e.preventDefault();
//     if (!prompt) return;

//     setLoading(true);
//     setResponse("");

//     try {
//       const res = await axios.post("http://localhost:7777/api/generate", { prompt });
//       setResponse(res.data.response);
//     } catch (error) {
//       setResponse("Error fetching response.");
//     } finally {
//       setLoading(false);
//     }
//   };

//   return (
//     <div className="flex flex-col items-center justify-center min-h-screen bg-gradient-to-br from-purple-500 to-indigo-500">
//       <div className="w-full max-w-md bg-white bg-opacity-90 p-8 rounded-lg shadow-2xl transform transition-all duration-300 hover:scale-105">
//         <h1 className="text-3xl font-bold text-center mb-6 text-gray-800">
//         <div className="bg-red-500">Test</div>
//           Prompt Generator
//         </h1>
//         <form onSubmit={handleSubmit} className="space-y-6">
//           <input
//             type="text"
//             className="w-full p-3 border border-gray-300 rounded focus:outline-none focus:ring-2 focus:ring-indigo-500"
//             placeholder="Enter your prompt..."
//             value={prompt}
//             onChange={(e) => setPrompt(e.target.value)}
//           />
//           <button
//             type="submit"
//             className="w-full py-3 px-4 bg-indigo-600 hover:bg-indigo-700 transition-colors text-white font-semibold rounded shadow"
//           >
//             {loading ? "Loading..." : "Submit"}
//           </button>
//         </form>
//         {response && (
//           <div className="mt-8 p-4 bg-gray-100 rounded-lg shadow-inner">
//             <h2 className="text-xl font-semibold text-gray-700 mb-2">Response:</h2>
//             <p className="text-gray-600">{response}</p>
//           </div>
//         )}
//       </div>
//     </div>
//   );
// }

// export default App;
import React, { useState } from "react";
import axios from "axios";

function App() {
  // Your existing state and logic...

  return (
    <div>
      <div className="bg-red-500 text-white p-4">
        This div should have a red background.
      </div>
      {/* Rest of your component */}
    </div>
  );
}

export default App;