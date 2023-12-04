import React, { useState } from 'react';
import Card from '@mui/material/Card';
import CardContent from '@mui/material/CardContent';
import CardMedia from '@mui/material/CardMedia';
import Typography from '@mui/material/Typography';
import { CardActionArea } from '@mui/material';
import info from '../data/info.json'; 
import "../style/info.css";

// const handleTakeSeat = ({ spaceName }) => {
//   navigate({
//     pathname: "/lounge",
//     search: createSearchParams({ spaceName: spaceName }).toString()
//   });
// };


// // ActionButton Component
// const ActionButton = ({ onTakeSeat, className }) => (
//     <button className={`take-seat-button ${className}`} onClick={onTakeSeat}>
//       Take a seat
//     </button>
//   );  

const LoungeCards = () => {
  const [selectedCard, setSelectedCard] = useState(null);

  const handleCardClick = (key) => {
    setSelectedCard(key === selectedCard ? null : key);
  };

  return (
    <div className='container'>
      {info.map((lounge) => (
        <Card 
          key={lounge.key} 
          sx={{ maxWidth: 400, height: 300, position: 'relative' }} 
          className='card'
          onClick={() => handleCardClick(lounge.key)}
        >
          <CardActionArea>
            <CardMedia
              component="img"
              alt={lounge.name}
              image={`/img/${lounge.img}`}
              sx={{ height: 200, objectFit: 'cover' }}
            />
            <CardContent>
              <Typography gutterBottom variant="h5" component="div">
                {lounge.name}
              </Typography>
              <Typography variant="body2" color="text.secondary">
                {lounge.description}
              </Typography>
            </CardContent>
            
          </CardActionArea>
          {selectedCard === lounge.key && <div className="card-overlay">
          {/* <ActionButton onTakeSeat={onTakeSeat} /> */}
            </div>}
        </Card>
      ))}
    </div>
  );
};

export default LoungeCards;
