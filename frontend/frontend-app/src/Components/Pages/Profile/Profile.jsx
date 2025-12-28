import "./Profile.css"
import Menu from "../Menu/Menu";

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

function getUserData(userId) {
    return fetch(`/user?userId=${userId}`)
        .then(userData => {
            return userData.json()
        })
        .catch(error => {
            console.log("An error occured!")
        });
}

function onButtonClick() {
    let login, email, message;
    const re_email = /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/;

    login = document.getElementById("login");
    email = document.getElementById("email");
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


    return fetch(`/users?userId=${localStorage.getItem("userId")}&email=${email.value.trim()}&nickname=${login.value.trim()}`, {
        method: "PATCH",
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
                console.log(typeof (data[0]));
                console.log(typeof ("email"));
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

            window.location.reload();
        })
        .catch(error => {
            console.error('Error:', error);
            message.textContent = "Registration failed. Please try again.";
            message.color = "red";
        });
}

function Profile() {
    console.log(localStorage.getItem("userId"));
    var nickname, email;
    getUserData(localStorage.getItem("userId"))
        .then(userInfo => {
            console.log(`userInfo: ${userInfo}`);
            email = userInfo.email;

            nickname = userInfo.nickname;
            console.log(`User nickname: ${nickname}`);
            console.log(`User email: ${email}`);

            document.getElementById("login").value = nickname;
            document.getElementById("email").value = email;
        
        });
    checkAuthorization().then(isAuth => {
        if (!isAuth) {
            console.log("No auth.");
            window.location.href = "/signin";
        }
    });
    return (
        <>
            <header class="header">
                <h1 class="header-h1">Profile</h1>
            </header>
            <Menu />
            <div className="signin-form">
                <p class="input-name">Nickname</p>
                <input type="text" id="login" required></input>

                <p class="input-name">Email</p>
                <input type="text" id="email" required></input>

                <button id="verify" onClick={onButtonClick}>Change Info</button>
                <p id="message"></p>    
            </div>
        </>
    );
};

export default Profile;    
