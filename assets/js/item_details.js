import $ from 'jquery';
/*
    Called when the plus button next to a quantity is pressed
 */

alert("test")

$(".increment").click(function () {
    addQuantity(1, $(this))
});
/*
    Called when the minus button next to a quantity is pressed
 */
$(".decrement").click(function () {
        console.log("CLICKED decrement")
        //if quantity is less than zero, do not decrement further
        if (parseInt($(this).siblings(".item_quantity").val()) <= 0) {
            console.log("Could not decrement further")
        }
        else{
            addQuantity(-1, $(this))
        }
    });

/*
    Gets the quantity field for the incremented/decrement button and changes its value
 */
function addQuantity(value, caller) {
    var quantityElem = caller.siblings().find(".item_quantity")
    var newQuantity = parseInt(quantityElem.val()) + value
    quantityElem.val(newQuantity)
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
