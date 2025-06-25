import { Routes, Route } from 'react-router-dom'
import HomePage from './home'
import HandGestureMathQuiz from './HandGestureMathQuiz'

export default function App() {
  return (
    <Routes>
      <Route path="/" element={<HomePage />} />
      <Route path="/quiz" element={<HandGestureMathQuiz />} />
    </Routes>
  )
}
