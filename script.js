function processFile() {
    const fileInput = document.getElementById('fileInput');
    if (fileInput.files.length > 0) {
        const reader = new FileReader();
        reader.onload = function(e) {
            const fileContent = e.target.result;
            // Here you would send fileContent to the server for processing
            // For demonstration, we'll just log it to the console
            console.log(fileContent);
            // Assume server returns HTML and display it
            document.getElementById('transcriptOutput').innerHTML = '<div class="transcript">Formatted transcript goes here...</div>';
        };
        reader.readAsText(fileInput.files[0]);
    } else {
        alert('Please select a file first.');
    }
}
