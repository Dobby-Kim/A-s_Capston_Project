import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import { MdOutlineLocationOn } from "react-icons/md";
import { GoPerson } from "react-icons/go";
import "../style/lounges.css";

const Location = ({ building, address }) => (
  <div className="location">
    <h2 className="building-name">{building}</h2>
    <div className="address-container">
      <MdOutlineLocationOn className="location-icon" size={24} />
      <p className="address-info">{address}</p>
    </div>
  </div>
);

const QueueStatus = ({ current, total, className }) => (
  <div className={`queue-status ${className}`}>
    <GoPerson className="person-icon" size={24} />
    <span>
      {current}/{total}
    </span>
  </div>
);

const ActionButton = ({ onTakeSeat, className }) => (
  <button className={`take-seat-button ${className}`} onClick={onTakeSeat}>
    Take a seat
  </button>
);

const WaitingCard = ({ list, onTakeSeat }) => {
  const { current, total } = list.queueStatus;
  const occupancyRate = (current / total) * 100;
  const colorClass =
    occupancyRate >= 80 ? "red" : occupancyRate >= 50 ? "orange" : "";

  return (
    <div className="waiting-card">
      <Location
        building={list.building}
        address={list.address}
        floor={list.floor}
      />
      <div className="status-and-action">
        <QueueStatus current={current} total={total} className={colorClass} />
        <ActionButton onTakeSeat={onTakeSeat} className={colorClass} />
      </div>
    </div>
  );
};

const Lounges = () => {
  let navigate = useNavigate();
  const [waitingLists, setWaitingLists] = useState([
    {
      building: "ParkSangJo Lounge",
      address: "Engineering Building 2, Floor 1",
      queueStatus: { current: 3, total: 18 },
    },
    {
      building: "Haedong 1",
      address: "Engineering Building 1, Floor 1",
      queueStatus: { current: 45, total: 48 },
    },
    {
      building: "Haedong 2",
      address: "Engineering Building 1, Floor B1",
      queueStatus: { current: 42, total: 80 },
    },
    {
      building: "Engineering Library",
      address: "Engineering Building 2, Floor B1",
      queueStatus: { current: 6, total: 70 },
    },
  ]);

  const handleTakeSeat = () => {
    navigate("/lounge");
  };

  return (
    <div className="waiting-list-interface">
      {waitingLists.map((list, index) => (
        <WaitingCard key={index} list={list} onTakeSeat={handleTakeSeat} />
      ))}
    </div>
  );
};

export default Lounges;
