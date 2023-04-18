home_route={
    months:['JANUARY','FEBRUARY','MARCH','APRIL','MAY','JUNE','JULY','AUGUEST','SEPTEMBER','OCTOBER','NOVEMBAR','DECEMBER'],
    form:function(){
        
        return document.getElementById('form')
    },
    anchor:function(){
        return document.querySelectorAll("a[href='/view/']");
    },
    registerFormEvent:function(){
        this.form().addEventListener('submit',function(event){
            event.preventDefault();
            home_route.formHandler();
            console.log('event triggred')
        })
    },
    formHandler:function(){
        var data=this.formData(home_route.form())
        form_json=JSON.stringify(data);
        var request=new XMLHttpRequest();
        request.open('POST','/home');
        request.setRequestHeader("content-type","application/json");
        request.onload=function(event){
            if(request.responseText=="success"){
                console.log('json sent')
                home_route.updateDom(home_route.formData(home_route.form()));
            }
        }
        request.send(form_json);
    },
    formData:function(form){
        form_data={}
        form_data.date=form.elements['date'].value
        return form_data
    },
    updateDom:function(data){
        
        const date=new Date(data.date);
        let formated_date=`${this.months[date.getMonth()]} ${date.getDate()},${date.getFullYear()}`
        var food_floor=document.getElementById('food_floor');
        food_floor.innerHTML +=` <div class="food_tile" >
        <h3>${formated_date}</h3>
        <ul>
            <li>protein<span>0</span></li>
            <li>carbohydrates<span>0</span></li>
            <li>fat<span>0</span></li>
            <li>calories<span>0</span></li>
            <li><a href="/view/" style="color:inherit" class="${formated_date}">View Date</a></li>
        </ul>
    </div>
    `

    },
    sendQueary:function(){
        this.anchor().forEach(function(value){
            value.addEventListener('click',function(event){
                var anchorObj=event.target;
                anchorObj.href=`${anchorObj.href}?date=${anchorObj.className}`
                console.log(anchorObj.href)
                
            }

            )
        })
    }
}
window.onload=function(){
    home_route.registerFormEvent();
    home_route.sendQueary();
}
    