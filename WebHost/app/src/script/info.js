import React from 'react';
import Card from '@mui/material/Card';
import CardContent from '@mui/material/CardContent';
import CardMedia from '@mui/material/CardMedia';
import Typography from '@mui/material/Typography';
import { CardActionArea } from '@mui/material';
import info from '../data/info.json'; // info.json 파일을 올바른 경로로 import

const LoungeCards = () => {
  return (
    <div>
      {info.map((lounge) => (
        <Card key={lounge.key} sx={{ maxWidth: 345, marginBottom: 2 }}>
          <CardActionArea>
            <CardMedia
              component="img"
              height="140"
              // 예시 이미지 경로를 사용하거나, lounge 객체에 이미지 경로를 추가할 수 있습니다.
              image="/static/images/cards/contemplative-reptile.jpg"
              alt={lounge.name}
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
