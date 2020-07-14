// Assign a maxlength attribute to the "key" field
// Wtforms doesn't automatically add the maxlength attribute
document.querySelector("#key")
    .setAttribute("maxlength", "16");


function checkActive(inputField, label) {
    if (inputField.value.length > 0) {
        label.classList.add("label-active");
    } else {
        label.classList.remove("label-active");
    }
}

for (let label of document.querySelectorAll("label")) {
    const labelFor = label.getAttribute("for");
    const inputField = document.querySelector(`#${labelFor}`);

    inputField.setAttribute("autocomplete", "off")

    // Check once when loading the page in case of the inputs being already
    // full (form resubmittion)
    checkActive(inputField, label);

    inputField.addEventListener("keyup", () => {
        checkActive(inputField, label);
    });
}


cretedUrlField = document.querySelector(".created-url");
if (cretedUrlField) {
    cretedUrlField.addEventListener("click", () => {
        navigator.clipboard.writeText(cretedUrlField.textContent);
        // TODO: Show popup message "copied to clipboard"
    });
}
