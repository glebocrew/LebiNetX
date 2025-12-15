import "./SignIn.css";
import Menu from "../Menu/Menu";
import sha512 from "../Utils/Sha512";


async function authorize(login, pwd) {
    console.log(`/user?nickname=${login}&pwd=${pwd}`)
    return fetch(`/user?nickname=${login}&pwd=${pwd}`)
        .then(response => {
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            else {
                // console.log(response.json());
                return response.json();
            }
        })
        .then(data => {
            console.log('Data received:', data);
            console.log(login, pwd);
            console.log(`The declaration that data == null is ${data == null}`);
            if (data == null) {
                return 0;
            }
            else {
                // createJWT(data[])
                localStorage.setItem("userId", data.userId);
                localStorage.setItem("pwd", data.pwd);
                localStorage.setItem("createdAt", Date.now().toString());

                // if (new Date() - createdAt) / (1000 * 60 * 60) > 30

                console.log(data.userId, data.pwd);
                return 1;
            }
        })
        .catch(error => {
            console.error('Error fetching data:', error);
        });
};

function onButtonClick() {
    console.log("Clicked check info!")
    let login = document.getElementById("login").value.trim();
    let pwd = document.getElementById("pwd").value.trim();

    if (login === "" || pwd === "") return;

    if (!(login && pwd)) {
        console.log("Login and pwd not found!");
    }

    console.log(login, pwd);

    let message = document.getElementById("message");

    if (!message) {
        console.log("No message field found!");
    }

    sha512(pwd)
        .then(hashedPwd => {
            console.log("Hashed properly!");
            return authorize(login, hashedPwd);
        })
        .then(result => {
            if (message) {
                console.log(`Result: ${result}`)
                if (result) {
                    message.textContent = `Correct data!`;
                }
                else {
                    message.textContent = "Incorrect data!";
                }
            }
        })
        .catch(error => {
            console.log("An error occured! Full e:", error);
        });
};






function SignIn() {

    return (
        <>
            <header class="header">
                <h1 class="header-h1">Sign In</h1>
            </header>
            <Menu />
            <div className="signin-form">
                <p class="input-name">Nickname</p>
                <input type="text" id="login" autoComplete="off" required></input>
                
                <p class="input-name">Password</p>
                <input type="password" id="pwd" autoComplete="off" required></input>

                <button id="verify" onClick={onButtonClick}>Check Info</button>
                <p id="message"></p>
            </div>
        </>
    );
};

export default SignIn;    