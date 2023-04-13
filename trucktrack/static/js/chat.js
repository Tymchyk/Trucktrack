document.addEventListener("DOMContentLoaded", ()=>{
    document.querySelectorAll(".user").forEach(element =>{
        element.addEventListener("click", ()=> Openchat(element.value))
    })
})

function Openchat(user){
    document.querySelector(".chat").innerHTML =" ";
    document.querySelector(".send").innerHTML =" ";
    fetch(`/chats/${user}`)
    .then(response => response.json())
    .then(chat=>{
        for (let i = 0; i< chat.length; i++)
        {
            if(chat[i].message)
            {
                let elem = document.createElement("div")
                elem.classList ="item"
                elem.innerHTML =`<h6 class="username">${chat[i].writer}</h6>
                <h6 class="message">${chat[i].message}</h6>`
                document.querySelector(".chat").append(elem)
            }
        }
        let element = document.createElement("div")
        element.innerHTML =`<form action ="/chats/${user}" id ="send" method = "post" onsubmit="return false;">
        <input type= "text" placeholder= "Write message" name ="message" id = "message" class="form-control">
        <button class="btn btn-success sendMessage mt-2 ms-3">Send message</button>
        </form>`
        document.querySelector(".send").append(element)
        document.querySelector(".sendMessage").addEventListener("click",()=>{
            let message = document.querySelector("#message").value;
            fetch(`/chats/${user}`,{
                method:"POST",
                body:JSON.stringify({
                    "message":`${message}`,
                    })
                })
                let username = document.querySelector(".send").dataset.value;
                let newmess =document.createElement("div")
                newmess.innerHTML =`<h6 class="username">${username}</h6>
                <h6 class="message">${message}</h6>`
                document.querySelector(".chat").append(newmess)
                document.forms["send"].reset()
            })
          
    })
    
}