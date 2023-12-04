import React from 'react';
import Card from '@mui/material/Card';
import CardContent from '@mui/material/CardContent';
import CardMedia from '@mui/material/CardMedia';
import Typography from '@mui/material/Typography';
import { CardActionArea } from '@mui/material';
import info from '../data/info.json'; 
import img from "../img/black.png";
import "../style/info.css";

const LoungeCards = () => {
  return (
    <div className='container'>
      {info.map((lounge) => (
        // 카드 height 300으로 고정
        <Card key={lounge.key} sx={{ maxWidth: 400, height: 300 }} className='card'> 
          <CardActionArea>
            <CardMedia
              component="img"
              alt={lounge.name}
              image={img}
              sx={{ height: 200, objectFit: 'cover' }} // 사진 크기 200으로 고정
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
        </Card>
      ))}
    </div>
  );
};

export default LoungeCards;
