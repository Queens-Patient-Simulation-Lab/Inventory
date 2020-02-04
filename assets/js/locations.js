$(".deleteBtn").click(function () {
    locationId = $(this).closest("tr").attr("id")
    $.ajax({
        type: "DELETE",
        url: "{% url 'location-list' %}" + locationId,
        headers: {"X-CSRFToken": "{{ csrf_token }}"},
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