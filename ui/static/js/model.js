var ModelForm = {
    _form: $("#modelForm"),
    submitButton: $("#modelForm submit"),

    onSubmit: function(){
        console.log("Submitting modelForm"); 
	var fieldValues = ModelForm.getFieldValues(); 
	console.dir(fieldValues); 
    },

    getFieldValues: function(){
	console.log("getFieldValues()"); 
	var fieldValues = [];
	var field_rows = $("#modelForm #field-row"); 
	for (var i=0; i< field_rows.length; i++) { 
	    console.log(field_rows[i]); 
	    var fieldValue = FieldRow.getFieldValue(field_rows[i]); 
	    fieldValues.push(fieldValue); 
	}
	return fieldValues;
    }, 

    submitModelFormEvent: function() {
        $("#modelSubmit").click(function() {
	    event.preventDefault(); 
	    console.log("submitButton clicked"); 
            ModelForm.onSubmit(); 
        })
    },
}; 

var FieldRow = {
    _row: $("#field-row-template"),
    fieldAttrs: ["name", "type", "choices", "is_required", "min_size", 
                 "max_size", "default_value", "messages", "compound_type"],

    getFieldValue: function(rowHtmlElem) {
	var fieldAttrValues = {}
        for (var i=0; i<FieldRow.fieldAttrs.length; i++) {
	    fieldAttrElem = $(rowHtmlElem).find("#"+ FieldRow.fieldAttrs[i]);
	    fieldAttrValues[FieldRow.fieldAttrs[i]] = fieldAttrElem.html(); 
	}
	return fieldAttrValues; 
    },

    create: function(data, append_to) {
       var newRow = this._row.clone(); 
       newRow.attr({class: "field-row",
	            id: "field-row"
	          }); 
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
        var data = {"name": FieldForm._fields[0].value,
	            "type": FieldForm._fields[1].value,
                    "default_value": FieldForm._fields[2].value,
                    "model": FieldForm._fields[3].value,
	               };
	    FieldRow.create(data); 
    },
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
    
    ModelForm.submitModelFormEvent(); 
    populateModelTypesSelect();
    bindAddFieldClickEvent(); 
}

$(document).ready(function(){
    console.log("Document ready");
    $("#field-row-template").hide(); 
    addModelFormEvents(); 
}); 

