const express = require("express");
const path = require("path");
const app = express();
const PORT = process.env.PORT || 3001;


app.use(express.json());
app.use(express.urlencoded({ extended: true }));
app.use(express.static(path.join(__dirname, "public")));

app.get("/", (req, res) => {
  res.sendFile("index.html");
});

app.post("/api", (req, res) => {
    console.log(req.body);
})

app.listen(PORT, () => {
  console.log(`Listening on http://localhost:${PORT}`);
});
