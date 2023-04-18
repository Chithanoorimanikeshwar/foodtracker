Addfood={
    formData:function(form){
        form_data={};
        form_data.food=form.elements["food"].value;
        form_data.proteins=form.elements["protein"].value;
        form_data.carbohydrates=form.elements["carbohydrates"].value;
        form_data.fats=form.elements["fat"].value;
        form_data.calories=form.elements["calories"].value;
        return form_data
    },
    updateTotal:function(form_data){
            if(document.getElementById('tot_protein').firstElementChild.innerHTML=="None"){
                document.getElementById('tot_protein').firstElementChild.innerHTML=form_data.proteins;
                document.getElementById('tot_carbohydrates').firstElementChild.innerHTML=form_data.carbohydrates;
                document.getElementById('tot_fat').firstElementChild.innerHTML=form_data.fats;
                document.getElementById('tot_calories').firstElementChild.innerHTML=form_data.calories;
            }
            else {
                document.getElementById('tot_protein').firstElementChild.innerHTML=Number(document.getElementById('tot_protein').firstElementChild.innerHTML)+Number(form_data.proteins);
                document.getElementById('tot_carbohydrates').firstElementChild.innerHTML=Number(document.getElementById('tot_carbohydrates').firstElementChild.innerHTML)+Number(form_data.carbohydrates);
                document.getElementById('tot_fat').firstElementChild.innerHTML=Number(document.getElementById('tot_fat').firstElementChild.innerHTML)+Number(form_data.fats);
                document.getElementById('tot_calories').firstElementChild.innerHTML=Number(document.getElementById('tot_calories').firstElementChild.innerHTML)+Number(form_data.calories);
            }

    },
    url:function(form){
        var actions=form.getAttribute('action');   
        return actions;
        },
    handleForm:function(){
        var form=document.getElementById('foods');
        var url=this.url(form);
        var json_form=JSON.stringify(this.formData(form));
        var request=new XMLHttpRequest();
        request.open("POST",'/add_food');
        request.setRequestHeader("content-type","application/json");
        request.onload=function(){
            console.log(request.responseText);
            if(request.responseText=='success'){
                var form=document.getElementById('foods');
                Addfood.addItems(Addfood.formData(form));
                Addfood.updateTotal(Addfood.formData(form))
                form.reset()
            }
            else if(request.responseText=='repeat'){
                alert('item is already in the cart')
            }
            else{
                alert('sever busy please try adding after a minute')
            }
        }
        request.send(json_form);
        
    },
    addItems:function(form_data){
        const parent=document.getElementById('food_floor');
        /*
        const clone_parent=child.cloneNode(true);
        clone_child.id=form_data["food"];
        const parent=document.getElementById('food_floor');
        parent.appendChild(clone_child);
        document.querySelector('#'+form_data['food']+' ul li.special').textContent=form_data['food'];
        var list_items=document.querySelectorAll('#'+form_data['food']+' ul>li + *');
        var count=0;
        var inner_count=0;
        for(data in form_data){
            
            console.log('1');
            if(count>0){
                
                list_items[inner_count].querySelector('span').innerHTML=form_data[data];
                inner_count=inner_count+1;
            }      
            count=count+1;  
        }
        */
    parent.innerHTML+=
        `<div class="food_tile add_food_tile">
            <ul>
                <li class="special">${  form_data['food'] }</li>
                <li>protein<span>${ form_data['proteins'] }</span></li>
                <li>carbohydrates<span>${ form_data['carbohydrates'] }</span></li>
                <li>fat<span>${ form_data['fats'] }</span></li>
                <li>calories<span>${ form_data['calories']}</span></li>
            </ul>
        </div>`

    }


}
form=document.getElementById("foods");
form.addEventListener('submit',function(event){
    event.preventDefault();
    Addfood.handleForm();
})
