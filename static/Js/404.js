// --- Elements ---
const body = document.querySelector("body");
const modeTogglerBtn = document.querySelector(".tdnn");
const modeTogglerMoon = document.querySelector(".moon");
const homeBtn = document.getElementById("homeBtn");
const svgContainer = document.querySelector(".svgContainer");

lottie.loadAnimation(

{ container: svgContainer,

renderer: 'svg',

loop: true,

autoplay: true,

  path: '/static/404_anime.json'}
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



