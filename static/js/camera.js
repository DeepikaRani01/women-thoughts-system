// Women Thoughts System - Camera Logic

const video = document.getElementById('video');
const canvas = document.getElementById('canvas');
const snapBtn = document.getElementById('snap');
const startBtn = document.getElementById('start-camera');
const statusDiv = document.getElementById('verification-status');
const overlay = document.getElementById('camera-overlay');
const isVerifiedField = document.getElementById('is_verified');

let stream = null;

// Start Camera
startBtn.addEventListener('click', async () => {
    try {
        stream = await navigator.mediaDevices.getUserMedia({ video: true, audio: false });
        video.srcObject = stream;
        startBtn.style.display = 'none';
        snapBtn.style.display = 'inline-block';
        overlay.style.display = 'none';
    } catch (err) {
        console.error("Camera Error:", err);
        statusDiv.innerHTML = '<span class="text-danger">Error: Could not access camera.</span>';
    }
});

// Capture and Verify
snapBtn.addEventListener('click', async () => {
    statusDiv.innerHTML = '<div class="spinner"></div> Verifying...';
    snapBtn.disabled = true;

    // Draw to canvas
    const context = canvas.getContext('2d');
    canvas.width = video.videoWidth;
    canvas.height = video.videoHeight;
    context.drawImage(video, 0, 0, canvas.width, canvas.height);
    
    const imageData = canvas.toDataURL('image/jpeg');

    try {
        const response = await fetch('/api/verify-gender', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': document.querySelector('input[name="csrf_token"]').value
            },
            body: JSON.stringify({ image: imageData })
        });
        
        const data = await response.json();
        
        if (data.verified) {
            statusDiv.innerHTML = `<span style="color: green;">${data.message}</span>`;
            isVerifiedField.value = 'true';
            stopCamera();
        } else {
            statusDiv.innerHTML = `<span style="color: red;">${data.message}</span>`;
            snapBtn.disabled = false;
        }
    } catch (err) {
        statusDiv.innerHTML = '<span style="color: red;">Verification failed. Please try again.</span>';
        snapBtn.disabled = false;
    }
});

function stopCamera() {
    if (stream) {
        stream.getTracks().forEach(track => track.stop());
    }
    video.style.display = 'none';
    snapBtn.style.display = 'none';
}
