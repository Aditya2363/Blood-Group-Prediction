document.getElementById("uploadForm").addEventListener("submit", async function(event) {
    event.preventDefault();

    let fileInput = document.getElementById("fileInput").files[0];
    if (!fileInput) {
        alert("Please select an image file.");
        return;
    }

    let formData = new FormData();
    formData.append("file", fileInput);

    try {
        let response = await fetch("http://localhost:5000/detect", {
            method: "POST",
            body: formData
        });

        let data = await response.json();
        document.getElementById("result").innerHTML = `<h4>Predicted Blood Group: ${data.blood_group}</h4>`;
    } catch (error) {
        console.error("Error:", error);
        document.getElementById("result").innerHTML = `<h4 style="color:red;">Error processing request</h4>`;
    }
});
