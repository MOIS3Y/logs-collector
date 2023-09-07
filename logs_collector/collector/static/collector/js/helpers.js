// formatted byte size to human readable:
const sizify = (value) => {
    let ext = ''
    if (value < 512000) {
        value = value / 1024.0
        ext = 'KB'
    } else if (value < 4194304000) {
        value = value / 1048576.0
        ext = 'MB'
    } else {
        value = value / 1073741824.0
        ext = 'GB'
    };
    return `${Math.round(value * 10) / 10} ${ext}`
};

// fix update bootstrap tooltip func:
const updateBsTooltip = (instance) => {
    let tt = bootstrap.Tooltip.getInstance(instance);
    tt.dispose();
    bootstrap.Tooltip.getOrCreateInstance(instance);
};

// update storage info widget:
const updateStorageInfo = () => {
    // set storage items vars:
    let storageIcon = $("#storage_icon")
    let storageProgressContainer = $("#storage_progress_container")
    let storage_progress = $("#storage_progress")
    // set API url:
    const storageUrl = storage_progress.attr("storage-url")
    $.ajax({
        type: "GET",
        url: storageUrl,
        headers: {
            "Content-Type":"application/json"
        },
        dataType: "json",
        success: function (data, textStatus, jqXHR) {
            // JSON answer:
            let storage = data.storage
            // set updated fields:
            let storageInfoNewFields = [
                `Total: ${sizify(storage.total)}`,
                '<br>',
                `Used: ${sizify(storage.used)}`,
                '<br>',
                `Free: ${sizify(storage.free)}`
            ].join('')
            // progress bar update:
            storage_progress.attr("style", `width:${storage.used_percent}%`)
            // progress bar color update:
            if (storage.used_percent > 90) {
                storage_progress.attr("class", "progress-bar bg-danger");
            } else if (storage.used_percent > 80) {
                storage_progress.attr("class", "progress-bar bg-warning");
            } else {
                storage_progress.attr("class", "progress-bar bg-success");
            };
            // tooltips update:
            storageIcon.attr("data-bs-title", `Storage used: ${storage.used_percent}%`)
            storageProgressContainer.attr("data-bs-title", storageInfoNewFields)
            updateBsTooltip(storageIcon)
            updateBsTooltip(storageProgressContainer)
        }
    });
};

export {sizify, updateBsTooltip, updateStorageInfo};
