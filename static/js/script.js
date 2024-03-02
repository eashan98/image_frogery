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

function forgeryDetection(detectionType) {
    const fileInput = document.getElementById('file_upload');
    const output_content = document.getElementById('output_content');
    const output_image = document.getElementById('output_image');
    const output_content_heading = document.getElementById('output_content_heading');
    const output_content_subheading = document.getElementById('output_content_subheading');
    const detection_button = document.getElementById(detectionType);
    var noLoadingImg = detection_button.querySelector('.icon > .no-loading');
    var loadingImg = detection_button.querySelector('.icon > .loading');
    const file = fileInput.files[0];

    var buttons = document.querySelectorAll('.detection-button');
    buttons.forEach(function(button){
        if(button.id != detectionType){
            button.classList.remove('active');
        }
    });
    detection_button.classList.add('active');
    noLoadingImg?.classList.add('d-none');
    loadingImg?.classList.remove('d-none');
    detection_button.disabled = true;

    if (!file) {
        alert('Please select an image file.');
        return;
    }

    const formData = new FormData();
    formData.append('image', file);

    // Send the file to the server
    fetch('/'+detectionType, {
        method: 'POST',
        body: formData,
    })
    .then(response => response.json())
    .then(data => {
        // Handle the response data
        console.log(data);
        detection_button.disabled = false;
        noLoadingImg?.classList.remove('d-none');
        loadingImg?.classList.add('d-none');
        if(data.status){
            output_content_heading.innerHTML = data.message;
            output_content_subheading.textContent = 'Image Processed Successfully';
            if(data.image){
                output_content.style.display = 'none';
                output_image.style.display = 'block';
                let preview_output_image = document.getElementById('preview_output_image');
                preview_output_image.src = data.image;
            }else{
                output_content.style.display = 'block';
                output_image.style.display = 'none';
            }
            return;
        }else{
            output_content_heading.textContent = 'Error: ' + data.message;
            output_content_subheading.textContent = 'Some Error Occurred';
            return;
        }
    })
    .catch(error => {
        console.error('Error:', error);
        alert(error)
    });
}