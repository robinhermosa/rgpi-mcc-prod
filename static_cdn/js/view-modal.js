function openProfile(){
    var modalDiv = $("#modal-div");

    $(".open-modal").on("click", function () {
        $.ajax({
            url: $(this).attr("data-url"),
            success: function (data) {
                modalDiv.html(data);
                $("#user-details").modal();
            }
        });
    });
}


$(document).ready(function () {
    var modalDiv2 = $("#modal-div2");

    $(".open-modal").on("click", function () {
        $.ajax({
            url: $(this).attr("data-url"),
            success: function (data) {
                modalDiv2.html(data);
                $("#user-edit").modal();
            }
        });
    });
})