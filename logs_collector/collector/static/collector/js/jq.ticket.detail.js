$(function () {
    // CSRF token:
    const csrf = $("input[name=csrfmiddlewaretoken]").val()
    
    function deleteArchiveListElement(id) {
        const archiveList = `#li-archive-${id}`
        $(archiveList).hide(1500);
    }
    $(".btn-archive-eraser").click(function (e) { 
        e.preventDefault();
        const archiveListElement = $(this).attr("data-jq-archive-target");
        $.ajax({
            type: "delete",
            url: $(this).attr("href"),
            headers: {
                'X-CSRFToken':csrf,
                'Content-Type':'application/json'
            },
            // beforeSend: function(xhr) {
            //     xhr.setRequestHeader("X-CSRFToken", csrf);
            // },
            success: function (response) {
                console.log(response.status)
                deleteArchiveListElement(archiveListElement);
            },
            error: function (response) {
                console.log(response.status)
            }
        });
    });
    $("#ticket-state").click(function () { 
        console.log('Press');
        let resolved = false;
        if ($(this).attr("checked")) {
            console.log('Find it!!!')
            resolved = true;   
        } else {
            resolved = false;
        }
        $.ajax({
            type: "post",
            url: $(this).attr("ticket-state-url"),
            headers: {
                'X-CSRFToken':csrf,
                'Content-Type':'application/json'
            },
            contentType: 'application/json',
            dataType: 'json',
            data: JSON.stringify({
                "resolved": resolved
            }),
            success: function (response) {
                console.log(response.status)
            },
            error: function (response) {
                console.log(response.status)
            }
        });
    });
    console.log("JQ is ready to work");
});
