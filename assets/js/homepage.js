$('#itemTable tr').click(function () {
    $.get($(this).attr('data-access-url'), (data) => { document.getElementById("modalContainer").innerHTML = data; });
});