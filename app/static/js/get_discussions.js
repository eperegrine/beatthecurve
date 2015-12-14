
function getDiscussions(lectureId, options, callback) {
    var request = $.ajax("/notes/get-discussions/" + lectureId);
    request.done(function (data) {
        callback(options, data);
    });
}

function addNoteSelectFields(options, data) {
    var selectFieldId = "#" + options['selectFieldId'];
    $(selectFieldId).empty();
    console.log(data);
    if (Object.keys(data).length == 0) {
        $(selectFieldId).prop('disabled', true);
        var option = "<option value='-1'>No Discussions</option>";
        $(selectFieldId).append(option)

    } else {
        $(selectFieldId).prop('disabled', false);
    }
    for (var key in data) {
      if (data.hasOwnProperty(key)) {
        var option = "<option value='" + key + "'>" + data[key] + "</option>";
        $(selectFieldId).append(option);

      }
    }
    $(selectFieldId).material_select();
}

function addQuestionDiscussionSelectFieldUpdate(options, data) {
    $("#discussion").empty();
    if (Object.keys(data).length == 0) {
        $("#discussion").prop('disabled', true);
        var option = "<option value='-1'>No Discussions</option>";
        $("#discussion").append(option)
    } else {
        $("#discussion").prop('disabled', false);
        for (var key in data) {
          if (data.hasOwnProperty(key)) {
            var option = "<option value='" + key + "'>" + data[key] + "</option>";
            $("#discussion").append(option);

          }
        }
        var option = "<option value='-1'>N/A</option>";
        $("#discussion").append(option);
    }
    $('select').material_select();

}

