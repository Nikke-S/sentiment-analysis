import { useState } from "react";

export default function App() {
  const [text, setText] = useState("");
  const [model, setModel] = useState("custom");
  const [result, setResult] = useState({ sentiment: "", confidence: "" });
  const [loading, setLoading] = useState(false);

  const analyzeSentiment = async () => {
    setLoading(true);
    try {
      const response = await fetch("http://127.0.0.1:8000/analyze/", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ text, model }),
      });
      const data = await response.json();
      setResult(data);
    } catch (error) {
      console.error("Error analyzing sentiment:", error);
    }
    setLoading(false);
  };

  return (
    <div className="bg-gray-100 min-h-screen p-6">
      <div className="max-w-2xl w-full p-6 bg-white shadow-md rounded-xl">
        <h2 className="text-2xl font-bold mb-2">Movie Review Sentiment Analysis</h2>
        <p className="text-sm text-gray-600 mb-4">
          This app allows you to analyze the sentiment of a movie review using two models:
          <br />
          <strong>Custom Model:</strong> A fine-tuned version of distilbert-base-uncased on the IMDB
          movie reviews dataset for binary sentiment classification (positive vs. negative).
          <br />
          <strong>Llama 3:</strong> A powerful large language model for general-purpose text analysis.
        </p>

        <textarea
          className="w-full p-3 border rounded-md focus:outline-none focus:ring-2 focus:ring-blue-400"
          rows="4"
          placeholder="Enter your text here..."
          value={text}
          onChange={(e) => setText(e.target.value)}
        />

        <div className="mt-3">
          <select
            className="w-full p-2 border rounded-md"
            value={model}
            onChange={(e) => setModel(e.target.value)}
          >
            <option value="custom">Custom Model</option>
            <option value="llama">Llama 3</option>
          </select>
        </div>

        <button
          onClick={analyzeSentiment}
          className="w-full mt-4 p-2 bg-blue-500 text-white font-semibold rounded-md hover:bg-blue-600 transition duration-300"
          disabled={loading}
        >
          {loading ? "Analyzing..." : "Analyze Sentiment"}
        </button>

        <div className="mt-4 p-3 bg-gray-200 rounded-md text-center">
          <p className="text-lg font-semibold">
            Sentiment:{" "}
            <span className="text-blue-600">
              {result.sentiment || "Not Analyzed Yet"}
            </span>
          </p>
          <p className="text-lg font-semibold">
            Confidence:{" "}
            <span className="text-blue-600">
              {result.confidence ? result.confidence.toFixed(2) : "Not Available"}
            </span>
          </p>
        </div>
      </div>
    </div>
  );
}
