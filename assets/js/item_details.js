/*
    Called when the plus button next to a quantity is pressed
 */
$(".increment").click(function () {
    addQuantity(1, $(this))
});
/*
    Called when the minus button next to a quantity is pressed
 */
$(".decrement").click(function () {
    addQuantity(-1, $(this))
});

/*
    Gets the quantity field for the incremented/decrement button and changes its value
 */
function addQuantity(value, caller) {
    quantityElem = caller.siblings().find(".item_quantity")
    newQuantity = parseInt(quantityElem.val()) + value
    quantityElem.val(newQuantity)
}