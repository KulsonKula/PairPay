import { StrictMode } from 'react';
import { createRoot } from 'react-dom/client';
import './index.css';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import App from './App.jsx'; 
import Login from './Login.jsx';
import Register from './Register.jsx';
import { NextUIProvider } from '@nextui-org/react';

createRoot(document.getElementById('root')).render(
  <StrictMode>
    <NextUIProvider className="dark text-foreground bg-background">
    <Router> 
        <main>
          <Routes>
            <Route path="/" element={<App />} /> 
            <Route path="/register" element={<Register />} />
            <Route path="/login" element={<Login />} />
          </Routes>
        </main>
      </Router>
    </NextUIProvider>
  </StrictMode>,
)
