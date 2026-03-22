// --- Elements ---
const body = document.querySelector("body");
const modeTogglerBtn = document.querySelector(".tdnn");
const modeTogglerMoon = document.querySelector(".moon");
const homeBtn = document.getElementById("homeBtn");
const deleteForm = document.getElementById('deleteRequestForm'); 
const svgContainer = document.querySelector(".svgContainer")
// load animation 
lottie.loadAnimation(

{ container: svgContainer,

renderer: 'svg',

loop: true,

autoplay: true,

  path: '/static/Cat_playing_animation.json'}
)




if (modeTogglerBtn) {
    modeTogglerBtn.addEventListener("click", () => {
        const isLight = body.classList.toggle('light');
        modeTogglerBtn.classList.toggle('day');
        modeTogglerMoon.classList.toggle("sun");
        
        if (homeBtn) homeBtn.classList.toggle("light");
        
        // Toggle classes on the form
        if (deleteForm) {
            deleteForm.classList.toggle("light");
            deleteForm.classList.toggle("formLight");
        }

        localStorage.setItem('theme', isLight ? 'light' : 'dark');
    });
}


if (deleteForm) {
    deleteForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        const submitBtn = document.getElementById('submitDelBtn');
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
                alert("Request sent successfully!");
                window.location.href = "/";
            } else {
                alert("Error sending request.");
            }
        } catch (error) {
            console.error("Submission Error:", error);
        } finally {
            submitBtn.textContent = "Send Delete Request";
            submitBtn.disabled = false;
        }
    });
}