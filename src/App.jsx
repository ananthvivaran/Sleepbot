import React, { useState } from "react";
import axios from "axios";
import moonIcon from './moon.jpeg'; // Your local moon image

function App() {
  const [question, setQuestion] = useState("");
  const [chatHistory, setChatHistory] = useState([]);

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!question.trim()) return;

    const newHistory = [...chatHistory, { question, answer: "Thinking..." }];
    setChatHistory(newHistory);
    setQuestion("");

    try {
      const response = await axios.get("http://localhost:8080/ask", {
        params: { question },
      });
      const newAnswer = response.data?.answer || "No response from server";
      setChatHistory((prev) =>
        prev.map((item, index) =>
          index === newHistory.length - 1 ? { ...item, answer: newAnswer } : item
        )
      );
    } catch (error) {
      console.error("API Error:", error);
      setChatHistory((prev) =>
        prev.map((item, index) =>
          index === newHistory.length - 1
            ? { ...item, answer: "Error: " + (error.message || "Unknown") }
            : item
        )
      );
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center relative">
      <div className="bg-black bg-opacity-90 p-6 rounded-xl shadow-2xl w-full max-w-2xl mx-auto transform transition-all duration-300 hover:scale-105 relative">
        <div className="flex items-center justify-center mb-6">
          <img src={moonIcon} alt="Moon Icon" className="mr-2 w-12 h-12" />
          <h1 className="text-3xl font-bold text-gray-300">Sleep Chatbot</h1> {/* Light gray text for readability on black */}
        </div>
        <div className="h-96 overflow-y-auto mb-6 p-4 border rounded-xl bg-black relative">
          {/* Blinking Stars across the whole chat area */}
          <div className="absolute inset-0">
            <span className="star blink"></span>
            <span className="star blink" style={{ left: '50px', top: '20px' }}></span>
            <span className="star blink" style={{ left: '100px', top: '10px' }}></span>
            <span className="star blink" style={{ left: '150px', top: '50px' }}></span>
            <span className="star blink" style={{ left: '200px', top: '30px' }}></span>
          </div>
          {chatHistory.map((chat, index) => (
            <div key={index} className="mb-4 fade-in">
              <p className="font-semibold text-gray-200">You: {chat.question}</p> {/* Lighter text for readability */}
              <p className="text-gray-400 break-words">
                {chat.answer}
                {index === chatHistory.length - 1 && (
                  <img src="https://img.icons8.com/ios/20/000000/bed.png" alt="Sleep Icon" className="inline ml-2" />
                )}
              </p>
            </div>
          ))}
        </div>
        <form onSubmit={handleSubmit} className="flex gap-4">
          <input
            type="text"
            value={question}
            onChange={(e) => setQuestion(e.target.value)}
            placeholder="Ask about sleep..."
            className="flex-1 p-3 border rounded-lg focus:outline-none focus:ring-2 focus:ring-indigo-500 text-gray-800 bg-gray-800 text-white"
          />
                <button
                  type="submit"
                  className="bg-gradient-to-r from-indigo-500 to-purple-600 text-white p-3 rounded-lg hover:from-indigo-600 hover:to-purple-700 focus:outline-none focus:ring-2 focus:ring-indigo-500"
                >
                  Send
                          </button>
                        </form>
                </div>
              </div>
            );
          }
          
          export default App;