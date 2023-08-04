$(function () {
    console.log("JQ is ready to work");
    // CSRF token:
    const CSRF = $("input[name=csrfmiddlewaretoken]").val()
    // -- -- -- --
    function deleteArchiveListElement(id) {
        const archiveList = `#li-archive-${id}`
        $(archiveList).hide(1500);
    };
    $(".btn-archive-eraser").click(function (e) { 
        e.preventDefault();
        const archiveListElement = $(this).attr("data-jq-archive-target");
        $.ajax({
            type: "delete",
            url: $(this).attr("href"),
            headers: {
                "X-CSRFToken":CSRF,
                "Content-Type":"application/json"
            },
            // beforeSend: function(xhr) {
            //     xhr.setRequestHeader("X-CSRFToken", csrf);
            // },
            success: function (response) {
                console.log(response.status);
                deleteArchiveListElement(archiveListElement);
            },
            error: function (response) {
                console.log(response.status);
            }
        });
    });
    $("#ticket-state").click(function () { 
        console.log('Press');
        let resolved = false;
        let ticket_state_url = $(this).attr("ticket-state-url")
        if ($(this).attr("ticket-state-switch") === "1") {
            console.log('Find it!!!')
            resolved = true;
            $(this).attr("ticket-state-switch", "0");  // disable

        } else {
            resolved = false;
            $(this).attr("ticket-state-switch", "1");  // enable
        }
        console.log(resolved)
        $.ajax({
            type: "post",
            url: ticket_state_url,
            headers: {
                "X-CSRFToken":CSRF,
                "Content-Type":"application/json"
            },
            contentType: "application/json; charset=utf-8",
            dataType: "json",
            data: JSON.stringify({
                resolved: resolved,
            }),
            success: function (response) {
                console.log(response.resolved)
            },
            error: function (response) {
                console.log(response.resolved)
            }
        });
    });
    $(".btn-ticket-del").click(function (e) {
        e.preventDefault(); 
        const del_url = $(this).attr("href")
        const redirect_url = $(this).attr("data-jq-ticket-del-redirect")
        $.ajax({
            type: "DELETE",
            url: del_url,
            headers: {
                'X-CSRFToken':CSRF,
                'Content-Type':'application/json'
            },
            success: function (response) {
                console.log(response.status);
                if (redirect_url) {
                    window.location.href = redirect_url;
                }else {
                    console.log("Need delete ticket card");
                }
            },
            error: function (response) {
                console.log(response.status);
            }
        });
    });
});
