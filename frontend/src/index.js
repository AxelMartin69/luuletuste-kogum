import React from 'react';
import ReactDOM from 'react-dom/client';
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import App from './components/App';
import LogIn from './components/LogIn';
import MyPoems from './components/MyPoems';

const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(
    <BrowserRouter>
        <Routes>
            <Route path="/" element={<App />} />
            <Route path="/login" element={<LogIn />} />
            <Route path="/my-poems" element={<MyPoems />} />
        </Routes>
    </BrowserRouter>
);
