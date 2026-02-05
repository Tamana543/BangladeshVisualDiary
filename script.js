const imageContainer = document.getElementById('imageContainer')
const addBtn = document.getElementById('addBtn')
const container = document.querySelector(".container")
const formContainer = document.querySelector(".form_container")


// Via Json
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

}

addBtn.addEventListener("click",formDisplayer)