import React from 'react';
import { useNavigate } from 'react-router-dom';
export default function HomePage() {
    const navigate = useNavigate()
  return (
    <div className="min-h-screen bg-gradient-to-b from-purple-500 to-indigo-600 text-white font-sans">
      <section className="text-center py-16 px-4">
        <h1 className="text-5xl font-bold mb-4">FingerSolve</h1>
        <p className="text-lg mb-6">Solve Math with Just Your Hands!</p>
        <p className="text-sm mb-8 text-white/80">
          AI-powered gesture recognition for fun, interactive learning.
        </p>
        <div className="flex justify-center gap-4">
          <button onClick={()=>navigate('/quiz')} className="bg-white text-purple-600 font-semibold px-6 py-2 rounded-2xl shadow hover:scale-105 transition">
            Start Now
          </button>
          
        </div>
      </section>

      {/* How It Works */}
      <section className="bg-white text-gray-800 py-16 px-6 rounded-t-3xl">
        <h2 className="text-3xl font-bold text-center mb-8">How It Works</h2>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-8 text-center">
          <div>
            <div className="text-5xl mb-2">1️⃣</div>
            <p>Show fingers on camera</p>
          </div>
          <div>
            <div className="text-5xl mb-2">2️⃣</div>
            <p>We detect your answer</p>
          </div>
          <div>
            <div className="text-5xl mb-2">3️⃣</div>
            <p>You get instant feedback</p>
          </div>
        </div>
    </section>
    </div>
  );
}
