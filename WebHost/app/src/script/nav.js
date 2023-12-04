import * as React from 'react';
import BottomNavigation from '@mui/material/BottomNavigation';
import BottomNavigationAction from '@mui/material/BottomNavigationAction';
import InfoIcon from '@mui/icons-material/Info';
import LocationOnIcon from '@mui/icons-material/LocationOn';
import "../style/nav.css"

const LabelBottomNavigation = () => {
  const [value, setValue] = React.useState('recents');

  const handleChange = (event, newValue) => {
    setValue(newValue);
  };

  return (
    <div className='navigation'>
        <BottomNavigation sx={{ width: 500 }} value={value} onChange={handleChange}>

        <BottomNavigationAction
            label="Spaces"
            value="Spaces"
            icon={<LocationOnIcon />}
        />
        
        <BottomNavigationAction
            label="Description"
            value="Description"
            icon={<InfoIcon />}
        />
        
        </BottomNavigation>
    </div>
  );
}

export default LabelBottomNavigation;