const imageContainer = document.getElementById('imageContainer')

function oldMethodTask(){

     let end = 34
     for (let i = 2; i <= end ; i++) {
        
          const html = `
          <div class="image">
                         <img src="./default_images/img_${i}.jpg" alt="${i} image">
                    </div>
          `
        imageContainer.innerHTML += html
        
     }
}

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
