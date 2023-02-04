$(document).on("click", ".confirm-delete-button", function() {
  var taskId = $(this).data("task-id");
  $.ajax({
    url: "/delete-task",
    type: "DELETE",
    data: {
      taskId: taskId
    },
    success: function(data) {
      $("#task-" + taskId).remove();
      $("#delete-modal").modal("hide");
    }
  });
});
