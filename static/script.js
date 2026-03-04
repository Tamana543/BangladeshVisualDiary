const imageContainer = document.getElementById('imageContainer')
const addBtn = document.getElementById('addBtn')
const sendBtn = document.getElementById('sendBtn')
const container = document.querySelector(".container")
const formContainer = document.querySelector(".form_container")
const svgContainer = document.querySelector(".svgContainer")
const homeBtn = document.getElementById("homeBtn");
const dropArea = document.querySelector(".formbold-file-input");
const fileInput = document.getElementById("file")
// Jsons

// loding images

// fetch('/api/photos').then(res=>{ // take a look here
//   return res.json()
// })

const xhr = new XMLHttpRequest();

xhr.open("POST", "/api/photos", true);

xhr.upload.onprogress = function (e) {
  if (e.lengthComputable) {
    const percent = (e.loaded / e.total) * 100;
    console.log("Uploading: " + percent.toFixed(0) + "%");

    progressBar.style.width = percent + "%";
    progressText.textContent = percent.toFixed(0) + "%";
  }
};

xhr.onload = function () {
  if (xhr.status === 201) {
    progressText.textContent = "Upload Complete ✅";
    setTimeout(() => location.reload(), 1000);
  } else {
    progressText.textContent = "Upload Failed ❌";
  }
};

xhr.onerror = function () {
  progressText.textContent = "Upload Error ❌";
};

xhr.send(formData).then(images=>{
  images.forEach((element,ind) => {
    // /static/default_images/${element.fileInput}

    imageContainer.innerHTML +=  `
    <div class="image hover10">
    <img src="/static/default_images/${element.filename}" alt="image ${ind+1}">
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
// Drag and drop functionality 

dropArea.addEventListener("dragover",(event)=>{
event.preventDefault()
})

dropArea.addEventListener("drop",(event)=>{
event.preventDefault()
fileInput.files = event.dataTransfer.files;
})

dropArea.addEventListener("dragenter", () => {
  dropArea.style.border = "2px solid #F83999";
});

dropArea.addEventListener("dragleave", () => {
  dropArea.style.border = "1px dashed #e0e0e0";
});
//Event listeners
addBtn.addEventListener("click",formDisplayer)
sendBtn.addEventListener("click",(event)=>{

  event.preventDefault();

  const fileInput = document.getElementById("file");
  const description = document.getElementById("description").value;
  const sender = document.getElementById("sender").value;

  const formData = new FormData() // creates a container(object) that mimics a real HTML form submission and allows file uploads.
  formData.append("file",fileInput.files[0])// to get the uploaded file 
  formData.append("description",description)
  formData.append("sender",sender)





  fetch("/api/photos", {
    method: "POST",
    body: formData
  })
  .then(res => res.json())
  .then(data => {
    console.log("Success:", data);

    // reload page to show new image
    location.reload();
  })
  .catch(err => console.log(err));
});

