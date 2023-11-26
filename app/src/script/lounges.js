
import React, { useState, useEffect } from 'react';
import { useNavigate } from "react-router-dom";
import { MdOutlineLocationOn } from "react-icons/md";
import { GoPerson } from "react-icons/go";
import "../style/lounges.css";
import LoungeData from "../data/lounges.json";



// Location Component
const Location = ({ building, address }) => (
  <div className="location">
    <h2 className="building-name">{building}</h2>
    <div className="address-container">
      <MdOutlineLocationOn className="location-icon" size={24} />
      <p className="address-info">{address}</p>
    </div>
  </div>
);

// QueueStatus Component
const QueueStatus = ({ available, total, className }) => (
  <div className={`queue-status ${className}`}>
    <GoPerson className="person-icon" size={24} />
    <span>
      {available}/{total}
    </span>
  </div>
);

// ActionButton Component
const ActionButton = ({ onTakeSeat, className }) => (
  <button className={`take-seat-button ${className}`} onClick={onTakeSeat}>
    Take a seat
  </button>
);

// WaitingCard Component
const WaitingCard = ({ spaceName, info, onTakeSeat }) => {
  const { available, total } = info;
  const occupancyRate = (available / total) * 100;
  const colorClass =
    occupancyRate >= 80 ? "red" : occupancyRate >= 50 ? "orange" : "";

  return (
    <div className="waiting-card">
      <Location
        building={spaceName}
        address={info.address}
      />
      <div className="status-and-action">
        <QueueStatus available={available} total={total} className={colorClass} />
        <ActionButton onTakeSeat={onTakeSeat} className={colorClass} />
      </div>
    </div>
  );
};

const Lounges = () => {
  let navigate = useNavigate();
  const [waitingLists, setWaitingLists] = useState([]);

  useEffect(() => {
    // JSON 데이터가 배열 안에 객체 형태로 되어 있으므로 첫 번째 요소만 사용합니다.
    const loungeDataObject = LoungeData[0];
    const lists = Object.keys(loungeDataObject).map(key => ({
      spaceName: key,
      info: loungeDataObject[key]
    }));
    setWaitingLists(lists);
  }, []);

  const handleTakeSeat = () => {
    navigate("/lounge");
  };

  return (
    <div className="waiting-list-interface">
      {waitingLists.map((list, index) => (
        <WaitingCard key={index} spaceName={list.spaceName} info={list.info} onTakeSeat={handleTakeSeat} />
      ))}
    </div>
  );
};

export default Lounges;
