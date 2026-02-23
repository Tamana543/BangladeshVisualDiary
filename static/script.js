const imageContainer = document.getElementById('imageContainer')
const addBtn = document.getElementById('addBtn')
const sendBtn = document.getElementById('sendBtn')
const container = document.querySelector(".container")
const formContainer = document.querySelector(".form_container")
const svgContainer = document.querySelector(".svgContainer")
// Jsons

// loding images

fetch('/api/photos').then(res=>{ // take a look here
  return res.json()
})
.then(images=>{
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

