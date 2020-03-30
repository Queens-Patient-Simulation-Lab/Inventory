$(".deleteBtn").click(function () {
    locationUrl = $(this).closest("tr").attr("data-attr-value")
    var csrftoken = jQuery("[name=csrfmiddlewaretoken]").val();

    $.ajax({
        type: "DELETE",
        url: locationUrl,
        beforeSend: function(xhr) {
        xhr.setRequestHeader("X-CSRFToken", csrftoken);
    },
        complete: function (msg) {
            location.reload()
        }
    });
})
$(".editBtn").click(function () {
    locationElem = $(this).closest("tr")
    modalElem = $("#changeLocationModal")

    locationId = locationElem.attr("id")
    locationName = locationElem.find("#locationName").text()
    locationDescription= locationElem.find("#locationDescription").text()


    modalElem.find("#modalLocationId").val(locationId)
    modalElem.find("#modalName").val(locationName)
    modalElem.find("#modalDescription").val(locationDescription)
})