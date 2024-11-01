
// Text area character count
try {
    document.querySelector("#post-text").addEventListener("keyup", () => {
        let counter = document.querySelector("#char-count");
        let text = document.querySelector("#post-text").value;

        counter.innerText = text.length;
    })
} catch { }

// Handles following and unfollowing
try {
    document.querySelector("#follow-btn").onclick = () => {

        const btn = document.querySelector("#follow-btn");

        const formData = new FormData();
        formData.append("btnText", btn.innerText);
        formData.append("username", btn.dataset.user);

        sendRequests("following", formData);
    }
} catch { }

// Handles posting
try {
    document.querySelector("#post-form").onsubmit = (e) => {
        e.preventDefault();
        const postText = document.querySelector("#post-text").value;
        const inputValue = document.querySelector("#submit-post").value;
        const id = document.querySelector("#edit-post-id").value;

        const formData = new FormData();
        formData.append("post-text", postText);

        if (inputValue === "Post") {
            sendRequests("create_post", formData);
        } else {
            formData.append("id", id)
            sendRequests("edit_post", formData);
        }
    }
} catch { }

// Handles liking and unliking
document.querySelectorAll(".like-post").forEach(a => {
    a.onclick = () => {
        const id = a.dataset.id;
        const linkTxt = a.dataset.text;

        const formData = new FormData();
        formData.append("link-txt", linkTxt)
        formData.append("id", id)

        sendRequests("likes", formData)
    }
})

// Handles sending of requests
async function sendRequests(url, formData) {
    const cookie = document.cookie.split("=");
    const csrftoken = cookie[1];

    await fetch(`/${url}`, {
        method: "POST",
        headers: { 'X-CSRFToken': csrftoken },
        mode: "same-origin",
        body: formData,
    })
        .then(res => res.json())
        .then(res => {
            if (url === "following") {
                handleFollowingUpdate(res)
            } else if (url === "create_post") {
                window.location.replace("/")
            } else if (url === "edit_post") {
                alert(res.response)
            } else if (url === "likes") {
                handleLikesUpdate(res)
            }
        })
        .catch(err => console.log(err))
}

// Handles liking and unliking without reloading the page
function handleLikesUpdate(res) {
    const like = document.querySelector(`#like-post${res.postID}`)
    const icon = document.querySelector(`#like-icon${res.postID}`)

    if (res.linkTxt === "like") {
        like.innerText = parseInt(like.innerText) + 1;
        like.dataset.text = "unlike";

        icon.classList.remove("fa-regular");
        icon.classList.add("fa-solid");
    } else {
        like.innerText = parseInt(like.innerText) - 1;
        like.dataset.text = "like";

        icon.classList.remove("fa-solid");
        icon.classList.add("fa-regular");
    }
}

// Handles updating the following and follwers count without reloading the page
function handleFollowingUpdate(res) {
    const followers = document.querySelector("#followers");
    const btn = document.querySelector("#follow-btn");

    if (res.btnText === "Follow") {
        followers.innerText = parseInt(followers.innerText) + 1;
        btn.innerText = "Unfollow"
    } else {
        followers.innerText = parseInt(followers.innerText) - 1;
        btn.innerText = "Follow"
    }
}