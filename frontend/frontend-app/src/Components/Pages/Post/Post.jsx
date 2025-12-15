import "./Post.css"
import Menu from "../Menu/Menu";
import { useEffect, useRef } from "react";
import { useParams } from "react-router-dom";

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
        now = new Date();

        console.log(`Now is ${now}`);
        console.log(`The auth createdAt: ${createdAt}`);
        console.log((now - createdAt) / (1000 * 60 * 60));

        if ((now - createdAt) / (1000 * 60 * 60) > 30) {
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
        console.log("Something went wrong while getting from local storage. ")
        return 0;
    }
}

function getPost(postId) {
    console.log(postId.postId)
    console.log(`getPost(postId=${postId.postId})`)
    return fetch(`/posts?postId=${postId.postId}`)
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
};

function getPostHashTags(postId) {
    return fetch(`/hashtags?postId=${postId}`)
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


function Post() {
    const hasFetchedRef = useRef(false);
    console.log(`Registration checked: result - ${checkAuthorization()}`);

    const { postId } = useParams();

    useEffect(() => {
        const checkAuth = async () => {
            if (!(await checkAuthorization())) {
                console.log("No auth.");
                window.location.href = "/signin";
            }


            if (hasFetchedRef.current) return;
            hasFetchedRef.current = true;
            const postsContainer = document.getElementById("postsContainer");
            console.log(`starting getPost(postId=${postId})`)
            getPost({ postId })
                .then(posts => {
                    if (posts === 0 || posts === 0) {
                        let p = document.createElement("p");
                        p.textContent = "Post not found"
                        postsContainer.appendChild(p);
                    }
                    else {
                        console.log(`Posts length is ${posts.length}`)
                        for (let i = 0; i < posts.length; ++i) {
                            console.log(posts[i]);
                            let post = document.createElement("div");
                            post.className = "post";

                            let postTitle = document.createElement("h1");
                            postTitle.className = "post-h1";
                            postTitle.textContent = posts[i].title;


                            let postContent = document.createElement("p");
                            postContent.className = "post-p";
                            postContent.textContent = posts[i].content;


                            let hashtagsContainer = document.createElement("div");
                            hashtagsContainer.className = "post-hashtags";

                            // Исправлена опечатка в цикле (было i вместо h)
                            getPostHashTags(posts[i].postId).then(postHashTags => {
                                for (let h = 0; h < postHashTags.length; ++h) {
                                    let postHashTag = document.createElement("p");
                                    postHashTag.className = "hashtag";
                                    postHashTag.textContent = postHashTags[h].hashtag;
                                    hashtagsContainer.appendChild(postHashTag);
                                }
                            });

                            post.appendChild(postTitle);
                            post.appendChild(postContent);
                            post.appendChild(hashtagsContainer);
                            postsContainer.appendChild(post);
                        }
                    }
                });
        };
        checkAuth();
    }, [[postId]]);

    return (
        <>
            <header class="header">
                <h1 class="header-h1">Post</h1>
            </header>
            <Menu />
            <div class="posts" id="postsContainer">
            </div>
        </>
    );
};

export default Post;