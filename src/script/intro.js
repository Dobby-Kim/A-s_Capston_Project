import React, { useEffect } from "react";
import { useNavigate } from "react-router-dom";
import "../style/intro.css";
import title_image from "../img/Empty Seats.png";
import logo_image from "../img/chair.png";
import team_image from "../img/team A’s.png";
import skku_image from "../img/skku.png";

// intro 화면을 터치하거나 3초간 대기하면 화면 전환
const Intro = () => {
  let navigate = useNavigate();

  useEffect(() => {
    const timer = setTimeout(() => {
      navigate("/lounges");
    }, 3000);

    return () => clearTimeout(timer);
  }, [navigate]);

  // Handler for click or touch event
  const handleTouch = () => {
    navigate("/lounges");
  };

  return (
    <div
      className="intro-container"
      onClick={handleTouch}
      onTouchStart={handleTouch}
    >
      <img src={title_image} alt="Title Image" className="title-image" />
      <img src={logo_image} alt="Logo Image" className="logo-image" />
      <img src={team_image} alt="Team Image" className="team-image" />
      <img src={skku_image} alt="SKKU Image" className="skku-image" />
    </div>
  );
};

export default Intro;
