import React, { useState, useEffect } from "react";
import placeData from "../data/places.json";

import "../style/lounge.css";
import { IoPersonOutline } from "react-icons/io5";
import { LuMapPin } from "react-icons/lu";

const Header = ({ available, reserved, occupied }) => {
  const totalSeats = available + reserved + occupied;

  return (
    <header className="header">
      <h1>ParkSangJo</h1>
      <div className="header-info">
        <LuMapPin className="icon map" size="21" />
        <p className="num-text">Engineering Building 2, Floor 1</p>
      </div>
      <div className="header-info seat-status">
        <IoPersonOutline className="icon person" size="23" />
        <span className="num-text">{`${available}/${totalSeats} `}</span>
      </div>
    </header>
  );
};

const StatusIndicator = () => {
  return (
    <div className="status-indicator">
      <div className="status-item">
        <span className="status-dot available"></span>
        <span className="status-text">Available</span>
      </div>
      <div className="status-item">
        <span className="status-dot reserved"></span>
        <span className="status-text">Reserved</span>
      </div>
      <div className="status-item">
        <span className="status-dot occupied"></span>
        <span className="status-text">Occupied</span>
      </div>
    </div>
  );
};

const Lounge = () => {
  const [placeName, setPlaceName] = useState("");
  const [seatInfo, setSeatInfo] = useState({});

  const load = async (placeName) => {
    try {
      const response = await fetch(
        `/seat?placeName=${encodeURIComponent(placeName)}`
      );
      const data = await response.json();
      setSeatInfo(data);
    } catch (error) {
      console.error(error);
      alert(`⚠️ 서버에서 데이터를 가져올 수 없어요! ⚠️\n${error.message}`);
    }
  };

  const searchPlace = async (event) => {
    event.preventDefault();
    await load(placeName);
  };

  // JSON 파일에서 데이터 로드
  useEffect(() => {
    const loungeSeats = placeData[0]["parksangjo"];
    setSeatInfo(loungeSeats);
  }, []);

  const renderSeatRows = () => {
    const seatLayout = [
      ["seat1", "seat2", "seat3", "seat4", "seat5", "empty"],
      ["empty", "empty", "empty", "empty", "empty", "seat6"],
      ["empty", "empty", "seat11", "seat12", "empty", "seat7"],
      ["empty", "empty", "seat13", "seat14", "empty", "seat8"],
      ["empty", "empty", "seat15", "seat16", "empty", "seat9"],
      ["empty", "empty", "seat17", "seat18", "empty", "seat10"],
    ];

    // 각 좌석 및 빈 자리를 렌더링하는 로직
    return seatLayout.map((row, rowIndex) => (
      <div className="row" key={`row-${rowIndex}`}>
        {row.map((seat, seatIndex) => {
          const seatNumber = seat.replace("seat", "");
          const seatStatus = seatInfo[seat];
          let seatClass = "";

          switch (seatStatus) {
            case 0: // empty
              seatClass = "available";
              break;
            case 1: // reserved
              seatClass = "reserved";
              break;
            case 2: // occupied
              seatClass = "occupied";
              break;
            default: // unknown
              seatClass = "unknown";
          }

          return seat !== "empty" ? (
            <div className={`seat ${seatClass}`} key={seat}>
              {seatNumber}
            </div>
          ) : (
            <div className="empty" key={`empty-${rowIndex}-${seatIndex}`}></div>
          );
        })}
      </div>
    ));
  };

  // 좌석 상태에 따른 카운트 계산
  const available = Object.values(seatInfo).filter(
    (status) => status === 0
  ).length;
  const reserved = Object.values(seatInfo).filter(
    (status) => status === 1
  ).length;
  const occupied = Object.values(seatInfo).filter(
    (status) => status === 2
  ).length;

  return (
    <div className="wrapper">
      <Header available={available} reserved={reserved} occupied={occupied} />
      <StatusIndicator />
      {/* <h1 className="title">박상조 라운지</h1> */}
      {/* <h2 className="title">현재 시각</h2> */}
      <section className="card">{renderSeatRows()}</section>
    </div>
  );
};

export default Lounge;

// ReactDOM.createRoot(document.getElementById('root')).render(
//   <React.StrictMode>
//     <Lounge />
//   </React.StrictMode>
// );
