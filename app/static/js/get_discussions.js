function getDiscussions(lectureId, selectFieldId) {
    var request = $.ajax("/notes/get-discussions/" + lectureId);
    request.done(function (data) {
        selectFieldId = "#" + selectFieldId;
        $(selectFieldId).empty();
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
    })
}
