import "./SignIn.css"
import Menu from "../Menu/Menu";

function authorize(login, password) {
    fetch(`/user?login=${login}&password=${password}`)
        .then(response => {
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            if (response.json == null) {
                return 0;
            }
            else {
                return 1;
            }
        })
        .then(data => {
            console.log('Data received:', data);
        })
        .catch(error => {
            console.error('Error fetching data:', error);
        });
};

function verify() {
    const button = document.getElementById("verify");

}

function SignIn() {
    return (
        <>
            <header class="header">
                <h1 class="header-h1">Sign In</h1>
            </header>
            <Menu />
            <div class="login-form">
                <input type="text" id="login"></input>
                <input type="password" id="password"></input>

                <button id="verify">Check Info</button>
            </div>
        </>
    );
};

export default SignIn;    