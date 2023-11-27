import React, { useState, useEffect } from "react";
import { useMediaQuery } from 'react-responsive';
import placeData from "../data/places.json";
import "../style/lounge.css";
import { IoPersonOutline } from "react-icons/io5";
import { LuMapPin } from "react-icons/lu";
import { ReactComponent as SeatIcon } from '../img/seat.svg';

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

  const isDesktopOrLaptop = useMediaQuery({ minDeviceWidth: 1224 });
  const isTabletOrMobile = useMediaQuery({ maxWidth: 1224 });
  const isPortrait = useMediaQuery({ orientation: 'portrait' });

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
      [{ id: 'empty' },
       { id: 'empty' },
       { id: 'seat6', chairPosition: 'below' },
       { id: 'seat7', chairPosition: 'below' },
       { id: 'seat8', chairPosition: 'below' },
       { id: 'seat9', chairPosition: 'below' },
       { id: 'seat10', chairPosition: 'below' }],
      [{ id: 'seat5', chairPosition: 'right' },
       { id: 'empty' },
       { id: 'empty' },
       { id: 'empty' },
       { id: 'empty' },
       { id: 'empty' },
       { id: 'empty' }],
      [{ id: 'seat4', chairPosition: 'right' },
       { id: 'empty' },
       { id: 'empty' },
       { id: 'empty' },
       { id: 'empty' },
       { id: 'empty' },
       { id: 'empty' }],
       [{ id: 'seat3', chairPosition: 'right' },
       { id: 'empty' },
       { id: 'empty' },
       { id: 'seat12', chairPosition: 'up' },
       { id: 'seat14', chairPosition: 'up' },
       { id: 'seat16', chairPosition: 'up' },
       { id: 'seat18', chairPosition: 'up' }],
      [{ id: 'seat2', chairPosition: 'right' },
       { id: 'empty' },
       { id: 'empty' },
       { id: 'seat11', chairPosition: 'below' },
       { id: 'seat13', chairPosition: 'below' },
       { id: 'seat15', chairPosition: 'below' },
       { id: 'seat17', chairPosition: 'below' }],
      [{ id: 'seat1', chairPosition: 'right' },
       { id: 'empty' },
       { id: 'empty' },
       { id: 'empty' },
       { id: 'empty' },
       { id: 'empty' },
       { id: 'empty' }]
    ];

    return seatLayout.map((row, rowIndex) => (
      <div className="row" key={`row-${rowIndex}`} style={{ gap: '0.1rem' }}>
        {row.map((seat, seatIndex) => {
          if (seat.id === 'empty') {
            return <div className="seat-container empty" key={`empty-${rowIndex}-${seatIndex}`}></div>;
          }
  
          const seatStatus = seatInfo[seat.id];
          let seatClass = '';
          let iconClass = '';
  
          switch (seatStatus) {
            case 0: // empty
              seatClass = 'available';
              iconClass = 'available';
              break;
            case 1: // reserved
              seatClass = 'reserved';
              iconClass = 'reserved';
              break;
            case 2: // occupied
              seatClass = 'occupied';
              iconClass = 'occupied';
              break;
            default: // unknown
              seatClass = 'unknown';
              iconClass = 'unknown';
          }
  
          return (
            <div className={`seat-container ${seatClass} ${seat.chairPosition}`} key={`seat-${rowIndex}-${seatIndex}`}>
              <div className={`seat ${seatClass}`}>
                {seat.id.replace('seat', '')}
              </div>
              <SeatIcon className={`seat-icon ${iconClass}`} />
            </div>
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
    <div className={`wrapper ${isTabletOrMobile ? 'mobile' : 'desktop'} ${isPortrait ? 'portrait' : 'landscape'}`}>
      <Header available={available} reserved={reserved} occupied={occupied} />
      <StatusIndicator />
      <section className="card">
        {renderSeatRows()}
      </section>
    </div>
  );
};

export default Lounge;

// ReactDOM.createRoot(document.getElementById('root')).render(
//   <React.StrictMode>
//     <Lounge />
//   </React.StrictMode>
// );
