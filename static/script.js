const imageContainer = document.getElementById('imageContainer')
const addBtn = document.getElementById('addBtn')
const sendBtn = document.getElementById('sendBtn')
const container = document.querySelector(".container")
const formContainer = document.querySelector(".form_container")
const svgContainer = document.querySelector(".svgContainer")
const homeBtn = document.getElementById("homeBtn");
const dropArea = document.querySelector(".formbold-file-input");
const fileInput = document.getElementById("file")
const progressBar = document.getElementById("progressBar");
const progressFill = document.getElementById("progressFill");
const statusText = document.getElementById("uploadStatus");
const fileText = document.getElementById("fileText");
const fileLabel = document.getElementById("fileLabel");
const formboalContainer = document.getElementById("formbold-text-container")
const lightbox = document.querySelector(".lightbox")
const lightboxImg = document.querySelector(".lightbox-img")
const nextBtn = document.querySelector(".next")
const preBtn = document.querySelector(".prev")
const closeBtn = document.querySelector(".close")
const modeTogglerBtn = document.querySelector(".tdnn")
const modeTogglerMoon = document.querySelector(".moon")
const body = document.querySelector("body")
let currentInd = 0
let imageList = []
// loding images

fetch('/api/photos')
.then(res=>{
  return res.json()
})
.then(images=>{
imageList = images
  images.forEach((element,ind) => {
    // /static/default_images/${element.fileInput}
    
    imageContainer.innerHTML +=  `
    <div class="image hover">
    <img src="/static/default_images/${element.filename}"
     alt="image ${ind+1}"
      data-index="${ind}"
      >
    
       <div class="description"> 
  <p>${element.description} </p>
  <p>  📸 : ${element.sender} </p>

    </div>
    </div>
   
    ` 
 
 
});
})
.catch(err=>console.log(err))


function formDisplayer(){
container.classList.toggle("hidden")
formContainer.classList.toggle("show")
homeBtn.style.top  = "20px"

// looding svg 
lottie.loadAnimation(
  { container: svgContainer, 
    renderer: 'svg', 
    loop: true, 
    autoplay: true,
     path: '/static/Kitty_Cat.json'}
)
}

function formHide(){
  formContainer.classList.toggle("show")
  container.classList.toggle("hidden")
}
function showIMG(index){
const imageData = imageList[index]

lightboxImg.src = `/static/default_images/${imageData.filename}`
lightbox.alt =`image ${index + 1}`
}

function nextIMG(){
  currentInd++;
   if(currentInd >= imageList.length){
    currentInd = 0
  }

  showIMG(currentInd)
}

function prevIMG(){
currentInd--;
if(currentInd < 0){
  currentInd = 0
}
showIMG(currentInd)
}
function closeLightBox(){
  lightbox.classList.add("hidden")
}
//Event listeners
// Drag and drop functionality  

dropArea.addEventListener("dragover",(event)=>{
event.preventDefault()
})

dropArea.addEventListener("drop",(event)=>{
event.preventDefault()
fileInput.files = event.dataTransfer.files;
const fileName = fileInput.files[0].name;
fileText.textContent = fileName.length > 30 ? fileName.substring(0,30)+"..." : fileName;

fileLabel.style.border = "2px solid #f83999"
})

dropArea.addEventListener("dragenter", () => {
  dropArea.style.border = "2px solid #F83999";
});

dropArea.addEventListener("dragleave", () => {
  dropArea.style.border = "1px dashed #e0e0e0";
});

imageContainer.addEventListener("click",(event)=>{
  if(event.target.tagName === "IMG"){
    currentInd = Number(event.target.dataset.index)
    const src = event.target.src;
    const alt = event.target.alt;
    lightbox.classList.remove("hidden")
    lightboxImg.src = src;
    lightboxImg.alt = alt
  }
})

nextBtn.addEventListener("click",nextIMG)
preBtn.addEventListener("click",prevIMG)
closeBtn.addEventListener("click",closeLightBox)
document.addEventListener("keydown",(event)=>{
  if(event.key === "Escape"){
    closeLightBox()
  }

  if(event.key === "ArrowLeft"){
    prevIMG()
  }
if (event.key === "ArrowRight") {
  nextIMG()
}
})
// Btn event listeners
addBtn.addEventListener("click",formDisplayer)

sendBtn.addEventListener("click",async (event)=>{

  event.preventDefault();
  const file = fileInput.files[0];
  const description = document.getElementById("description").value;
  const sender = document.getElementById("sender").value;

if(!file){
alert("Please choose a file :)")
return;
}
  const formData = new FormData() 
  formData.append("file",file) 
  formData.append("description",description)
  formData.append("sender",sender)




// UI Changes before upload

sendBtn.disabled =true;
sendBtn.textContent = "Uploading.. "
progressBar.classList.remove("hidden")
statusText.classList.remove("hidden")
statusText.textContent = "Uploading your image... "

try {
  // not real 
  let width = 0;
  const progress = setInterval(() => {
    if (width < 90) {
      width += 5
      progressFill.style.width = width + '%';
    }
  }, 100);

  const response = await fetch("/api/photos", {
    method: "POST",
    body: formData
  })

  clearInterval(progress)

  if(!response.ok) throw new Error("Upload Failed");
  
    progressFill.style.width = "100%";
    statusText.textContent = "Uploaded Successfully ✓";
    sendBtn.textContent = "Done";

  setTimeout(() => {
    location.reload()
  }, 1200);

} catch (error) {
  progressFill.style.background = "red";
  statusText.textContent = " Upload Failed :("
  sendBtn.disabled = false;
  sendBtn.textContent = "Send File"
}
 
});

fileInput.addEventListener("change", () => {
  if (fileInput.files && fileInput.files.length > 0) {
    formboalContainer.style.display ="none"
    const fileName = fileInput.files[0].name;

    fileText.textContent =
      fileName.length > 30
        ? fileName.substring(0, 30) + "..."
        : fileName;

    fileLabel.style.border = "2px solid #f83999";
  }
});
modeTogglerBtn.addEventListener("click",()=>{
  modeTogglerBtn.classList.toggle('day');
body.classList.toggle('light')
modeTogglerMoon.classList.toggle("sun")
addBtn.classList.toggle("light")
})

