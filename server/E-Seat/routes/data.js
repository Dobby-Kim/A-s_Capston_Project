import express from "express";
import os from "os";
import { getSeats } from "../utils/fileUtils.js";

const router = express.Router();

//! OS 정보 얻기
router.get("/seat", async (req, res) => {
  const { placeName } = req.query;
  const seatInfo = await getSeats(placeName)
  res.json(seatInfo);
});

export default router;
