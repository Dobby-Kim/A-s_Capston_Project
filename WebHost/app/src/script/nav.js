import * as React from 'react';
import BottomNavigation from '@mui/material/BottomNavigation';
import BottomNavigationAction from '@mui/material/BottomNavigationAction';
import InfoIcon from '@mui/icons-material/Info';
import LocationOnIcon from '@mui/icons-material/LocationOn';
import { useNavigate } from 'react-router-dom';
import "../style/nav.css"

const LabelBottomNavigation = () => {
  const navigate = useNavigate();

  const [value, setValue] = React.useState('/lounges');

  const handleChange = (event, newValue) => {
    setValue(newValue);
    navigate(newValue);
  };

  return (
    <div className='navigation'>
        <BottomNavigation sx={{ width: 500 }} value={value} onChange={handleChange}>
          {[
            { label: 'Spaces', value: '/lounges', icon: <LocationOnIcon /> },
            { label: 'Description', value: '/info', icon: <InfoIcon /> },
            // Add more items as needed
          ].map((navItem) => (
            <BottomNavigationAction
              key={navItem.value}
              label={navItem.label}
              value={navItem.value}
              icon={navItem.icon}
              showLabel={value === navItem.value}
            />
          ))}
        </BottomNavigation>
    </div>
  );
}

export default LabelBottomNavigation;