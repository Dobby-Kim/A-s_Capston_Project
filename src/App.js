import React from "react";
import { BrowserRouter as Router, Route, Routes } from "react-router-dom";
import Intro from "./script/intro.js";
import Lounges from "./script/lounges.js";
import Lounge from "./script/lounge.js";

const App = () => {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<Intro />} />
        <Route path="/lounges" element={<Lounges />} />
        <Route path="/lounge" element={<Lounge />} />
      </Routes>
    </Router>
  );
};

export default App;
