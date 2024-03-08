document.getElementById('upload-form').onsubmit = function(event) {
    event.preventDefault();
    let fileInput = document.getElementById('srtFile');
    let file = fileInput.files[0];
    let formData = new FormData();
    formData.append('srtFile', file);

    fetch('/upload', {
        method: 'POST',
        body: formData,
    })
    .then(response => response.json())
    .then(data => {
        document.getElementById('result').textContent = data.story;
    })
    .catch(error => {
        console.error('Error:', error);
    });
};
