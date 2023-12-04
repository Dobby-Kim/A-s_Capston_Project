
import React, { useState, useEffect } from 'react';
import { createSearchParams, useNavigate } from "react-router-dom";
import { MdOutlineLocationOn } from "react-icons/md";
import { PiChairLight } from "react-icons/pi";
import "../style/lounges.css";
import LoungeData from "../data/lounges.json";
import LoungeData2 from "../data/lounges2.json";
import Nav3 from "../script/nav"

// Get Data
async function fetchLoungesData() {
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
    <PiChairLight className="person-icon" size={24} />
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
    occupancyRate <= 20 ? "red" : occupancyRate <= 50 ? "orange" : "";

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
  const navigate = useNavigate();
  const [waitingLists, setWaitingLists] = useState([]);

  // Json으로 테스트하기 위해서
  useEffect(() => {
    const loungeDataObject = LoungeData2;
    const lists = loungeDataObject.map((lounge) => ({
      spaceName: lounge.name,
      info: {
        address: lounge.address,
        available: lounge.available,
        total: lounge.total,
      }
    }));

    setWaitingLists(lists);
  }, []);

  // Server 연결 시 사용
  /*useEffect(() => {
    const fetchData = async () => {
      try {
        const temp = await fetchLoungesData();
        //console.log(temp);

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
  }, []);*/

  const handleTakeSeat = ({spaceName}) => {
    navigate({
      pathname: "/lounge",
      search: createSearchParams({placeName:spaceName}).toString()
    })
  };

  return (
    <div className="waiting-list-interface">
      {waitingLists.map((list, index) => (
        <WaitingCard key={index} spaceName={list.spaceName} info={list.info} onTakeSeat={()=>handleTakeSeat({spaceName:list.spaceName})} />
      ))}
      <Nav3/>
    </div>
  );
};

export default Lounges;
