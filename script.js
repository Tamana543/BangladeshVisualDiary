const imageContainer = document.getElementById('imageContainer')


let end = 34
for (let i = 2; i <= end ; i++) {
   
     const html = `
     <div class="image">
                    <img src="./default_images/img_${i}.jpg" alt="${i} image">
               </div>
     `
   imageContainer.innerHTML += html
     
}
