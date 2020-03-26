import 'bootstrap4-tagsinput/tagsinput'
/*
    Called when the plus button next to a quantity is pressed
 */

//--------------TAGS-----------------

$(".tagsInputBoxContainer").hide();

$.each($(".tagsShown").children().map(function(){return $(this).text();}).get(), function(index, value) {
    $('#tagsInputBox').tagsinput('add', value);
});

$("#tagsInputBox").tagsinput({
  trimValue: true
});

$(".tagEditBtn").click(function () {
    $(".tagsInputBoxContainer").show();
    $(".tagsShown").hide();
    $(".tagEditBtn").hide();
});

//--------------------------------

$(".increment").click(function () {
    addQuantity(1, $(this))
});
/*
    Called when the minus button next to a quantity is pressed
 */
$(".decrement").click(function () {
        console.log("CLICKED decrement");
        //if quantity is less than zero, do not decrement further
        if (parseInt($(this).siblings(".item_quantity").val()) <= 0) {
            console.log("Could not decrement further")
        }
        else{
            addQuantity(-1, $(this))
        }
});

function addQuantity(value, caller) {
    caller.siblings(".item_quantity").val(
        parseInt(caller.siblings(".item_quantity").val()) + value
    );
}


/* Async submit request */
$("#item-details-form").submit(function(e) {

    e.preventDefault(); // avoid to execute the actual submit of the form.

    var form = $(this);
    var url = form.attr('action');

    $.ajax({
           type: "POST",
           url: url,
           data: form.serialize(), // serializes the form's elements.
           success: function(data)
           {
               $(".modal").modal("hide");
           }
         });
    });

