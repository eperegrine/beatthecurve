function upload_file(file, signed_request, url){
    var xhr = new XMLHttpRequest();
    xhr.open("PUT", signed_request);
    xhr.setRequestHeader('x-amz-acl', 'public-read');
    xhr.onload = function() {
        if (xhr.status === 200) {
            console.log('submitting');
            alert("Submitting!");
            undisableForm();
            $("#progress").remove();
            document.createElement('form').submit.call(document.getElementById('add-exam-form'));
            console.log('called again')
        }
    };

    xhr.onerror = function() {
        undisableForm();
        $("#progress").remove();
        alert("Could not upload file.");
    };
    xhr.send(file);
}
function get_signed_request(file){
    var xhr = new XMLHttpRequest();
    xhr.open("GET", "/exams/sign_s3?file_name="+file.name+"&file_type="+file.type);
    xhr.onreadystatechange = function(){
        if(xhr.readyState === 4){
            if(xhr.status === 200){
                var response = JSON.parse(xhr.responseText);
                $("#file_hash").val(response.file_hash);
                upload_file(file, response.signed_request, response.url);
            }
            else{
                undisableForm();
                $("#progress").remove();
                alert("Could not get signed URL.");
            }
        }
    };
    xhr.send();
}

$(document).ready(function() {
    $('#submit').on('click', function(e) {
        if ($('#add-exam-form').attr('ajax-done') === 'true') {
            console.log('called');
            return true;
        } else {
            $('#add-exam-form').attr({'ajax-done': 'true'});

            var files = document.getElementById("file").files;
            var file = files[0];
            if (file == null) {
                alert("No file selected.");
            }
            else {
                disableForm();
                $("#average_grade").parent().append('<div class="progress" id="progress"><div class="indeterminate"></div></div>');
                get_signed_request(file);
            }
        }
});
});

function disableForm() {
    $("#add-exam-form").find('input, textarea, button, select').addClass("disabled");
    $("form > div .btn").addClass("disabled")
}

function undisableForm() {
    $("#add-exam-form").find('input, textarea, button, select').removeClass("disabled");
    $("form > div .btn").removeClass("disabled")
}
