import "./Posts.css"
import Menu from "../Menu/Menu";
import { useEffect, useRef } from "react";

function deletePost(postId){
    return fetch(`/posts?postId=${postId}`, {
        "method": "DELETE"
    })
        .then(response => {
            if (!response.ok) {
                console.log("The response code is not 200!");
                return null;
            }
            else {
                console.log(response)
                return response.json();
            }
        })
        .catch(error => {
            console.log("An error occured!");
            return null;
        });
}

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
function getPosts() {
    return fetch(`/posts`)
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


function Posts() {
    const hasFetchedRef = useRef(false);
    console.log(`Registration checked: result - ${checkAuthorization()}`);

    useEffect(() => {
        const checkAuth = async () => {
            if (!(await checkAuthorization())) {
                console.log("No auth.");
                window.location.href = "/signin";
            }


            if (hasFetchedRef.current) return;
            hasFetchedRef.current = true;
            const postsContainer = document.getElementById("postsContainer");

            const currentUserId = localStorage.getItem("userId");
            getPosts()
                .then(posts => {
                    const sortedPosts = posts.sort((a, b) => 
                    b.userId === currentUserId ? 1 : a.userId === currentUserId ? -1 : 0);
                    if (posts === 0 || posts === 0) {
                        let p = document.createElement("p");
                        p.textContent = "No Posts"
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
                            post.onclick = () => { window.location.href = `/post/${posts[i].postId}`; };

                            if (posts[i].userId === localStorage.getItem("userId")) {
                                let deletePostButton = document.createElement("button");
                                deletePostButton.className = "delete-post-button";
                                deletePostButton.textContent = "Delete Post";
                                deletePostButton.onclick = () => deletePost(posts[i].postId);
                                post.appendChild(deletePostButton);
                            }

                            postsContainer.appendChild(post);
                        }
                    }
                });
        };
        checkAuth();
    }, []);

    return (
        <>
            <header class="header">
                <h1 class="header-h1">Posts</h1>
            </header>
            <Menu />
            <div class="posts" id="postsContainer">
            </div>
        </>
    );
};

export default Posts;