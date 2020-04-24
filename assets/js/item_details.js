import 'bootstrap4-tagsinput/tagsinput'


const deletedImageIdsSet = new Set()
const uploadedImages = []

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

// https://stackoverflow.com/a/6658774/5619385
// since .delete-img-btn is dynamically generated, $(".delete-img-btn").click will not bind to new elements
$("#itemImageCarousel").on("click", ".delete-img-btn", function () {
    let carousel = document.getElementById("itemImageCarousel")
    let carouselIndicators = carousel.getElementsByClassName('carousel-indicators')[0]
    let carouselInner = carousel.getElementsByClassName("carousel-inner")[0]

    let deleteDiv = $(this).parent()
    let img = deleteDiv.find("img")[0]


    let imageId = $(this).attr("data-item-id")
    if (imageId != null && imageId != -1) {
        // This image came from the server
        deletedImageIdsSet.add(imageId)
    } else {
        let itemIndex = uploadedImages.indexOf(img.src)
        if (itemIndex != -1) {
            uploadedImages.splice( itemIndex, 1 )
        }
    }

    let childCount = carouselInner.childElementCount
    if (childCount > 1) {
        // The new active card should be the next card (first if there is no next card)
        let newActiveIndex = (deleteDiv.index() + 1) % (childCount);


        $('.carousel').one('slid.bs.carousel', function () {
            // Fires when the carousel has completed sliding the first time
            // Note that the event listener is one(), not on()
            deleteDiv.remove()
            carouselIndicators.lastElementChild.remove()
        })

        $('.carousel').carousel(newActiveIndex);
    } else {
        let defaultSrc = carouselInner.getAttribute("data-default-url")
        let img = deleteDiv.find("img")[0]
        deleteDiv.addClass("empty-item")
        img.src = defaultSrc;
    }


});


$("#add-image-input").change(function (e) {
    let carousel = document.getElementById("itemImageCarousel")
    let carouselIndicators = carousel.getElementsByClassName('carousel-indicators')[0]
    let carouselInner = carousel.getElementsByClassName("carousel-inner")[0]

    let firstImgDiv = carouselInner.firstElementChild
    let firstIsEmpty = false
    if (firstImgDiv.classList.contains("empty-item")) {
        firstIsEmpty = true
        firstImgDiv.classList.remove("empty-item")
    }

    for (var i = 0; i < e.target.files.length; i++) {

        var file = e.target.files[i];

        console.log("File was uploaded")

        let newIndicator = carouselIndicators.firstElementChild.cloneNode(true)
        newIndicator.classList.remove("active")

        newIndicator.setAttribute("data-slide-to", carouselIndicators.childElementCount)
        carouselIndicators.appendChild(newIndicator)


        // Add new image
        let newImageDiv = firstImgDiv.cloneNode(true)
        newImageDiv.classList.remove("active")
        newImageDiv.getElementsByClassName("delete-img-btn")[0].setAttribute("data-item-id", -1)

        let image = newImageDiv.getElementsByClassName("carousel-image")[0]
        let reader = new FileReader();
        reader.onloadend = function () {
            uploadedImages.push(reader.result)
            image.src = reader.result;
        }
        reader.readAsDataURL(file);
        carouselInner.appendChild(newImageDiv)

    }
    if (firstIsEmpty) {
        firstImgDiv.remove()
        carouselInner.firstElementChild.classList.add("active")
        carouselIndicators.lastElementChild.remove()
    }
    $('.carousel').carousel(carouselIndicators.childElementCount - 1)
});


/* Async submit request */
$("#item-details-form").submit(function (e) {

    e.preventDefault(); // avoid to execute the actual submit of the form.

    let form = $(this);
    let url = form.attr('action');
    let data = new FormData(form[0]);

    // Sets can't be turned to JSON well to convert to Array first
    data.append("deletedImageIds", JSON.stringify(Array.from(deletedImageIdsSet)))
    data.append("uploadedImages", JSON.stringify(uploadedImages))


    $.ajax({
        type: "POST",
        url: url,
        enctype: 'multipart/form-data',
        processData: false,
        contentType: false,
        data: data,
        success: function (data) {
            $(".modal").modal("hide");
        }
    });
});

