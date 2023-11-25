import fs from "fs/promises";
import path from "path";
import { fileURLToPath } from "url";
import { dirname } from "path";

const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);
const PLACES_FILE = path.join(__dirname, "../places.json");

export const getPlaces = async () => {
  try {
    const data = await fs.readFile(PLACES_FILE, "utf-8");
    console.log(data);
    return data;
  } catch (error) {
    return [];
  }
};

export const getSeats = async (placeName) => {
  const places = await getPlaces();
  const seatInfo = places[0][placeName];
  console.log(seatInfo);
  return seatInfo;
};

export const saveUsers = async (users) => {
  await fs.writeFile(USERS_FILE, JSON.stringify(users, null, 2));
};
