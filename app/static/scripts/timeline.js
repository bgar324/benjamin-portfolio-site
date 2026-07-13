const form = document.querySelector("#timeline-form");
const postsContainer = document.querySelector("#timeline-posts");
const postTemplate = document.querySelector("#timeline-post-template");
const postCount = document.querySelector("#post-count");
const formStatus = document.querySelector("#form-status");
const contentInput = document.querySelector("#timeline-content");
const characterCount = document.querySelector("#character-count");
const submitButton = form.querySelector("button[type='submit']");

let timelinePosts = [];

function initialsAvatar(name) {
    const initials = name
        .trim()
        .split(/\s+/)
        .slice(0, 2)
        .map((part) => part[0])
        .join("")
        .toUpperCase() || "?";

    const svg = `<svg xmlns="http://www.w3.org/2000/svg" width="96" height="96" viewBox="0 0 96 96"><rect width="96" height="96" rx="48" fill="#d8e5ff"/><text x="48" y="54" text-anchor="middle" dominant-baseline="middle" fill="#163b73" font-family="Georgia,serif" font-size="34" font-weight="700">${initials}</text></svg>`;
    return `data:image/svg+xml;charset=UTF-8,${encodeURIComponent(svg)}`;
}

async function gravatarUrl(email, name) {
    if (!window.crypto?.subtle) {
        return initialsAvatar(name);
    }

    const normalizedEmail = email.trim().toLowerCase();
    const bytes = new TextEncoder().encode(normalizedEmail);
    const digest = await window.crypto.subtle.digest("SHA-256", bytes);
    const hash = Array.from(new Uint8Array(digest), (byte) => byte.toString(16).padStart(2, "0")).join("");

    return `https://www.gravatar.com/avatar/${hash}?s=96&d=identicon&r=g`;
}

function formatTimestamp(timestamp) {
    const date = new Date(timestamp);
    if (Number.isNaN(date.getTime())) {
        return { label: "Just now", iso: "" };
    }

    return {
        label: new Intl.DateTimeFormat(undefined, {
            month: "short",
            day: "numeric",
            year: "numeric",
            hour: "numeric",
            minute: "2-digit",
        }).format(date),
        iso: date.toISOString(),
    };
}

async function createPostElement(post, index) {
    const fragment = postTemplate.content.cloneNode(true);
    const card = fragment.querySelector(".dispatch-card");
    const avatar = fragment.querySelector(".dispatch-avatar");
    const author = fragment.querySelector(".dispatch-author");
    const time = fragment.querySelector(".dispatch-time");
    const content = fragment.querySelector(".dispatch-content");
    const formattedTime = formatTimestamp(post.created_at);

    card.style.setProperty("--dispatch-index", Math.min(index, 8));
    author.textContent = post.name;
    content.textContent = post.content;
    time.textContent = formattedTime.label;
    if (formattedTime.iso) time.dateTime = formattedTime.iso;

    avatar.alt = `${post.name}'s avatar`;
    avatar.src = await gravatarUrl(post.email, post.name);
    avatar.addEventListener("error", () => {
        avatar.src = initialsAvatar(post.name);
    }, { once: true });

    return fragment;
}

async function renderPosts() {
    postsContainer.setAttribute("aria-busy", "true");

    if (timelinePosts.length === 0) {
        postsContainer.innerHTML = `
            <div class="timeline-empty">
                <span aria-hidden="true">◇</span>
                <h4>The timeline is wide open.</h4>
                <p>Be the first person to leave a dispatch.</p>
            </div>`;
        postCount.textContent = "0 posts";
        postsContainer.setAttribute("aria-busy", "false");
        return;
    }

    const postElements = await Promise.all(timelinePosts.map(createPostElement));
    postsContainer.replaceChildren(...postElements);
    postCount.textContent = `${timelinePosts.length} ${timelinePosts.length === 1 ? "post" : "posts"}`;
    postsContainer.setAttribute("aria-busy", "false");
}

async function loadPosts() {
    try {
        const response = await fetch(form.action, { headers: { Accept: "application/json" } });
        if (!response.ok) throw new Error("Could not load the timeline.");

        const data = await response.json();
        timelinePosts = data.timeline_posts || [];
        await renderPosts();
    } catch (error) {
        postsContainer.innerHTML = `
            <div class="timeline-error" role="alert">
                <span aria-hidden="true">!</span>
                <div><h4>The timeline is taking a breather.</h4><p>${error.message}</p></div>
            </div>`;
        postCount.textContent = "Unavailable";
        postsContainer.setAttribute("aria-busy", "false");
    }
}

contentInput.addEventListener("input", () => {
    characterCount.textContent = `${contentInput.value.length} / 1000`;
});

form.addEventListener("submit", async (event) => {
    event.preventDefault();
    if (!form.reportValidity()) return;

    submitButton.disabled = true;
    submitButton.querySelector("span:first-child").textContent = "Publishing…";
    formStatus.className = "form-status";
    formStatus.textContent = "";

    try {
        const response = await fetch(form.action, {
            method: "POST",
            body: new FormData(form),
            headers: { Accept: "application/json" },
        });

        if (!response.ok) throw new Error("Your dispatch could not be published. Please try again.");

        const newPost = await response.json();
        timelinePosts = [newPost, ...timelinePosts.filter((post) => post.id !== newPost.id)];
        await renderPosts();
        form.reset();
        characterCount.textContent = "0 / 1000";
        formStatus.className = "form-status success";
        formStatus.textContent = "Your dispatch is live.";
        postsContainer.querySelector(".dispatch-card")?.scrollIntoView({ behavior: "smooth", block: "nearest" });
    } catch (error) {
        formStatus.className = "form-status error";
        formStatus.textContent = error.message;
    } finally {
        submitButton.disabled = false;
        submitButton.querySelector("span:first-child").textContent = "Publish dispatch";
    }
});

loadPosts();
