import express from "express";
import path from "path";
import cookieParser from "cookie-parser";
import authRoutes from "./routes/auth.js";
import dataRoutes from "./routes/data.js";
import { fileURLToPath } from "url";
import { dirname } from "path";

const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);
const app = express();

app.use(express.json());
app.use(express.static(path.join(__dirname, "view"))); //추가
app.use(authRoutes);
app.use(dataRoutes);

app.get("/", (req, res) => {
  res.sendFile(path.join(__dirname, "/view/seat_position.html"));
});

app.listen(3000, () => {
  console.log("Server started on http://localhost:3000");
});

export default app;
