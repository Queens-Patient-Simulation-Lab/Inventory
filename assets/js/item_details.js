import 'bootstrap4-tagsinput/tagsinput'
/*
    Called when the plus button next to a quantity is pressed
 */

//--------------TAGS-----------------

$(".tagsInputBoxContainer").hide();

if (!$("#locationSelect option:selected").length) {
    $(".locationAdder").hide()
}

$("#tagsInputBox").tagsinput({
  trimValue: true
});

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


$(".deleteRow").click((e) => {
    let quantity = $(e.target).siblings(".item_quantity")
    console.log(quantity)
    console.log(quantity.val())
    if ($(e.target).siblings(".item_quantity").val() > 0) {
        return
    }
    let deletedLocation = $(e.target).parent().parent().parent()
    let deletedId = deletedLocation.attr("id")
    deletedLocation.replaceWith("<input hidden name=\"deletedRows\" value=\""+ deletedId +"\">\n")
})


$(".addRow").click(function () {
    let locationSelector = $("#locationSelect option:selected");

    let locationId = locationSelector.attr('data-id');
    let locationName = locationSelector.val()
    // This value is 
    let itemStorageTag = "newItemStorage"

    let newRow = $($.parseHTML(
        "                    <tr>\n" +
        "                        <th scope=\"row\">"+ locationName +"</th>\n" +
        "                        <td class=\"row th-lg\">\n" +
        "                                <div class=\"input-group row\">\n" +
        "                                    <button type=\"button\" class=\"btn btn-danger decrement rounded-0 disable-tap-zoom\">\n" +
        "                                        -\n" +
        "                                    </button>\n" +
        "                                    <input hidden name=\""+ itemStorageTag +"\" value=\""+locationId+"\">" +
        "                                    <input name=\"original-quantity-location-"+ locationId +"\" readonly hidden class=\"form-control\" id=\"item_quantity_original\" value=\"0\">\n" +
        "                                    <input name=\"quantity-location-"+ locationId +"\" type=\"number\" min=\"0\" inputmode=\"numeric\" pattern=\"[0-9]*\" title=\"Non-negative integer\" id=\"item_quantity\"\n" +
        "                                           class=\"form-control item_quantity col-sm-6 col-8 text-center\"\n" +
        "                                           value=\"0\">\n" +
        "                                    <button type=\"button\" class=\"btn btn-success increment rounded-0 disable-tap-zoom\">\n" +
        "                                        +\n" +
        "                                    </button>\n" +
        "                                    <button type=\"button\" class=\"btn btn-sm btn-outline-danger m-1 deleteRow\">Delete</button>" +
        "                                </div>\n" +
        "                        </td>\n" +
        "                    </tr>\n"
    )[1]);

    newRow.find(".increment").click(function () {
        addQuantity(1, $(this))
    });
    newRow.find(".decrement").click(function () {
        //if quantity is less than zero, do not decrement further
        if (parseInt($(this).siblings(".item_quantity").val()) <= 0) {
            console.log("Could not decrement further")
        }
        else{
            addQuantity(-1, $(this))
        }
    });

    $(".locationsTable > tbody").append(newRow);

    locationSelector.remove()
    locationSelector = $("#locationSelect option:selected");

    if (!locationSelector.length) {
        $(".locationAdder").hide()
    }


});



/* Async submit request */
$("#item-details-form").submit(function(e) {

    e.preventDefault(); // avoid to execute the actual submit of the form.

    var form = $(this);
    var url = form.attr('action');

    $.ajax({
           type: "POST",
           url: url,
           data: form.serialize(), // serializes the form's elements.
           success: function(data) {
               $(".modal").modal("hide");
           }
    });
});

