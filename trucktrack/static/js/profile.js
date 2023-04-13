if(document.querySelector("#settings"))
{
    document.querySelector("#settings").addEventListener("click",() => addSettings());
}
if(document.querySelector("#chat")){
    document.querySelector("#chat").addEventListener("click",()=> chatting());
}
if(document.querySelector("#orders")){
    document.querySelector("#orders").addEventListener("click", ()=> MyOrders());
}
if(document.querySelector(".comment")){
    document.querySelector(".comment").addEventListener("click",() =>{
        let grade = document.querySelector("#stars").textContent;
        let comment = document.querySelector("#comment").value;
        let id = document.querySelector(".comment").value;
        fetch(`/rating/${id}`,{
            method:"POST",
            body:JSON.stringify({
                grade:`${grade}`,
                comment:`${comment}`
            })
        })
        let name = document.querySelector(".name").dataset.value;
        let element = document.createElement("div")
        element.classList ="commentDiv"
        element.innerHTML+=`<h5 class="commentTitle">${name}</h5>`;
        for(let j=0; j< parseInt(grade);j++){
            element.innerHTML +=`<div class="comment-star">`
        }
        element.innerHTML+=`<h6 class="commentText">${comment}</h6>`;
        document.querySelector(".comments").append(element)
    
        
    })
}


let ratings = document.querySelectorAll('.ratings');
for( let i= 0; i< ratings.length; i++)
{   const star = ratings[i];
    star.addEventListener("click",()=>{
    if(star.classList.value ==="ratings")
    {   for(let i = 0; i< star.value; i++)
        {
            ratings[i].classList.remove("ratings");
            ratings[i].classList.add("active-star");
        }
        document.querySelector("#stars").innerHTML =`${star.value}`
    }
    else{
        for(let i = ratings.length - 1; i >= star.value; i--)
        {   
            ratings[i].classList.remove("active-star");
            ratings[i].classList.add("ratings");
        }
            document.querySelector("#stars").innerHTML =`${star.value}`
    }
    
    })
}
let user = document.querySelector(".comments");
fetch(`/rating/${user.dataset.value}`)
.then(response => response.json())
.then(grade=>{
    for(let i=0; i< grade.length;i++){
        let elem = document.createElement("div");
        elem.classList ="commentDiv"
        elem.innerHTML+=`<h5 class="commentTitle">${grade[i].comentator}</h5>`;
        for(let j=0; j< parseInt(grade[i].grade);j++){
            elem.innerHTML +=`<div class="comment-star">`
        }
        elem.innerHTML+=`<h6 class="commentText">${grade[i].comment}</h6>`;
        document.querySelector(".comments").append(elem)
    }
})

function addSettings(){
    document.querySelector(".profile").style.display = "none";
    document.querySelector(".comments").style.display = "none";
    document.querySelector(".settings").innerHTML ="";
    document.querySelector(".settings").style.display = "block";
    let profile = document.querySelector("#settings").value;
    let elem =document.createElement("div");
    elem.classList ="setChanges"
    elem.innerHTML = `<form action="/profile/${profile}" method="post" onsubmit="return false;">
    <input class="form-control" id="phone" placeholder="Write your phone number">
    <input class="form-control" id ="city" placeholder="Write your city">
    <input class="form-control" id ="truckTonnage" placeholder="Write your truck tonnage">
    <button type= "submit" class="btn btn-success" id="confirm">Confirm changes</button>
    </form>
    <button class ="btn btn-success" id="toProfile"> Return to profile page</button>` 
    document.querySelector(".settings").append(elem)

    document.querySelector("#confirm").addEventListener("click",()=>confirmChanges(profile))
    document.querySelector("#toProfile").addEventListener("click",() =>toProfile())
}

function confirmChanges(profile){
    let city = document.querySelector("#city").value;
    let phone = document.querySelector("#phone").value;
    let truck = document.querySelector("#truckTonnage").value;
    fetch(`/profile/${profile}`,{
        method:"POST",
        body:JSON.stringify({
            "city":`${city}`,
            "phone":`${phone}`,
            "truck":`${truck}`
        })
    })
    toProfile()
    document.querySelector(".profile_city").innerHTML = `City: ${city}`;
    document.querySelector(".profile_phone").innerHTML = `Phone: ${phone}`;
    document.querySelector(".tonnage").innerHTML =`Truck tonnage: ${truck}`;

    
}

function toProfile(){
    document.querySelector(".profile").style.display = "block";
    document.querySelector(".settings").style.display = "none";
    document.querySelector(".chat").style.display = "none";
    document.querySelector(".comments").style.display ="block";
    if(document.querySelector("#settings")){
        document.querySelector("#settings").style.display ="block";
    }
}


function chatting(){
    document.querySelector(".profile").style.display = "none";
    if(document.querySelector("#settings")){
        document.querySelector("#settings").style.display ="none";
    }
    document.querySelector(".comments").style.display ="none";
    document.querySelector(".rating").style.display ="none";
    document.querySelector(".chat").innerHTML="";
    document.querySelector(".chat").style.display ="block"; 
    let profile = document.querySelector("#chat").value;
    let elem = document.createElement("div")
    elem.innerHTML=`<form action="/profile/${profile}" method="put" onsubmit="return false;">
    <input class="form-control" id ="message" placeholder="Write your message">
    <button type= "submit" class="btn btn-success" id="send">Send message</button>
    </form>
    <button class ="btn btn-success" id="toProfile"> Return to profile page</button>
    `
    document.querySelector(".chat").append(elem)
    document.querySelector("#send").addEventListener("click",()=>SendMessage(profile))
    document.querySelector("#toProfile").addEventListener("click",() =>toProfile())
}

function SendMessage(profile){
    let message= document.querySelector("#message").value;
    fetch(`/profile/${profile}`,{
        method:"PUT",
        body:JSON.stringify({
            "message":`${message}`
        })
    })
}

function MyOrders(){
    document.querySelector(".profile").style.display = "none";
    document.querySelector(".comments").style.display = "none";
    document.querySelector(".Orders").style.display ="block";
    document.querySelector(".Orders").innerHTML="";
    fetch("/profileorders")
    .then(response => response.json())
    .then(orders=>{
        for(let i = 0; i < orders.length ; i++)
        {
            let elem =document.createElement("div")
            elem.classList ="order";
            elem.innerHTML =`<h6 class="titleorder"><a href ="/order/${orders[i].id}">${orders[i].title}</a></h6>
            <h6 class="titleorder">${orders[i].sender} - ${orders[i].receiver}</h6>
            <h6 class ="titleorder">Price: ${orders[i].bid} $</h6>
            <h6 class ="titleorder">Tonnage: ${orders[i].timestamp} t</h6>`
            document.querySelector(".Orders").append(elem)
        }
        
    })
    let element = document.createElement("div")
    element.innerHTML =`<button class="btn btn-success returnTo"> Return to homepage </button>`
    document.querySelector(".Orders").append(element)
    document.querySelector(".returnTo").addEventListener("click",()=>{
        document.querySelector(".profile").style.display = "block";
        document.querySelector(".comments").style.display = "block";
        document.querySelector(".Orders").style.display = "none";
    })
}