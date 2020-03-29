$('#itemTable tr').click(function () {
    $.get($(this).attr('data-access-url'), (data) => {
        // we can't just load the new content into the page with innerhtml because that won't execute scripts
        // we can't use jquery load because that would inline scripts breaking CSP
        // NOTE: this only working for scripts loaded with an src attribute and ignores all other attributes
        const div = document.createElement("div");
        div.innerHTML = data;
        $("#modalContainer").empty()[0].appendChild(div); // insert the content into the page, replacing any existing modal, scripts don't run
        const scripts = div.getElementsByTagName("script");
        let pairs = [];
        // can't do the insert inside the loop or it will run infinitely
        for (let script of scripts) {
            const newScript = document.createElement("script");
            newScript.src = script.src;
            pairs.push({ old: script, new: newScript });
        }
        for (let pair of pairs) {
            const parent = pair.old.parentNode;
            parent.insertBefore(pair.new, pair.old);
            parent.removeChild(pair.old);
        }
    });
});

$('#itemCreationButton').click(function () {
    $.get($(this).attr('data-access-url'), (data) => {
        // we can't just load the new content into the page with innerhtml because that won't execute scripts
        // we can't use jquery load because that would inline scripts breaking CSP
        // NOTE: this only working for scripts loaded with an src attribute and ignores all other attributes
        const div = document.createElement("div");
        div.innerHTML = data;
        // document.getElementById("modalContainer").appendChild(div); // insert the content into the page scripts don't run
        $("#modalContainer").empty()[0].appendChild(div); // insert the content into the page, replacing any existing modal, scripts don't run
        const scripts = div.getElementsByTagName("script");
        let pairs = [];
        // can't do the insert inside the loop or it will run infinitely
        for (let script of scripts) {
            const newScript = document.createElement("script");
            newScript.src = script.src;
            pairs.push({ old: script, new: newScript });
        }
        for (let pair of pairs) {
            const parent = pair.old.parentNode;
            parent.insertBefore(pair.new, pair.old);
            parent.removeChild(pair.old);
        }
    });
});