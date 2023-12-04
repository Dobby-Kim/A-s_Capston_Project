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
    <div>
      {info.map((lounge) => (
        <Card key={lounge.key} sx={{ maxWidth: 400, height: 400, marginBottom: 10 }} className='card'>
          <CardActionArea>
            <CardMedia
              component="img"
              alt={lounge.name}
              image={img}
              sx={{ height: 200, objectFit: 'cover' }} // 이미지 크기와 스타일 설정
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
