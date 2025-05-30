const express = require("express");
const multer = require("multer");
const path = require("path");
const axios = require("axios");

const app = express();
const upload = multer({ dest: "uploads/" });

app.use(express.static("public"));

app.post("/upload", upload.single("file"), async (req, res) => {
    try {
        let filePath = req.file.path;

        let response = await axios.post("http://127.0.0.1:5000/detect", {
            file_path: filePath,
        });

        res.json(response.data);
    } catch (error) {
        console.error("Error:", error);
        res.status(500).json({ error: "Failed to process image" });
    }
});

app.listen(3000, () => {
    console.log("Server running on http://localhost:3000");
});
