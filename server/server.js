import express from "express";
import dataRoutes from "./routes/data.js";

const app = express();

app.use(express.json());
app.use("/data", dataRoutes);

app.listen(3000, () => {
  console.log("Server started on http://localhost:3000");
});

export default app;
