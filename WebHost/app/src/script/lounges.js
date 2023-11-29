import React, { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import { MdOutlineLocationOn } from "react-icons/md";
import { GoPerson } from "react-icons/go";
import "../style/lounges.css";
import LoungeData from "../data/lounges.json";

// Get Data
async function fetchLoungeData() {
  const response = await fetch("/data/getSpace/");
  const data = response.json();
  return data;
}

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
      <Location building={spaceName} address={info.address} />
      <div className="status-and-action">
        <QueueStatus
          available={available}
          total={total}
          className={colorClass}
        />
        <ActionButton onTakeSeat={onTakeSeat} className={colorClass} />
      </div>
    </div>
  );
};

const Lounges = () => {
  let navigate = useNavigate();
  const [waitingLists, setWaitingLists] = useState([]);

  // const getLoungeData = async () => {
  //   const res = await fetch("/data/getSpace/").then((res) => res.json);
  // };

  //console.log(getLoungeData);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const temp = await fetchLoungeData();
        console.log(temp);

        const lists = temp.map((lounge) => ({
          spaceName: lounge.name,
          info: {
            available: lounge.available,
            total: lounge.total,
            address: lounge.address,
          },
        }));

        setWaitingLists(lists);
      } catch (error) {
        console.error("Error fetching lounge data:", error);
      }
    };

    fetchData();
  }, []);

  const handleTakeSeat = () => {
    navigate("/lounge");
  };

  return (
    <div className="waiting-list-interface">
      {waitingLists.map((list, index) => (
        <WaitingCard
          key={index}
          spaceName={list.spaceName}
          info={list.info}
          onTakeSeat={handleTakeSeat}
        />
      ))}
    </div>
  );
};

export default Lounges;
