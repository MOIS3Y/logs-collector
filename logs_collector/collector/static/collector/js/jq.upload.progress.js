import {updateStorageInfo, genAlertMessage} from "./helpers.js";

$(function () {
    // set global variables:
    const uploadForm = document.getElementById('upload_form');
    const inputFile = document.getElementById('id_file');
    const progressBar = document.getElementById('progress');
    const alertContainer = document.getElementById('alert');
    // get upload form:
    $("#upload_form").submit(function(e){
        e.preventDefault();
        // collect request data:
        let formData = new FormData(this);
        let uploadToken = formData.get("token")
        // generate the URL for token validation:
        let tokenStatusUrl = [
            progressBar.getAttribute('token-status-url'),
            uploadToken
        ].join('')
        // init upload file func:
        const uploadFile = () => {
            // toggle visible progress bar:
            const mediaData = inputFile.files[0];
            if(mediaData != null){
                progressBar.classList.remove("not-visible");
            }
            // upload file (chunk) xrh request:
            $.ajax({
                type: 'POST',
                url: progressBar.getAttribute("upload-url"),
                data: formData,
                dataType: 'json',
                xhr:function(){
                    const xhr = new window.XMLHttpRequest();
                    xhr.timeout = 3600000; // increase request timeout to 1 hour
                    xhr.upload.addEventListener('progress', e=>{
                        if(e.lengthComputable){
                            const percentProgress = (e.loaded/e.total)*100;
                            console.log(percentProgress);
                            progressBar.innerHTML = `
                            <div
                                class="progress-bar progress-bar-striped progress-bar-animated"
                                style="width: ${percentProgress}%"
                            >
                            </div>`
                        }
                    });
                    return xhr
                },
                // set auth method:
                beforeSend: function(xhr) {
                    if (uploadToken) {
                        xhr.setRequestHeader("Upload-Token", uploadToken);
                    }
                },
                success: function(data, textStatus, jqXHR){
                    alertContainer.innerHTML = genAlertMessage(
                        'The file has been successfully uploaded to the server. Thank you!',
                        'success',
                        'col-lg-6'
                    )
                    uploadForm.reset()
                    progressBar.classList.add('not-visible')
                    try {
                        updateStorageInfo();
                    } catch (error) {
                        console.log(error)
                    };
                },
                error: function(jqXHR, textStatus, errorThrown){
                    let errorMessage = "Unexpected error. Try again please"
                    if (jqXHR.status === 423 || jqXHR.status === 403) {
                        errorMessage = `Error ${jqXHR.status} <br> ${jqXHR.responseJSON.detail}`
                    }
                    if (jqXHR.status === 401) {
                        errorMessage = `Error ${jqXHR.status} <br> The token field cannot be empty`
                    }
                    if (jqXHR.status === 400) {
                        errorMessage = `Error ${jqXHR.status} <br> ${jqXHR.responseJSON.detail}`
                    }
                    alertContainer.innerHTML = genAlertMessage(
                        errorMessage,
                        'danger',
                        'col-lg-6'
                    )
                    progressBar.classList.add('not-visible')
                },
                cache: false,
                contentType: false,
                processData: false,
            });
        }
        // check token status and upload file if token valid:
        $.ajax({
            type: 'GET',
            url: tokenStatusUrl,
            dataType: "json",
            success: function (data, textStatus, jqXHR) {
                if (data.attempts === 0) {
                    alertContainer.innerHTML = genAlertMessage(
                        `Error 423 <br> Token: ${uploadToken} expired`,
                        'danger',
                        'col-lg-6'
                    );
                }
                else if (data.resolved === true) {
                    alertContainer.innerHTML = genAlertMessage(
                        `Error 423 <br> Ticket bound with token: ${uploadToken} <br> already resolved`,
                        'danger',
                        'col-lg-6'
                    );
                } else {
                    alertContainer.innerHTML = genAlertMessage(
                        `Token: ${uploadToken} is valid. <br> Starting to upload...`,
                        'success',
                        'col-lg-6'
                    );
                    uploadFile();
                };
            },
            error: function(jqXHR){
                if (jqXHR.responseJSON.detail) {
                    alertContainer.innerHTML = genAlertMessage(
                        `Error 403 <br> Token: ${uploadToken} is not valid`,
                        'danger',
                        'col-lg-6'
                    )
                } else {
                    alertContainer.innerHTML = genAlertMessage(
                        `Unexpected error. Try again please`,
                        'danger',
                        'col-lg-6'
                    )
                }
            },
        });
    });
});
