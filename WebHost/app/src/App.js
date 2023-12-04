import React from "react";
import { BrowserRouter as Router, Route, Routes } from "react-router-dom";
import Intro from "./script/intro.js";
import Lounges from "./script/lounges.js";
import Lounge from "./script/lounge.js";
import Nav from "./script/nav.js"
import Info from "./script/info.js"

const App = () => {
  return (
    <Router>
      <Routes>
        {/* <Route path="/" element={<Intro />} />
        <Route path="/lounges" element={<><Lounges /> <Nav/></>} /> 
        <Route path="/lounge" element={<><Lounge /> <Nav/></>} /> */}
      </Routes>
    </Router>
  );
};

export default App;
