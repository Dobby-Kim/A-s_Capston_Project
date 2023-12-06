import * as React from 'react';
import BottomNavigation from '@mui/material/BottomNavigation';
import BottomNavigationAction from '@mui/material/BottomNavigationAction';
import InfoIcon from '@mui/icons-material/Info';
import LocationOnIcon from '@mui/icons-material/LocationOn';
import { useNavigate } from 'react-router-dom';
import "../style/nav.css";

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
  );
};

export default LabelBottomNavigation;
