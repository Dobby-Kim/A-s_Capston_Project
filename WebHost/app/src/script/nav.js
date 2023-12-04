import * as React from 'react';
import BottomNavigation from '@mui/material/BottomNavigation';
import BottomNavigationAction from '@mui/material/BottomNavigationAction';
import FavoriteIcon from '@mui/icons-material/Favorite';
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
            label="Nearby"
            value="nearby"
            icon={<LocationOnIcon />}
        />
        
        <BottomNavigationAction
            label="Favorites"
            value="favorites"
            icon={<FavoriteIcon />}
        />
        
        </BottomNavigation>
    </div>
  );
}

export default LabelBottomNavigation;