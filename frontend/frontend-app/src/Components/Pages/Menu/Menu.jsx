import "./Menu.css"
import { useNavigate } from "react-router-dom";

function Menu() {
    const navigate = useNavigate();

    const redirectHome = () => navigate("/");
    const redirectSignIn = () => navigate("/signin");
    const redirectSignUp = () => navigate("/signup");
    const redirectPosts = () => navigate("/posts");
    const redirectNewPost = () => navigate("/newpost");
    const redirectProfile = () => navigate("/profile");

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
                <li class="menu-ul-li" onClick={ redirectPosts }>
                    <div class="menu-ul-li-content">
                        {/* <img 
                        class="menu-ul-li-container-icon"
                        alt="menu-ul-li-container-icon"></img> */}
                        <p class="menu-ul-li-container-text">
                            Posts
                        </p>
                    </div>
                </li>

                <li class="menu-ul-li" onClick={ redirectNewPost }>
                    <div class="menu-ul-li-content">
                        {/* <img 
                        class="menu-ul-li-container-icon"
                        alt="menu-ul-li-container-icon"></img> */}
                        <p class="menu-ul-li-container-text">
                            New Post
                        </p>
                    </div>
                </li>

                <li class="menu-ul-li" onClick={ redirectProfile }>
                    <div class="menu-ul-li-content">
                        {/* <img 
                        class="menu-ul-li-container-icon"
                        alt="menu-ul-li-container-icon"></img> */}
                        <p class="menu-ul-li-container-text">
                            Profile
                        </p>
                    </div>
                </li>
            </ul >
        </nav >
    );
};

export default Menu;
