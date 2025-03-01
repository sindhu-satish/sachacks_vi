const express = require("express");
const cors = require("cors");
const bodyParser = require("body-parser");

const app = express();
app.use(cors());
app.use(bodyParser.json());

app.post("/api/generate", (req, res) => {
  const { prompt } = req.body;

  if (!prompt) {
    return res.status(400).json({ error: "Prompt is required" });
  }

  // Simulated API response
  const response = `Generated response for: "${prompt}"`;

  res.json({ response });
});

const PORT = 7777;
app.listen(PORT, () => console.log(`Server running on http://localhost:${PORT}`));
