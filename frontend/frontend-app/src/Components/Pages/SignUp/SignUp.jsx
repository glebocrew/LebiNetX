import "./SignUp.css"
import Menu from "../Menu/Menu";

function onButtonClick() {
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

    if (pwd.value !== repeat_pwd.value) {
        message.textContent = message.textContent + "Passwords doesn't match";
        message.color = "red";
    }

    fetch(`/users?email=${email.value}&nickname=${login.value}&password=${pwd.value}`, { 
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

function SignUp() {

    return (
        <>
            <header class="header">
                <h1 class="header-h1">Sign Up</h1>
            </header>
            <Menu />
            <div className="signin-form">
                <p class="input-name">Nickname</p>
                <input type="text" id="login" autoComplete="off" required></input>

                <p class="input-name">Email</p>
                <input type="text" id="email" autoComplete="off" required></input>

                <p class="input-name">Password</p>
                <input type="password" id="pwd" autoComplete="off" required></input>

                <p class="input-name">Repeat Password</p>
                <input type="password" id="repeat-pwd" autoComplete="off" required></input>


                <button id="verify" onClick={onButtonClick}>Check Info</button>
                <p id="message"></p>
            </div>
        </>
    );
};

export default SignUp;    