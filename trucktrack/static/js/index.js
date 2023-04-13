document.querySelector(".find").addEventListener("click",()=>SubmitForm())

function SubmitForm(){
    let form = document.forms.Form;
    let origin = form.origin.value;
    let destination = form.destination.value;
    let tonnage = form.tonnage.value;
    let type = form.type.value;
    fetch(`/orders_map`,{
        method:"POST",
        body:JSON.stringify({
            "origin":`${origin}`,
            "destination":`${destination}`,
            "tonnage":`${tonnage}`,
            "type":`${type}`,
        })
    })
}


function initMap(){
    let directionService = new google.maps.DirectionsService();
    let directionRender = new google.maps.DirectionsRenderer();
    const map = new google.maps.Map(document.getElementById("map"),{
        zoom:6,
        center:{lat: 50.452194, lng:30.527561},
    });
    const infowindow = new google.maps.InfoWindow();
    directionRender.setMap(map);
    fetch("/orders_map")
        .then(response => response.json())
        .then(data=>{
            for (let i =0; i< data.length; i++){
                const request={
                    query :`${data[i].sender}`,
                    fields:['name','geometry'],
                }
                let services = new google.maps.places.PlacesService(map);
                services.findPlaceFromQuery(request,(results)=>{
                    for(let i= 0; i<results.length;i++)
                    {
                        addMarker(results[i],request)
                    }
                    map.setCenter(results[0].geometry.location)
                })
            }
            
        })
    function addMarker(place,location){
        let marker = new google.maps.Marker({
            map,
            position:place.geometry.location,

        })
        marker.addListener("click",()=>{
            fetch("/orders_map")
            .then(response =>response.json())
            .then(data =>{
                for(let i=0; i< data.length; i++)
                {
                    const content = document.createElement("div")
                    content.innerHTML =`<h6><a href="/order/${data[i].id}">${data[i].title}</a></h6>
                    <p>Tonnage: ${data[i].tonnage}</p>
                    <p>Type:${data[i].type}</p>
                    <p>${data[i].timestamp}</p>`
                    infowindow.setContent(content);
                    infowindow.open(map, marker);
                    const request_receiver={
                        query :`${data[i].receiver}`,
                        fields:['name','geometry'],
                    }
                    let services = new google.maps.places.PlacesService(map);
                    services.findPlaceFromQuery(request_receiver,(results)=>{
                        map.setCenter(results[0].geometry.location)
                    })
                    if(data[i].sender === location.query)
                    {
                        directionService.route({
                            origin:{
                                query:`${data[i].sender}`,
                            },
                            destination:{
                                query:`${data[i].receiver}`,
                            },
                            travelMode : google.maps.TravelMode.DRIVING,
                        })    
                        .then((response) => {
                            directionRender.setDirections(response);
                          })
                    }
                }
            })
        })
        
    }
}
window.initMap = initMap;
