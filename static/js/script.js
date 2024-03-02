function handleImageUpload() {
    var input = document.getElementById('file_upload');
    var uploadImage = document.getElementById('upload_image');
    var uploadedImage = document.getElementById('uploaded_image');
    var previewImage = document.getElementById('preview_image');
    var fileNameElement = document.getElementById('file_name');

    const output_content = document.getElementById('output_content');
    const output_image = document.getElementById('output_image');
    const output_title = document.getElementById('output_title');
    const output_content_heading = document.getElementById('output_content_heading');
    const output_content_subheading = document.getElementById('output_content_subheading');
    const preview_output_image = document.getElementById('preview_output_image');

    const buttons = document.querySelectorAll('.detection-button');
    buttons.forEach(function(button){
        button.classList.remove('active');
        const noLoadingImg = button.querySelector('.icon > .no-loading');
        const loadingImg = button.querySelector('.icon > .loading');
        noLoadingImg?.classList.remove('d-none');
        loadingImg?.classList.add('d-none');
    });

    output_content.style.display = 'block';
    output_image.style.display = 'none';
    output_image.classList.remove('w-full');
    preview_output_image.src = '';
    output_title.textContent = 'Output';
    output_content_heading.textContent = 'Output will be shown here!';
    output_content_subheading.textContent = 'Please select any option to see output';
    output_title.classList.remove('text-success');
    output_title.classList.remove('text-info');
    output_title.classList.remove('text-danger');


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
    const output_title = document.getElementById('output_title');
    const output_content_heading = document.getElementById('output_content_heading');
    const output_content_subheading = document.getElementById('output_content_subheading');
    const detection_button = document.getElementById(detectionType);
    const preview_output_image = document.getElementById('preview_output_image');
    const noLoadingImg = detection_button.querySelector('.icon > .no-loading');
    const loadingImg = detection_button.querySelector('.icon > .loading');
    const file = fileInput.files[0];
    
    const buttons = document.querySelectorAll('.detection-button');
    buttons.forEach(function(button){
        if(button.id != detectionType){
            button.classList.remove('active');
        }
    });

    detection_button.classList.add('active');
    noLoadingImg?.classList.add('d-none');
    loadingImg?.classList.remove('d-none');
    detection_button.disabled = true;
    output_content.style.display = 'none';
    output_image.style.display = 'block';
    output_image.classList.add('w-full');
    preview_output_image.src = 'static/images/gif/loading-200.gif';
    preview_output_image.style.display = 'block';
    output_title.classList.remove('text-success');
    output_title.classList.remove('text-info');
    output_title.classList.remove('text-danger');
    output_title.classList.add('text-info');
    output_title.textContent = 'Processing Image...';

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
        output_title.classList.remove('text-success');
        output_title.classList.remove('text-info');
        output_title.classList.remove('text-danger');
        if(data.status){
            output_content_heading.innerHTML = data.data;
            output_content_subheading.textContent = 'Image Processed Successfully';
            if(data.image){
                output_title.classList.add(data.type == 'success' ? 'text-success' : (data.type == 'info' ? 'text-info' : 'text-danger'));
                output_title.textContent = data.message;
                output_content.style.display = 'none';
                output_image.style.display = 'block';
                output_image.classList.add('w-full');
                preview_output_image.src = data.image;
                preview_output_image.style.display = 'block';
            }else{
                output_title.classList.add(data.type == 'success' ? 'text-success' : (data.type == 'info' ? 'text-info' : 'text-danger'));
                output_title.textContent = data.message;
                output_content.style.display = 'block';
                output_image.style.display = 'none';
                output_image.classList.remove('w-full');
            }
            return;
        }else{
            output_title.classList.add(data.type == 'success' ? 'text-success' : (data.type == 'info' ? 'text-info' : 'text-danger'));
            output_title.textContent = 'Error: ' + data.message;
            output_content.style.display = 'block';
            output_image.style.display = 'none';
            output_image.classList.remove('w-full');
            output_content_heading.textContent = 'Error: ' + data.data;
            output_content_subheading.textContent = 'Some Error Occurred';
            return;
        }
    })
    .catch(error => {
        console.error('Error:', error);
        output_title.classList.remove('text-success');
        output_title.classList.remove('text-info');
        output_title.classList.remove('text-danger');
        output_title.classList.add('text-danger');
        output_title.textContent = 'Error : Exception Occurred';
        output_content.style.display = 'block';
        output_image.style.display = 'none';
        output_image.classList.remove('w-full');
        detection_button.disabled = false;
        noLoadingImg?.classList.remove('d-none');
        loadingImg?.classList.add('d-none');
        output_content_heading.textContent = 'Error: ' + error;
        output_content_subheading.textContent = 'Some Error Occurred';
        alert(error)
    });
}