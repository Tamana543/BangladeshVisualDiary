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
    // /static/default_images/${element.filename}

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

  const filename = document.getElementById("file").value;
  const description = document.getElementById("description").value;
  const sender = document.getElementById("email").value;

  fetch("/api/photos", {
    method: "POST",
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify({
      filename: filename,
      description: description,
      sender: sender
    })
  })
  .then(res => res.json())
  .then(data => {
    console.log("Success:", data);

    // reload page to show new image
    location.reload();
  })
  .catch(err => console.log(err));
});

