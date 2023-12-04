import React from 'react';
import Card from '@mui/material/Card';
import CardContent from '@mui/material/CardContent';
import CardMedia from '@mui/material/CardMedia';
import Typography from '@mui/material/Typography';
import { CardActionArea } from '@mui/material';
import info from '../data/info.json'; 
import img from "../img/psj.jpeg"
import "../style/info.css";

const LoungeCards = () => {
  return (
    <div>
      {info.map((lounge) => (
        <Card key={lounge.key} sx={{ maxWidth: 400, height: 400, marginBottom: 10 }}>
          <CardActionArea>
            <CardMedia
              component="img"
              alt="SKKU Image"
              image={img}
              className="skku-image"
              sx={{ height: 'auto' }} 
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
