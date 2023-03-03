
// start dashBord Script

let dropDataDownEl = document.querySelectorAll("[data-dropDown]");

function dropCheck(e) {
    if (e.children[0].parentElement.classList.contains("op")) {
        e.children[0].nextElementSibling.style.maxHeight = `${e.children[0].nextElementSibling.scrollHeight}px`
    }
    else {
        e.children[0].nextElementSibling.style.maxHeight = `${0}px`
    }
}
if (dropDataDownEl.length > 0) {

    dropDataDownEl.forEach(e => {
        // console.log(e.children);
        e.children[0].addEventListener("click", b => {
            e.children[0].parentElement.classList.toggle("op");
            dropCheck(e);
        })

    })
}

let linksPart = document.querySelector(".links-part");
let linksToggle = document.querySelector(".links-part .toggle-btn");
if(linksPart != null){
    function linksPartLeft(){
        if(window.innerWidth <= 991){
            linksPart.classList.add("close");
            // if(linksPart.classList.contains("close")){
            //     linksPart.style.left =  `-${linksPart.getBoundingClientRect().width}px`;
            // }
        }
        else{
            // linksPart.style.left =  `0px`;

        }
    }
    linksPartLeft();
    window.onresize = e=>{
        linksPartLeft();
    }
    if(linksToggle != null){
        linksToggle.addEventListener("click" , e=>{
            linksPart.classList.toggle("close")
        })
    }
}