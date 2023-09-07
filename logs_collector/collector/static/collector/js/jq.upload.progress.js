import {updateStorageInfo} from "./helpers.js";

$(function () {
    const uploadForm = document.getElementById('upload_form');
    const input_file = document.getElementById('id_file');
    const progress_bar = document.getElementById('progress');
    const alert_container = document.getElementById('alert');
    
    $("#upload_form").submit(function(e){
        e.preventDefault();
        // $form = $(this)
        let formData = new FormData(this);
        let upload_token = formData.get("token")
        const media_data = input_file.files[0];
        if(media_data != null){
            progress_bar.classList.remove("not-visible");
        }
        $.ajax({
            type: 'POST',
            url: progress_bar.getAttribute("upload-url"),
            data: formData,
            dataType: 'json',
            xhr:function(){
                const xhr = new window.XMLHttpRequest();
                xhr.timeout = 3600000; // increase request timeout to 1 hour
                xhr.upload.addEventListener('progress', e=>{
                    if(e.lengthComputable){
                        const percentProgress = (e.loaded/e.total)*100;
                        console.log(percentProgress);
                        progress_bar.innerHTML = `
                        <div
                            class="progress-bar progress-bar-striped progress-bar-animated"
                            style="width: ${percentProgress}%"
                        >
                        </div>`
                    }
                });
                return xhr
            },
            beforeSend: function(xhr) {
                if (upload_token) {
                    xhr.setRequestHeader("Upload-Token", upload_token);
                }
            },
            success: function(data, textStatus, jqXHR){
                console.log(jqXHR.status);
                let type = "success";
                alert_container.innerHTML = [
                    `<div class="alert alert-${type} alert-dismissible col-lg-6" role="alert">`,
                    `   <div>The file has been successfully uploaded to the server. Thank you!</div>`,
                    '   <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>',
                    '</div>'
                ].join('')
                uploadForm.reset()
                progress_bar.classList.add('not-visible')
                try {
                    updateStorageInfo();
                } catch (error) {
                    console.log(error)
                };
            },
            error: function(jqXHR, textStatus, errorThrown){
                console.log(jqXHR);
                let type = "danger";
                let error_message = "Unexpected error. Try again please"
                if (jqXHR.status === 423) {
                    error_message = `Error ${jqXHR.status}: ${jqXHR.responseJSON.error}`
                }
                if (jqXHR.status === 403) {
                    error_message = `Error ${jqXHR.status}: ${jqXHR.responseJSON.error}`
                }
                if (jqXHR.status === 401) {
                    error_message = 'The token field cannot be empty'
                }
                alert_container.innerHTML = [
                    `<div class="alert alert-${type} alert-dismissible col-lg-6" role="alert">`,
                    `   <div>${error_message}</div>`,
                    '   <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>',
                    '</div>'
                ].join('')
                progress_bar.classList.add('not-visible')
            },
            cache: false,
            contentType: false,
            processData: false,
        });
    });
});
