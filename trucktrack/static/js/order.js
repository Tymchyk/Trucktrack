document.addEventListener("DOMContentLoaded",()=>{
    if(document.querySelector("#reply")){
        document.querySelector("#reply").addEventListener("click",()=>customerReply())
    }
    if(document.querySelector("#start_job")){
        document.querySelector("#start_job").addEventListener("click",()=>customerStart())
    }  
    if(document.querySelector("#change_job")){
        document.querySelector("#change_job").addEventListener("click",()=>customerChange())
    }  
    if(document.querySelector("#delete_job")){
        document.querySelector("#delete_job").addEventListener("click",()=>customerDelete())
    }
})
 

function customerReply(){
    replyOrder = document.querySelector(".reply").dataset.value;
    performerReply = document.querySelector("#reply").value;
    fetch(`/order/${replyOrder}`,{
        method:"PUT",
        body:JSON.stringify({
            performer:`${performerReply}`,
        })
    })
}

function customerStart(){
    replyOrder = document.querySelector(".job").dataset.value;
    performerReply = document.querySelector("#performer").value;
    fetch(`/order/${replyOrder}`,{
        method: "POST",
        body:JSON.stringify({
            visability: 'False',
            perform: `${performerReply}`
        })
    })
    document.querySelector(".starting").style.display ="none";
    document.querySelector(".changes").style.display ="block";
    document.querySelector(".changes").innerHTML="";
    let id = document.querySelector("#orderid").textContent;
    let elem = document.createElement("div")
    elem.innerHTML =` <form action="/order/${replyOrder}" method="post" class="job" data-value="${id}" onsubmit="return false;" >
    <button id="changejob" class="btn btn-success change" type ="submit">Change worker </button>
    </form>
    <form action="/order/${replyOrder}" method="delete" class="job" data-value="${id}" onsubmit="return false;">
        <button id="deletejob" class="btn btn-success delete" type ="submit">Delete work</button>
    </form>`
    document.querySelector(".changes").append(elem)
    document.querySelector("#changejob").addEventListener("click",()=>customerChange())
    document.querySelector("#deletejob").addEventListener("click",()=>customerDelete())
}
function customerChange(){
    replyOrder = document.querySelector(".job").dataset.value;
    fetch(`/order/${replyOrder}`,{
        method: "POST",
        body:JSON.stringify({
            visability: 'True',
        })
    })
    document.querySelector(".changes").style.display="none";
    document.querySelector(".starting").style.display ="block";
    document.querySelector(".starting").innerHTML ="";
    fetch(`/orderstart/${replyOrder}`)
    .then(response =>response.json())
    .then(performers=>{
        let id = document.querySelector("#orderid").textContent;
        let elem = document.createElement("div")
        elem.innerHTML+=`<form action="/order/${replyOrder}" method="post" class="job" data-value="${id}" onsubmit="return false;">
        <select id="performer" class=" startForm form-select"></select>
        <button id="startjob" class="btn btn-success start" type ="submit">Start work </button>
        </form`
            document.querySelector(".starting").append(elem);
            document.querySelector(".performer");
            for(let i=0;i<performers.length;i++)
            {
                let option = document.createElement("option")
                option.text =`${performers[i].performer}`
                option.value=`${performers[i].performer_id}`
                document.querySelector("#performer").add(option)
            }
        document.querySelector("#startjob").addEventListener("click",()=>customerStart())
    })
    
}

function customerDelete(){
    replyOrder = document.querySelector(".job").dataset.value;
    fetch(`/order/${replyOrder}`,{
        method: "DELETE",
        body:JSON.stringify({
            visability: 'True',
        })
    }) 
    document.querySelector(".changes").innerHTML =`<h5 class="title">Delete order successfully</h5>`;
}
