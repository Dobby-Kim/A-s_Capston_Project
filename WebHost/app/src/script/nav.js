import * as React from 'react';
import BottomNavigation from '@mui/material/BottomNavigation';
import BottomNavigationAction from '@mui/material/BottomNavigationAction';
import InfoIcon from '@mui/icons-material/Info';
import LocationOnIcon from '@mui/icons-material/LocationOn';
import { useNavigate } from 'react-router-dom';
import "../style/nav.css";
import title_image from "../img/Empty Seats.png";
import team_image from "../img/team A’s.png";
import skku_image from "../img/chair.png";

const LabelBottomNavigation = () => {
  const navigate = useNavigate();

  const [value, setValue] = React.useState('/lounges');

  // 네비게이션 상태를 업데이트하는 함수
  const handleChange = (event, newValue) => {
    setValue(newValue);
    navigate(newValue);
  };

  // 외부 이벤트를 사용하여 네비게이션 상태를 업데이트하는 useEffect
  React.useEffect(() => {
    const handleNavigationUpdate = (e) => {
      setValue(e.detail);
    };

    window.addEventListener('navigationUpdate', handleNavigationUpdate);

    return () => {
      window.removeEventListener('navigationUpdate', handleNavigationUpdate);
    };
  }, []);

  const selectedStyle = {
    color: 'rgba(0, 0, 0, 0.54)', 
    '&.Mui-selected': {
      color: 'green',
    },
  };

  return (
    <div className='navigation-wrapper'>
      {/* <img src={skku_image} alt="Left" className="nav-image-left" /> */}
      <div className='navigation'>
        <BottomNavigation sx={{ width: 500 }} value={value} onChange={handleChange}>
          {[
            { label: 'Spaces', value: '/lounges', icon: <LocationOnIcon /> },
            { label: 'Description', value: '/info', icon: <InfoIcon /> },
          ].map((navItem) => (
            <BottomNavigationAction
              key={navItem.value}
              label={navItem.label}
              value={navItem.value}
              icon={navItem.icon}
              sx={selectedStyle}
              showLabel={value === navItem.value}
            />
          ))}
        </BottomNavigation>
    </div>
      {/* <img src={skku_image} alt="Right" className="nav-image-right" /> */}
    </div>
  );
};

export default LabelBottomNavigation;
