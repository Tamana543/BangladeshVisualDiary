const imageContainer = document.getElementById('imageContainer')
const addBtn = document.getElementById('addBtn')
const container = document.querySelector(".container")
const formContainer = document.querySelector(".form_container")
const svgContainer = document.querySelector(".svgContainer")

let svg = lottie.loadAnimation({ container: svgContainer, renderer: 'svg', loop: true, autoplay: true, path: 'Kitty_Cat.json'})
// Jsons

// loding images
fetch('./images.json').then(res=>{
 return res.json()
})
.then(images=>{
images.forEach((element,ind) => {

           imageContainer.innerHTML +=  `
        <div class="image">
          <img src="./default_images/${element}" alt="image ${ind}">
        </div> ` 
});
})
.catch(err=>console.log(err))


function formDisplayer(){
container.classList.toggle("hidden")
formContainer.classList.toggle("show")

// looding svg 
fetch('./Kitty_Cat.json').then(res=>{
  // console.log("I took the svg");
  return res.json()
}).then(svg=>{
  svgContainer.innerHTML += svg
})

}

addBtn.addEventListener("click",formDisplayer)