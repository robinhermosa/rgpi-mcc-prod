$(document).ready(function () {
  // var ShowForm = function () {
  //   var btn = $(this);
  //   $.ajax({
  //     url: btn.attr("data-url"),
  //     type: 'get',
  //     dataType: 'json',
  //     beforeSend: function () {
  //       $('#modal-book').modal('show');
  //     },
  //     success: function (data) {
  //       $('#modal-book .modal-content').html(data.html_form);
  //     }
  //   });
  // };

  var SaveForm = function () {
    var form = $(this);
    $.ajax({
      url: form.attr('data-url'),
      data: form.serialize(),
      type: form.attr('method'),
      success: function (data) {
          $('#user-edit .open-modal').html(data.context)
      }
    })
    return false;
  }
  //update
  $('#user-edit').on("submit", ".update-form", SaveForm)
});