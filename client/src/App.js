import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom'

// Pages
import Home from './views/Home';
// import Alerts from './views/Alerts';
// import Rules from './views/Rules';
// import Setup from './views/Setup';
// import Settings from './views/Settings';

// COmponents
import NavBar from './components/NavBar'
import Footer from './components/Footer'

function App() {
  return (
    <Router>
      <NavBar/>
        <Routes>
          <Route path='/' element={<Home/>}/>
        </Routes>
      <Footer/>
    </Router>
  );
}

export default App;
