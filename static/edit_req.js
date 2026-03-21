// --- Elements ---
const body = document.querySelector("body");
const modeTogglerBtn = document.querySelector(".tdnn");
const modeTogglerMoon = document.querySelector(".moon");
const homeBtn = document.getElementById("homeBtn");
const formSubContainer = document.querySelector(".formbold-form-wrapper");
const deleteForm = document.getElementById('deleteRequestForm');

// --- 1. Initial Theme Load ---
if (localStorage.getItem('theme') === 'light') {
    body.classList.add('light');
    if (modeTogglerBtn) modeTogglerBtn.classList.add('day');
    if (modeTogglerMoon) modeTogglerMoon.classList.add('sun');
}

// --- 2. Theme Toggler (Shared Logic) ---
if (modeTogglerBtn) {
    modeTogglerBtn.addEventListener("click", () => {
        body.classList.toggle('light');
        modeTogglerBtn.classList.toggle('day');
        modeTogglerMoon.classList.toggle("sun");
        if (homeBtn) homeBtn.classList.toggle("light");
        if (formSubContainer) formSubContainer.classList.toggle("light");
        
        localStorage.setItem('theme', body.classList.contains('light') ? 'light' : 'dark');
    });
}

// --- 3. Delete Request Submission ---
if (deleteForm) {
    deleteForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        
        const submitBtn = document.getElementById('submitDelBtn');
        const originalText = submitBtn.textContent;
        
        // UI Feedback
        submitBtn.textContent = "Sending Request...";
        submitBtn.disabled = true;

        const payload = {
            sender: document.getElementById('senderName').value,
            imageName: document.getElementById('delImageName').value,
            reason: document.getElementById('reason').value
        };

        try {
            const response = await fetch('/api/delete_request', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(payload)
            });

            if (response.ok) {
                alert("Your request has been sent to the admin. We will process it shortly.");
                window.location.href = "/"; // Redirect home after success
            } else {
                throw new Error("Failed to send");
            }
        } catch (error) {
            alert("Oops! Something went wrong. Please try again later.");
            console.error("Mail Error:", error);
        } finally {
            submitBtn.textContent = originalText;
            submitBtn.disabled = false;
        }
    });
}