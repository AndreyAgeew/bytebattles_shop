document.getElementById("loginForm").addEventListener("submit", function (event) {
    event.preventDefault();

    const formData = new FormData(this);
    const formDataObject = {};
    formData.forEach((value, key) => {
        formDataObject[key] = value;
    });

    fetch("/pages/login", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify(formDataObject)
    })
        .then(response => response.json())
        .then(data => {
            console.log(data);
            // Handle the response as needed
        })
        .catch(error => {
            console.error(error);
        });
});