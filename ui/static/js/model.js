var FieldRow = {
    _row: $("#field-row-template"),
    create: function(data, append_to) {
       console.log("FieldRow.create(): " + data); 
       console.log(data); 
       var newRow = this._row.clone(); 
       for (var key in data) {
	       var newRowAttr = newRow.find("#"+key); 
	       newRowAttr.html(data[key]);  
       }
       $("#fields").append(newRow); 
       newRow.show(); 
    },
};


var FieldForm = {
    _form: $("#fieldForm"),
    fieldName: $("#fieldForm #fieldName"),
    fieldType: $("#fieldForm #fieldType"),
    fieldDefault: $("#fieldForm #fieldDefault"),
    modelType: this.find("modelType"),
    submitButton : $("submit"),
    _fields: [fieldName, fieldType, fieldDefault, modelType],

    onSubmit: function(){
        console.log("FieldForm.onSubmit"); 
        for (var i=0; i < this._fields.length; i++) {
            console.log("_field is " + FieldForm._fields[i].value); 
        }
        var data = {"name": FieldForm._fields[0].value,
	                "type": FieldForm._fields[1].value,
                    "default_value": FieldForm._fields[2].value,
                    "model": FieldForm._fields[3].value,
	               };
	    FieldRow.create(data); 
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
    $("#field-row-template").hide(); 
    addModelFormEvents(); 
}); 

