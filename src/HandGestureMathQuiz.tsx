import React, { useEffect, useState, useRef } from "react";
import { motion } from "framer-motion";

export default function HandGestureMathQuiz() {
  const [mathProblem, setMathProblem] = useState("Loading...");
  const [prediction, setPrediction] = useState("");
  const [noHandMessage, setNoHandMessage] = useState("");
  const [score, setScore] = useState(0);
  const [showCorrect, setShowCorrect] = useState(false);

  const videoRef = useRef<HTMLVideoElement>(null);
  const answerRef = useRef<number>(0);
  const num1Ref = useRef<number>(0);
  const num2Ref = useRef<number>(0);
  const opRef = useRef<string>("+");
  const canvasRef = useRef<HTMLCanvasElement | null>(null);

  const generateMathProblem = () => {
    while (true) {
      const num1 = Math.floor(Math.random() * 10);
      const num2 = Math.floor(Math.random() * 10);
      const op = Math.random() > 0.5 ? "+" : "-";
      const result = op === "+" ? num1 + num2 : num1 - num2;

      if (result >= 1 && result <= 9) {
        num1Ref.current = num1;
        num2Ref.current = num2;
        opRef.current = op;
        answerRef.current = result;
        setMathProblem(`${num1} ${op} ${num2}`);
        break;
      }
    }
  };

  const setupWebcam = async () => {
    try {
      const stream = await navigator.mediaDevices.getUserMedia({ video: true });
      if (videoRef.current) {
        videoRef.current.srcObject = stream;
      }
    } catch (error) {
      console.error("Error accessing webcam:", error);
    }
  };

  const captureAndPredict = async () => {
    if (!videoRef.current || videoRef.current.videoWidth === 0) return;

    const video = videoRef.current;

    if (!canvasRef.current) {
      canvasRef.current = document.createElement("canvas");
    }

    const canvas = canvasRef.current;
    canvas.width = video.videoWidth;
    canvas.height = video.videoHeight;

    const ctx = canvas.getContext("2d");
    if (!ctx) return;

    ctx.drawImage(video, 0, 0, canvas.width, canvas.height);
    const imageData = canvas.toDataURL("image/jpeg");

    try {
      const controller = new AbortController();
      const timeoutId = setTimeout(() => controller.abort(), 5000);

      const res = await fetch("http://localhost:5000/predict", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ image: imageData }),
        signal: controller.signal,
      });

      clearTimeout(timeoutId);

      if (!res.ok) {
        throw new Error(`Server responded with status: ${res.status}`);
      }

      const result = await res.json();
      const predictedRaw = result.prediction;

      const labelToDigit: Record<string, number> = {
        Zero: 0,
        One: 1,
        Two: 2,
        Three: 3,
        Four: 4,
        Five: 5,
        Six: 6,
        Seven: 7,
        Eight: 8,
        Nine: 9,
      };

      const predicted =
        predictedRaw.charAt(0).toUpperCase() + predictedRaw.slice(1).toLowerCase();

      if (predicted === "Nohand") {
        setNoHandMessage("No hand detected");
        setPrediction("");
      } else if (predicted in labelToDigit) {
        setNoHandMessage("");
        setPrediction(predicted);

        if (labelToDigit[predicted] === answerRef.current) {
          setShowCorrect(true);
          setScore((prev) => prev + 1);

          setTimeout(() => {
            setShowCorrect(false);
            generateMathProblem();
          }, 3000);
        }
      }
    } catch (error) {
      if ((error as any).name === "AbortError") {
        setNoHandMessage("API request timed out");
      } else {
        console.error("Prediction error:", error);
        setNoHandMessage("Error: " + (error as Error).message);

      }
    }
  };

  useEffect(() => {
    const initialize = async () => {
      await setupWebcam();
      generateMathProblem();

      videoRef.current?.addEventListener("loadedmetadata", () => {
        const interval = setInterval(captureAndPredict, 1000);
        return () => clearInterval(interval);
      });
    };

    initialize();

    return () => {
      if (videoRef.current && videoRef.current.srcObject) {
        const stream = videoRef.current.srcObject as MediaStream;
        stream.getTracks().forEach((track) => track.stop());
      }
    };
  }, []);

  return (
    <div className="min-h-screen bg-gradient-to-br from-indigo-50 to-purple-50 flex flex-col items-center justify-center p-4">
      <div className="max-w-4xl w-full bg-white rounded-2xl shadow-xl overflow-hidden">
        <div className="bg-gradient-to-r from-purple-600 to-indigo-600 p-6 text-white">
          <h1 className="text-3xl font-bold text-center">Hand Gesture Math Quiz</h1>
          <p className="text-center opacity-90 mt-2">Show your answer with hand gestures!</p>
        </div>

        <div className="p-6">
          <div className="flex flex-col md:flex-row gap-8">
            <div className="flex-1">
              <div className="bg-gradient-to-br from-indigo-100 to-purple-100 p-6 rounded-xl shadow-md">
                <div className="text-center mb-4">
                  <div className="text-sm uppercase tracking-wider text-indigo-600 font-semibold">Current Problem</div>
                  <div className="text-4xl font-bold mt-2 text-gray-800">{mathProblem}</div>
                </div>

                <div className="flex justify-between items-center">
                  <div className="bg-white px-4 py-2 rounded-lg shadow-sm">
                    <span className="text-sm text-gray-600">Score</span>
                    <div className="text-2xl font-bold text-indigo-600">{score}</div>
                  </div>

                  {prediction && (
                    <div className="bg-white px-4 py-2 rounded-lg shadow-sm">
                      <span className="text-sm text-gray-600">Your Answer</span>
                      <div className="text-2xl font-bold text-green-600">{prediction}</div>
                    </div>
                  )}
                </div>

                {noHandMessage && (
                  <div className="mt-4 text-center text-red-500 bg-red-50 p-2 rounded-lg">{noHandMessage}</div>
                )}
              </div>

              <div className="mt-6 text-center text-gray-600">
                <p>Hold up your hand showing the correct number of fingers to answer!</p>
              </div>
            </div>

            <div className="flex-1 relative">
              <div className="relative overflow-hidden rounded-xl border-4 border-indigo-200 shadow-lg bg-black">
                <video ref={videoRef} className="w-full h-auto transform scale-x-[-1]" autoPlay playsInline />

                <div className="absolute inset-0 border-[3px] border-white border-opacity-20 rounded-lg pointer-events-none"></div>

                <div className="absolute top-3 left-3 w-3 h-3 bg-red-500 rounded-full animate-pulse"></div>
                <div className="absolute top-3 right-3 w-20 h-6 bg-black bg-opacity-50 rounded-full flex items-center justify-center text-white text-xs">
                  LIVE
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      {showCorrect && (
        <motion.div
          initial={{ scale: 0.5, opacity: 0 }}
          animate={{ scale: 1, opacity: 1 }}
          exit={{ scale: 1.5, opacity: 0 }}
          className="fixed inset-0 flex items-center justify-center pointer-events-none"
        >
          <div className="bg-green-500 text-white text-4xl font-bold rounded-full w-32 h-32 flex items-center justify-center shadow-lg">
            ✓ Correct!
          </div>
        </motion.div>
      )}
    </div>
  );
}
