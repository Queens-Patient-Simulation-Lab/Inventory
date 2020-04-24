
function onSelectionChanged() {
    const selected = $("#userSelection option:selected").val();
    if (selected !== "") {
        target = "/reports/userHistory/?user=" + selected;
        $("#csvBtn").attr("href", target + "&format=csv");
        $("#pdfBtn").attr("href", target + "&format=pdf");
        $.get(target, (data) => {
            $("#historyTableBody").empty().append(data);
            const today =  new Date();
            $("#generatedDate").text(today.getFullYear() + "-" + (today.getMonth()+1) + "-" + today.getDate());
            $(".initially-hidden").removeClass("initially-hidden");
        });

    }
}

onSelectionChanged();
$("#userSelection").change(onSelectionChanged);