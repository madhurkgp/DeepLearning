document.addEventListener('DOMContentLoaded', function() {
    const sourceInput = document.getElementById('source_image');
    const destinationInput = document.getElementById('destination_image');
    const sourceName = document.getElementById('source_name');
    const destinationName = document.getElementById('destination_name');
    const form = document.querySelector('form');
    const submitBtn = document.getElementById('submit');
    const loading = document.querySelector('.loading');
    const errorMessage = document.querySelector('.error-message');
    const successMessage = document.querySelector('.success-message');

    // File input handlers
    sourceInput.addEventListener('change', function() {
        const fileName = this.files[0] ? this.files[0].name : '';
        sourceName.textContent = fileName || 'No file selected';
        previewImage(this, 'source-preview');
    });

    destinationInput.addEventListener('change', function() {
        const fileName = this.files[0] ? this.files[0].name : '';
        destinationName.textContent = fileName || 'No file selected';
        previewImage(this, 'destination-preview');
    });

    // Image preview function
    function previewImage(input, previewId) {
        const preview = document.getElementById(previewId);
        if (input.files && input.files[0]) {
            const reader = new FileReader();
            reader.onload = function(e) {
                preview.src = e.target.result;
            };
            reader.readAsDataURL(input.files[0]);
        }
    }

    // Form submission handler
    form.addEventListener('submit', function(e) {
        e.preventDefault();
        
        // Validate that both images are selected
        if (!sourceInput.files[0] || !destinationInput.files[0]) {
            showError('Please select both source and destination images');
            return;
        }

        // Show loading state
        showLoading();
        hideMessages();

        // Create FormData
        const formData = new FormData(form);
        
        // Submit via fetch
        fetch('/', {
            method: 'POST',
            body: formData
        })
        .then(response => response.text())
        .then(html => {
            // Parse the response and update the result image
            const parser = new DOMParser();
            const doc = parser.parseFromString(html, 'text/html');
            const resultImg = doc.querySelector('#result-preview');
            if (resultImg) {
                document.getElementById('result-preview').src = resultImg.src;
                showSuccess('Face swap completed successfully!');
                
                // Show download button
                const downloadBtn = document.querySelector('.download-btn');
                if (downloadBtn) {
                    downloadBtn.style.display = 'inline-block';
                    downloadBtn.href = resultImg.src;
                    downloadBtn.download = 'face-swap-result.png';
                }
            }
        })
        .catch(error => {
            showError('An error occurred during face swap. Please try again.');
            console.error('Error:', error);
        })
        .finally(() => {
            hideLoading();
        });
    });

    function showLoading() {
        loading.style.display = 'block';
        submitBtn.disabled = true;
        submitBtn.textContent = 'Processing...';
    }

    function hideLoading() {
        loading.style.display = 'none';
        submitBtn.disabled = false;
        submitBtn.textContent = 'Swap Faces';
    }

    function showError(message) {
        errorMessage.textContent = message;
        errorMessage.style.display = 'block';
        setTimeout(() => {
            errorMessage.style.display = 'none';
        }, 5000);
    }

    function showSuccess(message) {
        successMessage.textContent = message;
        successMessage.style.display = 'block';
        setTimeout(() => {
            successMessage.style.display = 'none';
        }, 3000);
    }

    function hideMessages() {
        errorMessage.style.display = 'none';
        successMessage.style.display = 'none';
    }

    // Drag and drop functionality
    const uploadBoxes = document.querySelectorAll('.upload-box');
    
    uploadBoxes.forEach(box => {
        const imagePreview = box.querySelector('.image-preview');
        const fileInput = box.querySelector('input[type="file"]');
        
        ['dragenter', 'dragover', 'dragleave', 'drop'].forEach(eventName => {
            imagePreview.addEventListener(eventName, preventDefaults, false);
        });
        
        function preventDefaults(e) {
            e.preventDefault();
            e.stopPropagation();
        }
        
        ['dragenter', 'dragover'].forEach(eventName => {
            imagePreview.addEventListener(eventName, () => {
                imagePreview.classList.add('drag-over');
            }, false);
        });
        
        ['dragleave', 'drop'].forEach(eventName => {
            imagePreview.addEventListener(eventName, () => {
                imagePreview.classList.remove('drag-over');
            }, false);
        });
        
        imagePreview.addEventListener('drop', function(e) {
            const files = e.dataTransfer.files;
            if (files.length > 0) {
                fileInput.files = files;
                const event = new Event('change', { bubbles: true });
                fileInput.dispatchEvent(event);
            }
        }, false);
    });
});
