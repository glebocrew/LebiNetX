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
        console.log("Something went wrong while getting from local storage. ")
        return 0;
    }
}

function getPost(postId) {
    console.log(postId)
    console.log(`getPost(postId=${postId})`)
    return fetch(`/posts?postId=${postId}`)
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

function getComments(postId) {
    return fetch(`/comments?postId=${postId}`)
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

function deleteComment(commentId) {
    return fetch(`/comments?commentId=${commentId}`, {
        "method": "DELETE"
    })
        .then(response => {
            if (!response.ok) {
                console.log("The response code is not 200!");
                return null;
            }
            else {
                return response.json();
            }
        })
        .catch(error => {
            console.log("An error occured!");
            return null;
        });
}

function createComment(postId, content) {
    return fetch(`/comments?userId=${localStorage.getItem("userId")}&postId=${postId}&content=${content}`, {
        method: "POST",
        headers: {
            'Content-Type': 'application/json',
        }
    })
        .then(response => {
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            else {
                return response.json();
            }
        })
        .catch(error => {
            console.log("An error occured!");
            return null;
        });
}

function patchPost(postId, title, content) {
    return fetch(`/posts?postId=${postId}&title=${title}&content=${content}`, {
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
        .catch(error => {
            console.error('Error:', error);
            return null;
        });
}


function Post() {
    const hasFetchedRef = useRef(false);
    console.log(`Registration checked: result - ${checkAuthorization()}`);

    const { postId } = useParams();
    console.log(`Const postId: ${postId}`)

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
            getPost(postId)
                .then(posts => {
                    console.log(posts)
                    if (posts === 0) {
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

                            getPostHashTags(posts[i].postId).then(postHashTags => {
                                for (let h = 0; h < postHashTags.length; ++h) {
                                    let postHashTag = document.createElement("p");
                                    postHashTag.className = "hashtag";
                                    postHashTag.textContent = postHashTags[h].hashtag;
                                    hashtagsContainer.appendChild(postHashTag);
                                }
                            });

                            let postEditContainer = document.createElement("div");
                            postEditContainer.className = "post-edit";
                            if (posts[i].userId === localStorage.getItem("userId")) {
                                let editTitleInput = document.createElement("input");
                                editTitleInput.className = "edit-input";
                                editTitleInput.type = "text";
                                editTitleInput.value = posts[i].title;

                                let editContentInput = document.createElement("textarea");
                                editContentInput.className = "edit-textarea";
                                editContentInput.value = posts[i].content;

                                let editButton = document.createElement("button");
                                editButton.className = "edit-button";
                                editButton.textContent = "Edit Post";
                                editButton.onclick = async () => {
                                    await patchPost(posts[i].postId, editTitleInput.value.trim(), editContentInput.value.trim());
                                    postTitle.textContent = editTitleInput.value;
                                    postContent.textContent = editContentInput.value;
                                };

                                postEditContainer.appendChild(editTitleInput);
                                postEditContainer.appendChild(editContentInput);
                                postEditContainer.appendChild(editButton);
                            }

                            let commentsContainer = document.createElement("div");
                            commentsContainer.className = "comments";

                            let commentsTitle = document.createElement("h3");
                            commentsTitle.className = "comments-title";
                            commentsTitle.textContent = "Comments";
                            commentsContainer.appendChild(commentsTitle);

                            getComments(posts[i].postId).then(comments => {
                                if (comments === 0 || comments === undefined) {
                                    let p = document.createElement("p");
                                    p.textContent = "No comments yet";
                                    commentsContainer.appendChild(p);
                                }
                                else {
                                    for (let c = 0; c < comments.length; ++c) {
                                        let comment = document.createElement("div");
                                        comment.className = "comment";

                                        let commentUser = document.createElement("p");
                                        commentUser.className = "comment-user";
                                        commentUser.textContent = `User: ${comments[c].userId}`;
                                        getUserById(comments[c].userId).then(user => {
                                            if (user !== 0 && user !== undefined) {
                                                commentUser.textContent = `User: ${user.nickname}`;
                                            }
                                        });

                                        let commentContent = document.createElement("p");
                                        commentContent.className = "comment-content";
                                        commentContent.textContent = comments[c].content;

                                        if (comments[c].userId === localStorage.getItem("userId")) {
                                            let deleteCommentButton = document.createElement("button");
                                            deleteCommentButton.className = "delete-comment-button";
                                            deleteCommentButton.textContent = "Delete Comment";
                                            deleteCommentButton.onclick = async () => {
                                                await deleteComment(comments[c].commentId);
                                                comment.remove();
                                            };
                                            comment.appendChild(deleteCommentButton);
                                        }

                                        comment.appendChild(commentUser);
                                        comment.appendChild(commentContent);

                                        commentsContainer.appendChild(comment);
                                    }
                                }
                            });

                            let newCommentContainer = document.createElement("div");
                            newCommentContainer.className = "new-comment";

                            let newCommentInput = document.createElement("textarea");
                            newCommentInput.className = "new-comment-input";
                            newCommentInput.placeholder = "Write your comment";

                            let newCommentButton = document.createElement("button");
                            newCommentButton.className = "new-comment-button";
                            newCommentButton.textContent = "Add Comment";
                            newCommentButton.onclick = async () => {
                                if (newCommentInput.value.trim() === "") return;
                                await createComment(posts[i].postId, newCommentInput.value.trim());
                                newCommentInput.value = "";
                                commentsContainer.innerHTML = "";
                                let commentsTitleReload = document.createElement("h3");
                                commentsTitleReload.className = "comments-title";
                                commentsTitleReload.textContent = "Comments";
                                commentsContainer.appendChild(commentsTitleReload);
                                getComments(posts[i].postId).then(comments => {
                                    if (comments === 0 || comments === undefined) {
                                        let p = document.createElement("p");
                                        p.textContent = "No comments yet";
                                        commentsContainer.appendChild(p);
                                    }
                                    else {
                                        for (let c = 0; c < comments.length; ++c) {
                                            let comment = document.createElement("div");
                                            comment.className = "comment";

                                            let commentUser = document.createElement("p");
                                            commentUser.className = "comment-user";
                                            commentUser.textContent = `User: ${comments[c].userId}`;
                                            getUserById(comments[c].userId).then(user => {
                                                if (user !== 0 && user !== undefined) {
                                                    commentUser.textContent = `User: ${user.nickname}`;
                                                }
                                            });

                                            let commentContent = document.createElement("p");
                                            commentContent.className = "comment-content";
                                            commentContent.textContent = comments[c].content;

                                            if (comments[c].userId === localStorage.getItem("userId")) {
                                                let deleteCommentButton = document.createElement("button");
                                                deleteCommentButton.className = "delete-comment-button";
                                                deleteCommentButton.textContent = "Delete Comment";
                                                deleteCommentButton.onclick = async () => {
                                                    await deleteComment(comments[c].commentId);
                                                    comment.remove();
                                                };
                                                comment.appendChild(deleteCommentButton);
                                            }

                                            comment.appendChild(commentUser);
                                            comment.appendChild(commentContent);

                                            commentsContainer.appendChild(comment);
                                        }
                                    }
                                });
                            };

                            newCommentContainer.appendChild(newCommentInput);
                            newCommentContainer.appendChild(newCommentButton);

                            post.appendChild(postTitle);
                            post.appendChild(postContent);
                            post.appendChild(hashtagsContainer);
                            post.appendChild(postEditContainer);
                            post.appendChild(commentsContainer);
                            post.appendChild(newCommentContainer);
                            postsContainer.appendChild(post);
                        }
                    }
                });
        };
        checkAuth();
    }, [postId]);

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
