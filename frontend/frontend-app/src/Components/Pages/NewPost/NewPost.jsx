import "./NewPost.css"
import Menu from "../Menu/Menu";
import { useRef, useEffect } from "react";

function getUserById(userId) {
    return fetch(`/user?userId=${userId}`)
        .then(response => {
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            else {
                return response.json();
            }
        })
        .then(data => {
            // console.log('Data received:', data);
            // console.log(login, pwd);
            // console.log(`The declaration that data == null is ${data == null}`);
            if (data == null) {
                return 0;
            }
            else {
                return data;
            }
        })
        .catch(error => {
            console.error('Error fetching data:', error);
        });
}

async function checkAuthorization() {
    let userId, hashedPwd, createdAt, now;
    try {
        userId = localStorage.getItem("userId");
        console.log(`userId is ${userId}`);
        hashedPwd = localStorage.getItem("pwd");
        createdAt = localStorage.getItem("createdAt");

        createdAt = Number(createdAt);

        now = Date.now();

        console.log(`Now timestamp: ${now}`);
        console.log(`The auth createdAt: ${createdAt}`);
        console.log(`Difference in hours: ${(now - createdAt) / (1000 * 60 * 60)}`);

        if (isNaN(createdAt)) {
            console.log('createdAt is not a valid number');
            return 0;
        }

        if ((now - createdAt) / (1000 * 60 * 60) > 1) {
            localStorage.removeItem("userId");
            localStorage.removeItem("pwd");
            localStorage.removeItem("createdAt");
            return 0;
        }

        let user = await getUserById(userId);
        console.log(user);
        if (user !== 0) {
            console.log(`Pwd from LS: ${hashedPwd}`);
            console.log(`Pwd from DB: ${user.pwd}`);
            if (user.pwd === hashedPwd) {
                return 1;
            }
        }

        return 0;
    }
    catch {
        console.log("Something went wrong while getting from local storage.");
        return 0;
    }
}

async function onButtonClick() {
    let title, content, message;

    title = document.getElementById("title");
    content = document.getElementById("content");
    message = document.getElementById("message");

    if (title.value === "") {
        message.textContent = "Title is empty! ";
        message.color = "orange";
        return;
    }

    if (content.value === "") {
        message.textContent = message.textContent + "Content is empty! ";
        message.color = "red";
        return;
    }

    fetch(`/posts?userId=${localStorage.getItem("userId")}&title=${title.value.trim()}&content=${content.value.trim()}`, {
        method: "POST",
        headers: {
            'Content-Type': 'application/json',
        }
    })
        .then(response => {
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            window.location.href = "posts";
        })
        .catch(error => {
            console.error('Error:', error);
            message.textContent = "Registration failed. Please try again.";
            message.color = "red";
        });
}

function NewPost() {
    const hasFetchedRef = useRef(false);
    console.log(`Registration checked: result - ${checkAuthorization()}`);

    useEffect(() => {
        if (hasFetchedRef.current) return;
        hasFetchedRef.current = true;

        const checkAuth = async () => {
            if (!(await checkAuthorization())) {
                console.log("No auth.");
                window.location.href = "/signin";
            }
            if (hasFetchedRef.current) return;
            hasFetchedRef.current = true;
        };
        checkAuth();
    }, []);
    return (
        <>
            <header class="header">
                <h1 class="header-h1">Create New Post</h1>
            </header>
            <Menu />
            <div className="signin-form">
                <p class="input-name">Title</p>
                <input type="text" id="title" autoComplete="off" required></input>

                <p class="input-name">Content</p>
                <textarea type="textarea" class="input-textarea" id="content" autoComplete="off" required></textarea>

                <button id="verify" onClick={onButtonClick}>Check Info</button>
                <p id="message"></p>
            </div>
        </>
    );
};

export default NewPost;    