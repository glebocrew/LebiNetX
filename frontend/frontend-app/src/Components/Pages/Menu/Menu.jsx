import "./Menu.css"

function redirect(href) {
    window.location.href = href;
};

function Menu() {
    const redirectHome = () => redirect("/");
    const redirectSignIn = () => redirect("/signin");
    const redirectSignUp = () => redirect("/signup");

    return (
        <nav class="menu">
            <ul class="menu-ul">
                <li class="menu-ul-li" onClick={ redirectHome }>
                    <div class="menu-ul-li-content">
                        {/* <img 
                        class="menu-ul-li-container-icon"
                        alt="menu-ul-li-container-icon"
                        id="home"
                        ></img> */}
                        <p class="menu-ul-li-container-text">
                            Home
                        </p>
                    </div>
                </li>
                <li class="menu-ul-li" onClick={ redirectSignIn }>
                    <div class="menu-ul-li-content">
                        {/* <img 
                        class="menu-ul-li-container-icon"
                        alt="menu-ul-li-container-icon"></img> */}
                        <p class="menu-ul-li-container-text">
                            Sign In
                        </p>
                    </div>
                </li>
                <li class="menu-ul-li" onClick={ redirectSignUp }>
                    <div class="menu-ul-li-content">
                        {/* <img 
                        class="menu-ul-li-container-icon"
                        alt="menu-ul-li-container-icon"></img> */}
                        <p class="menu-ul-li-container-text">
                            Sign Up
                        </p>
                    </div>
                </li>
            </ul >
        </nav >
    );
};

export default Menu;