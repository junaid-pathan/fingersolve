import React from 'react';
import ReactDOM from 'react-dom/client';
import './index.css';
import HandGestureMathQuiz from './HandGestureMathQuiz';

const root = ReactDOM.createRoot(
  document.getElementById('root') as HTMLElement
);

root.render(
  <React.StrictMode>
    <HandGestureMathQuiz />
  </React.StrictMode>
);