var FieldForm = {
    _form: $("#fieldForm"),
    fieldName: $("#fieldForm #fieldName"),
    fieldType: $("#fieldForm #fieldType"),
    modelType: this.find("modelType"),
    submitButton : $("submit"),
    _fields: [fieldName, fieldType, modelType],

    onSubmit: function(){
        console.log("FieldForm.onSubmit"); 
        for (var i=0; i < this._fields.length; i++) {
            console.log("_field is " + FieldForm._fields[i].value); 
        }
    }

};



function addModelFormEvents(){
    var populateModelTypesSelect = function() {
        console.log("Populating modelsTypesSelect " + FieldForm.modelType); 
        $.ajax({
            type: "GET",
            url: "/modeltypes/list",
            success: function(data) {
                console.log("Success");
                console.log(data);     
            }
        }); 
        

    }; 

    var bindAddFieldClickEvent = function() {
        $("#addFieldSubmit").click(function() {
            FieldForm.onSubmit(); 
        })
    }; 
    
    populateModelTypesSelect();
    bindAddFieldClickEvent(); 
}

$(document).ready(function(){
    console.log("Document ready");
    addModelFormEvents(); 
}); 

