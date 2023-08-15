$(function () {
    console.log("JQ is ready to work");

    // CSRF token:
    const CSRF = $("input[name=csrfmiddlewaretoken]").val()
    // -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --

    // delete one attachment
    // -- -- -- -- -- -- --
    $(".btn-archive-eraser").click(function (e) { 
        e.preventDefault();
        const archiveListElement = $(this).attr("data-jq-archive-target");
        const delUrl = $(this).attr("href");
        $.ajax({
            type: "DELETE",
            url: delUrl,
            headers: {
                "X-CSRFToken":CSRF,
                "Content-Type":"application/json"
            },
            // beforeSend: function(xhr) {
            //     xhr.setRequestHeader("X-CSRFToken", csrf);
            // },
            success: function (data, textStatus, jqXHR) {
                console.log(jqXHR.status);
                $(archiveListElement).hide(1500);
            },
            error: function (data, textStatus, jqXHR) {
                console.log(jqXHR.status);
            }
        });
    });
    // change ticket state
    // -- -- -- -- -- -- --
    $("input[name=ticket-state]").click(function () { 
        console.log('Press');
        let resolved = false;
        let ticketStateUrl = $(this).attr("ticket-state-url")
        if ($(this).attr("ticket-state-switch") === "1") {
            $(this).attr("ticket-state-switch", "0");  // disable
        } else {
            resolved = true;
            $(this).attr("ticket-state-switch", "1");  // enable
        }
        $.ajax({
            type: "PATCH",
            url: ticketStateUrl,
            headers: {
                "X-CSRFToken":CSRF,
                "Content-Type":"application/json"
            },
            contentType: "application/json; charset=utf-8",
            dataType: "json",
            data: JSON.stringify({
                resolved: resolved,
            }),
            success: function (data, textStatus, jqXHR) {
                console.log(jqXHR.status)
            },
            error: function (data, textStatus, jqXHR) {
                console.log(data)
                console.log(jqXHR.status)
            }
        });
    });
    // delete ticket with attachments:
    // -- -- -- -- -- -- -- -- -- -- --
    $(".btn-ticket-del").click(function (e) {
        e.preventDefault(); 
        const delUrl = $(this).attr("href")
        const redirectUrl = $(this).attr("data-jq-ticket-del-redirect")
        const elementTarget = $(this).attr("data-jq-ticket-del-target")
        const delDiv = $(elementTarget)
        $.ajax({
            type: "DELETE",
            url: delUrl,
            headers: {
                'X-CSRFToken':CSRF,
                'Content-Type':'application/json'
            },
            success: function (data, textStatus, jqXHR) {
                console.log(jqXHR.status);
                if (delDiv.length) {
                    delDiv.hide(1500);
                } else {
                    window.location.href = redirectUrl;
                }
            },
            error: function (data, textStatus, jqXHR) {
                console.log(jqXHR.status);
            }
        });
    });
    // copy token to clipboard:
    // -- -- -- -- -- -- -- --
    $(".token-clipboard").click(function (e) { 
        e.preventDefault();
        const btn = $(this)
        const tokenInput = btn.siblings("input[name=ticket-token]").val();
        const icon = btn.children(":first").get(0)
        navigator.clipboard.writeText(tokenInput);
        btn.html('<i class="bi bi-check-lg"></i>')
        // Revert button label after 500 milliseconds
        setTimeout(function(){
            btn.html(icon);
        }, 500)
    });
});
