$(function () {
    function deleteArchiveListElement(id) {
        const archiveList = `#li-archive-${id}`
        $(archiveList).remove()
    }
    $(".btn-archive-eraser").click(function (e) { 
        e.preventDefault();
        const csrf = $("input[name=csrfmiddlewaretoken]").val()
        console.log(csrf)
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
                console.log(response)
                deleteArchiveListElement(archiveListElement);
            },
            error: function (response) {
                console.log(response)
            }
        });
    });
    console.log("JQ is ready to work");
});
