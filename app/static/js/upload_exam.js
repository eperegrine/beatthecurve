function upload_file(file, signed_request, url){
    var xhr = new XMLHttpRequest();
    xhr.open("PUT", signed_request);
    xhr.setRequestHeader('x-amz-acl', 'public-read');
    xhr.onload = function() {
        if (xhr.status === 200) {
            undisableForm();

            sweetAlert({
                title: "Finished!",
                text: "Your file was successfully uploaded",
                type: "success"
            }, function () {
                document.createElement('form').submit.call(document.getElementById('add-exam-form'));
                console.log('called again');
            });
        }
    };

    xhr.onerror = function() {
        sweetAlert("Error!", "Could not upload file", "error");
        $("#progress").remove();
        undisableForm();
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
                sweetAlert("Error!", "Could not get signed url", "error");
                $("#progress").remove();
                undisableForm();
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
            var files = document.getElementById("file").files;
            var file = files[0];
            if (file == null) {
                sweetAlert("No File", "Please select a file", "error");
            }
            else {
                sweetAlert({
                    title: "Upload File",
                    text: "Do you want to upload the file?",
                    type: "info",
                    showCancelButton: true,
                    closeOnConfirm: false,
                    showLoaderOnConfirm: true
                }, function() {
                    disableForm();
                    get_signed_request(file);
                    $('#add-exam-form').attr({'ajax-done': 'true'});
                });

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
