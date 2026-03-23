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

  path: '/static/Cat playing animation_2.json'}
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

// Function alert box
function  showFancyAlert(title, message) {
    const modal = document.getElementById('customAlert');
    document.getElementById('alertTitle').textContent = title;
    document.getElementById('alertMessage').textContent = message;
    
    modal.classList.remove('hidden');

    lottie.loadAnimation({
        container: document.getElementById('successAnim'),
        renderer: 'svg',
        loop: false,
        autoplay: true,
        path: '/static/Loader cat.json' 
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
      const resData = await response.json();
            if (response.ok) {
               showFancyAlert("Request Sent!", resData.message);
                
                document.getElementById('closeAlertBtn').onclick = () => {
                    window.location.href = "/";
                };

            } else {
               showFancyAlert("Error", "Something went wrong on the server.");
            }
        } catch (error) {
            console.error("Submission Error:", error);
            showFancyAlert("Error", "Could not connect to the server.");
        } finally {
            submitBtn.textContent = "Send Delete Request";
            submitBtn.disabled = false;
        }
    });
}