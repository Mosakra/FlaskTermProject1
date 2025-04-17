addEventListener("DOMContentLoaded", () => {
    let form = document.querySelector("form");
    const titleInput = document.querySelector('input[name = "title"]');
    const yearInput = document.querySelector('input[name = "year"]');
    const fileInput = document.querySelector('input[name = "file"]');
    const allowedExtensions = ['.png', '.jpg'];

    form.addEventListener("submit", event => {
        let isValid = true;
        let errors = [];

        if (titleInput.value.trim() === "") {
            errors.push("Title is required.");
            isValid = false;
        }

        const platformInput = document.querySelector('input[name = "plat"]');
        if (platformInput.value.trim() === "") {
            errors.push("Platform is required.");
            isValid = false;
        }

        if (yearInput.value.trim() === "") {
            errors.push("Year is required.");
            isValid = false;
        } else if (isNaN(yearInput.value)) {
            errors.push("Year must be a number.");
            isValid = false;
        }

        if (fileInput.files.length > 0) {
            const fileName = fileInput.files[0].name.toLowerCase();
            const fileExtension = fileName.substring(fileName.lastIndexOf('.'));
            if (!allowedExtensions.includes(fileExtension)) {
                errors.push("Only .png and .jpg image files are supported.");
                isValid = false;
            }

        } else {
            errors.push("Please select an image file.");
            isValid = false;
        }

        if (!isValid) {
            event.preventDefault();
            alert(errors.join('\n'));
        }
    });
});
