const imageContainer = document.getElementById('imageContainer')
const addBtn = document.getElementById('addBtn')
const sendBtn = document.getElementById('sendBtn')
const container = document.querySelector(".container")
const formContainer = document.querySelector(".form_container")

// Jsons

// loding images
fetch('./src/images.json').then(res=>{
  return res.json()
})
.then(images=>{
  images.forEach((element,ind) => {
    
    imageContainer.innerHTML +=  `
    <div class="image hover10">
    
    <img src="./default_images/${element.file}" alt="image ${ind+1}">
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
     path: './src/Kitty_Cat.json'}
)
}

function formHide(){
  formContainer.classList.toggle("show")
  container.classList.toggle("hidden")
}

addBtn.addEventListener("click",formDisplayer)
sendBtn.addEventListener("click",formHide)
console.log(descriptionContainer);
