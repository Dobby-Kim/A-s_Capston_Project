import React, { useState, useEffect } from 'react';
import { createSearchParams, useNavigate } from "react-router-dom";
import Card from '@mui/material/Card';
import CardContent from '@mui/material/CardContent';
import CardMedia from '@mui/material/CardMedia';
import Typography from '@mui/material/Typography';
import { CardActionArea } from '@mui/material';
import info from '../data/info.json'; 
import "../style/info.css";



// ActionButton Component
const ActionButton = ({ spaceName, onTakeSeat }) => (
  <button className="take-seat-button-info" onClick={() => onTakeSeat(spaceName)}>
    Take a seat
  </button>
);  

const LoungeCards = () => {
  const navigate = useNavigate();
  const [selectedCard, setSelectedCard] = useState(null);

  useEffect(() => {
    window.dispatchEvent(new CustomEvent('navigationUpdate', { detail: '/info' }));
  }, []);

  const handleCardClick = (key) => {
    setSelectedCard(key === selectedCard ? null : key);
  };

  const handleTakeSeat = (spaceName) => {
    navigate({
      pathname: "/lounge",
      search: createSearchParams({ spaceName: spaceName }).toString()
    } );

    window.dispatchEvent(new CustomEvent('navigationUpdate', { detail: '/lounges' }));
  };

  return (
    <div className='img_container'>
      {info.map((lounge) => (
        <Card 
          key={lounge.key} 
          className='each_card'
          onClick={() => handleCardClick(lounge.key)}
        >
          <CardActionArea>
            <CardMedia
              className='card_img'
              component="img"
              alt={lounge.name}
              image={`/img/${lounge.img}`}
            />
            <CardContent>
              <Typography gutterBottom variant="h5" component="div" fontWeight= 'bold'>
                {lounge.name}
              </Typography>
              <Typography variant="body2" color="text.secondary" >
                {lounge.description1}
              </Typography>
              <div style={{ margin: "1rem 0" }}></div>
              <Typography variant="body2" color="green" >
                {lounge.description2}
              </Typography>
            </CardContent>
            
          </CardActionArea>
          {selectedCard === lounge.key && <div className="card-overlay">
          <ActionButton spaceName={lounge.key} onTakeSeat={handleTakeSeat} />
            </div>}
        </Card>
      ))}
    </div>
  );
};

export default LoungeCards;
