import dotenv from "dotenv";
import express from "express";
import sql from "mssql";
import { getSeats } from "../util/fileUtil.js";
dotenv.config();

const router = express.Router();

const dbConfig = {
  user: process.env.USER,
  password: process.env.PASSWORD,
  server: process.env.SERVER,
  database: process.env.DATABASE,
  options: {
    encrypt: true,
    trustServerCertificate: true, // 개발 환경에서만 사용
  },
};

//! 상세 좌석 정보 얻기
//* page depth 2에서 사용하는 API
router.get("/getSeats", async (req, res) => {
  try {
    // 데이터베이스에 연결
    await sql.connect(dbConfig);

    const { spaceName } = req.query;
    const query = `
          SELECT seatID, seatState 
          FROM SeatDataTable 
          WHERE name = '${spaceName}'`;

    // 쿼리 실행
    const result = await sql.query(query);

    // seatID에서 spaceID 부분 제거 및 응답 데이터 생성
    // return format {좌석 번호: 0,1,2로 나타낸 좌석 상태}
    const seatStates = result.recordset.reduce((acc, record) => {
      acc[record.seatID % 100] = record.seatState;
      return acc;
    }, {});

    // 결과를 JSON으로 res 날리기
    res.json(seatStates);
  } catch (err) {
    console.error(err);
    res.status(500).send("Server Error");
  } finally {
    // 연결 종료
    sql.close();
  }
});

//! 간략한 공간 현황 및 정보
//* page depth 1에서 사용하는 API
router.get("/getSpace", async (req, res) => {
  try {
    // 데이터베이스에 연결
    await sql.connect(dbConfig);

    //쿼리 생성
    const { spaceName } = req.query;
    const query = `
          SELECT name, address, available_seat, total_seat 
          FROM SpaceTable 
          `;

    // 쿼리 실행
    const result = await sql.query(query);

    //database에서 가져온 정보를 address, available, total로 가공
    //return format {address: str, available: int, total: int}
    const spaceInfo = result.recordset.map((record) => {
      return {
        name: record.name,
        address: record.address,
        available: record.available_seat,
        total: record.total_seat,
      };
    });

    console.log(spaceInfo);

    // 결과를 JSON으로 res 날리기
    res.json(spaceInfo);
  } catch (err) {
    console.error(err);
    res.status(500).send("Server Error");
  } finally {
    // 연결 종료
    sql.close();
  }
});

router.get("/", (req, res) => {
  res.send("Router for Space & Seat Data");
});

export default router;
