// Women Thoughts System - Main JS

// SOS Modal Toggle
function toggleSOSModal() {
    const modal = document.getElementById('sos-modal');
    modal.style.display = (modal.style.display === 'block') ? 'none' : 'block';
    
    if (modal.style.display === 'block') {
        startBreathingAnimation();
    }
}

// Breathing Animation text cycle
function startBreathingAnimation() {
    const textEl = document.querySelector('.breathing-text');
    if (!textEl) return;
    
    let state = 0;
    const states = ["Breathe in...", "Hold...", "Breathe out...", "Rest..."];
    
    setInterval(() => {
        state = (state + 1) % states.length;
        textEl.innerText = states[state];
    }, 2000);
}

// SOS Submit
async function submitSOS(event) {
    event.preventDefault();
    const form = event.target;
    const formData = new FormData(form);
    
    try {
        const response = await fetch('/sos', {
            method: 'POST',
            body: formData
        });
        const data = await response.json();
        
        if (data.success) {
            alert('Your SOS request has been sent. Help is on the way. 💜');
            toggleSOSModal();
        }
    } catch (error) {
        console.error('SOS Error:', error);
    }
}

// Like Post
async function likePost(postId, btn) {
    try {
        const response = await fetch(`/post/${postId}/like`, {
            method: 'POST',
            headers: {
                'X-CSRFToken': document.querySelector('input[name="csrf_token"]').value
            }
        });
        const data = await response.json();
        
        if (data.success) {
            const countSpan = btn.querySelector('.like-count');
            countSpan.innerText = data.count;
            btn.querySelector('i').className = 'fas fa-heart';
            btn.style.color = '#E91E8C';
        }
    } catch (error) {
        console.error('Like Error:', error);
    }
}

// Report Post
async function reportPost(postId, btn) {
    const reason = prompt("Please provide a reason for reporting this post:");
    if (!reason) return;

    try {
        const response = await fetch(`/post/${postId}/report`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': document.querySelector('input[name="csrf_token"]').value
            },
            body: JSON.stringify({ reason: reason })
        });
        const data = await response.json();
        
        if (data.success) {
            alert(data.message);
            btn.style.color = '#ff4757';
            btn.disabled = true;
        } else {
            alert(data.message);
        }
    } catch (error) {
        console.error('Report Error:', error);
    }
}

// Comments
function toggleComments(postId) {
    const section = document.getElementById(`comments-${postId}`);
    section.style.display = (section.style.display === 'none') ? 'block' : 'none';
}

async function submitComment(event, postId) {
    event.preventDefault();
    const form = event.target;
    const formData = new FormData(form);
    
    try {
        const response = await fetch(`/post/${postId}/comment`, {
            method: 'POST',
            headers: {
                'X-CSRFToken': document.querySelector('input[name="csrf_token"]').value
            },
            body: formData
        });
        const data = await response.json();
        
        if (data.success) {
            // Append new comment to UI
            const list = form.previousElementSibling;
            const item = document.createElement('div');
            item.className = 'comment-item';
            item.innerHTML = `
                <strong>${data.comment.username}</strong>
                <p>${data.comment.body}</p>
                <small>${data.comment.created_at}</small>
            `;
            list.appendChild(item);
            form.reset();
            
            // Update count
            const card = document.getElementById(`comments-${postId}`).parentElement;
            const countSpan = card.querySelector('.comment-count');
            countSpan.innerText = parseInt(countSpan.innerText) + 1;
        }
    } catch (error) {
        console.error('Comment Error:', error);
    }
}

// Close modal when clicking outside
window.onclick = function(event) {
    const modal = document.getElementById('sos-modal');
    if (event.target == modal) {
        toggleSOSModal();
    }
}
