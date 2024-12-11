const uploadLock = "isUploading";
localStorage.setItem(uploadLock, false);

const errorHandler = (request) => (async (query, endpoint) => {
    try {
        return await request(query, endpoint);
    } catch (error) {
        if (error instanceof TypeError) {
            return {
                status: false,
                body: error.message
            };
        }
    }
});
  

const apiClient = errorHandler(async (data, endpoint) => {
    return await fetch(
        `/api/v1/${endpoint}`,
        {
            body: data,
            method: "POST"
        }
    ).then(async (res) => await res.json());
});

document.querySelector("#file")?.addEventListener("change", (event) => {
    const file = event.target.files[0];
    document.querySelector("#preview").src = URL.createObjectURL(file);
});

document.querySelector("#analyzer")?.addEventListener("submit", async (event) => {
    event.preventDefault();

    if (JSON.parse(localStorage.getItem(uploadLock))) {
        alert("Upload already in progress");
        return;
    }

    document.getElementById("loading").classList.remove("hidden");
    document.getElementById("success").classList.add("hidden");
    document.getElementById("failure").classList.add("hidden");

    localStorage.setItem(uploadLock, true);

    const data = new FormData(event.target);

    const { success, label, confidence, error } = await apiClient(data, "classify");
    document.getElementById("loading").classList.add("hidden");

    if (success) {
        document.querySelector("#result").innerText = label;
        document.querySelector("#confidence").innerText = `${(Number(confidence) * 100).toFixed(2)}%.`;
        document.getElementById("success").classList.remove("hidden");
    } else {
        document.querySelector("#error").innerText = error;
        document.getElementById("failure").classList.remove("hidden");
    }

    window.scrollTo(0, document.body.scrollHeight);
    localStorage.setItem(uploadLock, false);
});

document.querySelector("#refresh").addEventListener("click", () => {
    // Clear all the fields, forms and elements
    document.querySelector("#preview").src = "#";
    document.querySelector("#analyzer").reset();
    document.getElementById("failure").classList.add("hidden");
    document.getElementById("success").classList.add("hidden");
    document.getElementById("loading").classList.add("hidden");

    // Scroll to top
    window.scrollTo(0, 0);

    // Clear uploading status
    localStorage.setItem(uploadLock, false);
});