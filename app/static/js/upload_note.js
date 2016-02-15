function upload_file(file, signed_request, url){
    var xhr = new XMLHttpRequest();
    xhr.open("PUT", signed_request);
    xhr.setRequestHeader('x-amz-acl', 'public-read');
    xhr.onload = function() {
        if (xhr.status === 200) {
            console.log('submitting');
            alert("Submitting!");
            undisableForm();
            document.createElement('form').submit.call(document.getElementById('add-note-form'));
            console.log('called again')
        }
    };

    xhr.onerror = function() {
        alert("Could not upload file.");
        $("#progress").remove()
        undisableForm();
    };
    xhr.send(file);
}
function get_signed_request(file){
    var xhr = new XMLHttpRequest();
    xhr.open("GET", "/notes/sign_s3?file_name="+file.name+"&file_type="+file.type);
    xhr.onreadystatechange = function(){
        if(xhr.readyState === 4){
            if(xhr.status === 200){
                var response = JSON.parse(xhr.responseText);
                $("#file_hash").val(response.file_hash);
                upload_file(file, response.signed_request, response.url);
            }
            else{
                alert("Could not get signed URL.");
                $("#progress").remove();
                undisableForm();
            }
        }
    };
    xhr.send();
}

$(document).ready(function() {
    $('#submit').on('click', function(e) {
        alert("Clicked");
        if ($('#add-note-form').attr('ajax-done') === 'true') {
            console.log('called');
            return true;
        } else {
            $('#add-note-form').attr({'ajax-done': 'true'});

            var files = document.getElementById("file").files;
            var file = files[0];
            if (file == null) {
                alert("No file selected.");
            }
            else {
                $("#description").parent().parent().append('<div class="progress" id="progress"><div class="indeterminate"></div></div>');
                disableForm();
                get_signed_request(file);
            }
        }
});
});

function disableForm() {
    $("#add-note-form").find('input, textarea, button, select').addClass("disabled");
    $("form > div .btn").addClass("disabled");
    alert("Disabled");
}

function undisableForm() {
    $("#add-note-form").find('input, textarea, button, select').removeClass("disabled");
    $("form > div .btn").removeClass("disabled")
}

