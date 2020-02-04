$('#itemTable tr').click(function () {
    $("#modalContainer").load($(this).attr('data-access-url'));
});