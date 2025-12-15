import "./Profile.css"
import Menu from "../Menu/Menu";
import sha512 from "../Utils/Sha512";

function getUserData(userId) {
    return fetch(`/user?userId=${userId}`)
        .then(userData => {
            return userData.json()
        })
        .catch(error => {
            console.log("An error occured!")
        });
}

async function onButtonClick() {
    let login, email, pwd, repeat_pwd, message;
    const re_email = /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/;

    login = document.getElementById("login");
    email = document.getElementById("email");
    pwd = document.getElementById("pwd");
    repeat_pwd = document.getElementById("repeat-pwd");
    message = document.getElementById("message");

    message.textContent = "";

    if (login.value === "") {
        message.textContent = "Login is empty! ";
        message.color = "orange";
    }

    if (!(re_email.test(email.value))) {
        message.textContent = message.textContent + "Email is incorrect! ";
        message.color = "orange";
    }

    if (pwd.value === "") {
        message.textContent = message.textContent + "Password is empty! ";
        message.color = "red";
    }

    if (pwd.value.trim() !== repeat_pwd.value.trim()) {
        message.textContent = message.textContent + "Passwords doesn't match";
        message.color = "red";
    }

    const pwdHashed = await sha512(pwd.value);

    fetch(`/users?email=${email.value.trim()}&nickname=${login.value.trim()}&password=${pwdHashed}`, { 
        method: "POST",
        headers: {
            'Content-Type': 'application/json',
        } 
    })
    .then(response => {
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        return response.json(); 
    })
    .then(data => {
        console.log('Success:', data);
        if (data[0] !== "") {
            console.log(data[0]);
            console.log(typeof(data[0]));
            console.log(typeof("email"));
            let flag = true;
            if (data[0].includes("email")) {
                message.textContent = "The email is already taken! "
                message.color = "red";
                flag = false;
            } 
            if (data[0].includes("nickname")) {
                message.textContent = message.textContent + "The login is already taken!";
                message.color = "red";
                flag = false;
            }
            if (!flag) return;
        }
        message.textContent = "Registration successful!";
        message.style.color = "green";
        
        login.value = "";
        email.value = "";
        pwd.value = "";
        repeat_pwd.value = "";
    })
    .catch(error => {
        console.error('Error:', error);
        message.textContent = "Registration failed. Please try again.";
        message.color = "red";
    });
}

async function Profile() {
    let userInfo = await getUserData(localStorage.getItem("userId"));
    let nickname = "";
    let email = ""

    if (userInfo != []) {
        nickname = userInfo.nickname;
        email = userInfo.email;
    }


    return (
        <>
            <header class="header">
                <h1 class="header-h1">Profile</h1>
            </header>
            <Menu />
            <div className="signin-form">
                <p class="input-name">Nickname</p>
                <input type="text" id="login" autoComplete="off" value={nickname} required></input>

                <p class="input-name">Email</p>
                <input type="text" id="email" autoComplete="off" value={email} required></input>

                <button id="verify" onClick={onButtonClick}>Change Info</button>
                <p id="message"></p>
            </div>
        </>
    );
};

export default Profile;    