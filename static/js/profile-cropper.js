class ProfileCropper {
    constructor() {
        this.cropper = null;
        this.elements = {
            imageInput: document.getElementById('imageInput'),
            cropperContainer: document.getElementById('cropperContainer'),
            cropperImage: document.getElementById('cropperImage'),
            cropButton: document.getElementById('cropButton'),
            previewImage: document.getElementById('previewImage'),
            profileForm: document.getElementById('profileForm')
        };
        this.init();
    }

    init() {
        if (this.elements.imageInput) {
            this.elements.imageInput.addEventListener('change', this.handleImageSelect.bind(this));
        }
        if (this.elements.cropButton) {
            this.elements.cropButton.addEventListener('click', this.handleCrop.bind(this));
        }
        if (this.elements.profileForm) {
            this.elements.profileForm.addEventListener('submit', this.handleSubmit.bind(this));
        }
    }

    handleImageSelect(e) {
        const file = e.target.files[0];
        if (file) {
            const reader = new FileReader();
            reader.onload = (e) => this.initCropper(e.target.result);
            reader.readAsDataURL(file);
        }
    }

    initCropper(imageUrl) {
        if (this.cropper) {
            this.cropper.destroy();
        }

        this.elements.cropperImage.src = imageUrl;
        this.elements.cropperContainer.style.display = 'block';
        
        this.cropper = new Cropper(this.elements.cropperImage, {
            aspectRatio: 1,
            viewMode: 2,
            autoCropArea: 1,
            cropBoxResizable: true
        });
    }

    handleCrop() {
        if (!this.cropper) return;

        const canvas = this.cropper.getCroppedCanvas({
            width: 300,
            height: 300
        });

        // Update preview image
        this.elements.previewImage.src = canvas.toDataURL();
        this.elements.previewImage.style.display = 'block';

        // Convert canvas to blob for form submission
        canvas.toBlob((blob) => {
            const formData = new FormData();
            formData.append('profile_picture', blob, 'profile.jpg');
            
            // Store the blob for form submission
            this.croppedBlob = blob;
        }, 'image/jpeg', 0.9);
    }

    handleSubmit(e) {
        e.preventDefault();

        if (this.croppedBlob) {
            const formData = new FormData(this.elements.profileForm);
            
            // Add cropped image with unique filename
            const timestamp = new Date().getTime();
            const filename = `profile_${timestamp}.jpg`;
            formData.set('profile_picture', this.croppedBlob, filename);

            // Add indicator for Vercel environment
            if (window.VERCEL_ENV) {
                formData.append('is_vercel', 'true');
            }

            fetch(this.elements.profileForm.action, {
                method: 'POST',
                body: formData,
                headers: { 
                    'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value,
                    'X-Requested-With': 'XMLHttpRequest'
                }
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    // Update preview with new Blob URL or local URL
                    this.elements.previewImage.src = data.image_url;
                    messages.success('Profile picture updated successfully!');
                    window.location.reload();
                } else {
                    messages.error(data.error || 'Failed to update profile picture.');
                }
            })
            .catch(error => {
                console.error('Error:', error);
                messages.error('An error occurred while updating profile picture.');
            });
        } else {
            this.elements.profileForm.submit();
        }
    }
}

// Initialize when DOM is loaded
document.addEventListener('DOMContentLoaded', () => new ProfileCropper());