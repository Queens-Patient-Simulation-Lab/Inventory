import 'bootstrap4-tagsinput/tagsinput'
/*
    Called when the plus button next to a quantity is pressed
 */

//--------------TAGS-----------------

$(".tagsInputBoxContainer").hide();

$("#tagsInputBox").tagsinput({
    trimValue: true
});

$.each($(".tagsShown").children().map(function () {
    return $(this).text();
}).get(), function (index, value) {
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
    } else {
        addQuantity(-1, $(this))
    }
});

function addQuantity(value, caller) {
    caller.siblings(".item_quantity").val(
        parseInt(caller.siblings(".item_quantity").val()) + value
    );
}

$(".delete-img-btn").click(function(){
    var deleteUrl = $(this).attr('data-access-url')
    var csrftoken = jQuery("[name=csrfmiddlewaretoken]").val();

    $.ajax({
        type: "DELETE",
        url: deleteUrl,
        beforeSend: function(xhr) {
        xhr.setRequestHeader("X-CSRFToken", csrftoken);
    },
        complete: function (msg) {
            location.reload()

$("#add-image-input").change(function (e) {
    // todo, add items to a list of files to submit
    // todo, when you delete items, keep track of their ids if they exist, or remove from upload list otherwise
    let carousel = document.getElementById("itemImageCarousel")
    let carouselIndicators = carousel.getElementsByClassName('carousel-indicators')[0]
    let carouselInner = carousel.getElementsByClassName("carousel-inner")[0]

    let firstImgDiv = carouselInner.firstElementChild
    let firstIsEmpty = false
    if (firstImgDiv.classList.contains("empty-item")){
        firstIsEmpty = true
        firstImgDiv.classList.remove("empty-item")
    }

    for (var i = 0; i < e.target.files.length; i++) {

        var file = e.target.files[i];

        console.log("File was uploaded")

        // ADD NEW INDICATOR
        let newIndicator = carouselIndicators.firstElementChild.cloneNode(true)
        newIndicator.classList.remove("active")

        newIndicator.setAttribute("data-slide-to", carouselIndicators.childElementCount)
        carouselIndicators.appendChild(newIndicator)


        // Add new image
        let newImageDiv = firstImgDiv.cloneNode(true)
        newImageDiv.classList.remove("active")
        newImageDiv.setAttribute("data-item-id", -1)

        let image = newImageDiv.getElementsByClassName("carousel-image")[0]
        let reader = new FileReader();
        reader.onloadend = function() {
             image.src = reader.result;
        }
        reader.readAsDataURL(file);
        carouselInner.appendChild(newImageDiv)

    }
    if (firstIsEmpty){
        firstImgDiv.remove()
        carouselInner.firstElementChild.classList.add("active")
        carouselIndicators.lastElementChild.remove()
    }
    $('.carousel').carousel(carouselIndicators.childElementCount - 1)
});


/* Async submit request */
$("#item-details-form").submit(function (e) {

    e.preventDefault(); // avoid to execute the actual submit of the form.

    var form = $(this);
    var url = form.attr('action');

    $.ajax({
        type: "POST",
        url: url,
        data: form.serialize(), // serializes the form's elements.
        success: function (data) {
            $(".modal").modal("hide");
        }
    });
});

