function handleImageUpload() {
    var input = document.getElementById('file_upload');
    var uploadImage = document.getElementById('upload_image');
    var uploadedImage = document.getElementById('uploaded_image');
    var previewImage = document.getElementById('preview_image');
    var fileNameElement = document.getElementById('file_name');

    if (input.files && input.files[0]) {
        var reader = new FileReader();

        reader.onload = function (e) {
            previewImage.src = e.target.result;
            uploadImage.style.display = 'none';
            uploadedImage.style.display = 'block';
        };

        reader.readAsDataURL(input.files[0]);

        fileNameElement.textContent = 'File Selected: ' + input.files[0].name;
    }else{
        previewImage.src = '';
        uploadImage.style.display = 'block';
        uploadedImage.style.display = 'none';
        fileNameElement.textContent = 'Upload image to check forgery';
    }
}

function processCompressDetection() {
    const fileInput = document.getElementById('file_upload');
    const file = fileInput.files[0];

    if (!file) {
        alert('Please select an image file.');
        return;
    }

    const formData = new FormData();
    formData.append('image', file);

    // Send the file to the server
    fetch('/processCompressDetection', {
        method: 'POST',
        body: formData,
    })
    .then(response => response.json())
    .then(data => {
        // Handle the response data
        console.log(data);
    })
    .catch(error => console.error('Error:', error));
}