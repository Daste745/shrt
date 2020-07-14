const labels = document.querySelectorAll("label");

function checkActive(inputField, label) {
    if (inputField.value.length > 0) {
        label.classList.add("label-active");
    } else {
        label.classList.remove("label-active");
    }
}

for (let label of labels) {
    let labelFor = label.getAttribute("for");
    const inputField = document.querySelector(`#${labelFor}`);

    inputField.setAttribute("autocomplete", "off")

    checkActive(inputField, label);
    inputField.addEventListener("keyup", () => {
        checkActive(inputField, label);
    });
}

// Assign a maxlength attribute to the "key" field
document.querySelector("#key")
    .setAttribute("maxlength", "16");

cretedUrlField = document.querySelector(".created-url");
if (cretedUrlField) {
    cretedUrlField.addEventListener("click", () => {
        navigator.clipboard.writeText(cretedUrlField.textContent);
        // TODO: Show popup message "copied to clipboard"
    });
}

// TODO: Clean this script up
