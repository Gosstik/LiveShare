import Cookies from "js-cookie";
import { ENV } from "../config";

// import { toast } from 'react-toastify'; // Or your preferred notification library

const handleNetworkError = (taskName) => (error) => {
  console.log(`%cAPI call '${taskName}' failed: network error`, "color: red");
  Promise.reject(error);
};

const getResponseWithApiErrorHandling = (taskName) => async (response) => {
  if (response.ok) {
    return response.json();
  }

  const body = await response.json();

  console.groupCollapsed(
    `%cGET ${response.url} [${response.status}]`,
    "color: red"
  );

  console.log(`Task: ${taskName}`);
  console.log(`Status: ${response.status}`);
  console.log(`Date: ${new Date(Date.now()).toISOString()}`);
  console.log("response:", response);
  console.log("body:", body);

  console.groupEnd();

  return body;
};

////////////////////////////////////////////////////////////////////////////////

// Clients

function auxApiGetCall(api_path, task_name, headers = {}, credMode = "omit") {
  return fetch(`http://localhost:8000/${api_path}`, {
    method: "GET",
    headers,
    credentials: credMode,
  })
    .catch(handleNetworkError(task_name))
    .then(getResponseWithApiErrorHandling(task_name));
}

function auxApiPostCall(
  api_path,
  task_name,
  body,
  headers = {},
  credMode = "omit"
) {
  console.log(`!!! post body=${JSON.stringify(body)}`);
  return fetch(`http://localhost:8000/${api_path}`, {
    method: "POST",
    headers,
    body: JSON.stringify(body),
    credentials: credMode,
  })
    .catch(handleNetworkError(task_name))
    .then(getResponseWithApiErrorHandling(task_name));
}

export function apiGetPosts() {
  return auxApiGetCall("posts", "get all posts", {}, "include");
  // TODO: make errors probability on backend
  // return fetch("/api/posts")
  //   .catch(handleNetworkError("get posts"))
  //   .then(getResponseWithApiErrorHandling("get posts"));
  // return fetch("http://localhost:8000/posts")
  //   .catch(handleNetworkError("get posts"))
  //   .then(getResponseWithApiErrorHandling("get posts"));
}

export function apiGetPostComments(postId) {
  return auxApiGetCall(`comments/by-post/${postId}`, `comments for ${postId}`);
  // http://localhost:8000/comments/by-post/:postId
  // return fetch(`/api/comments/${postId}`)
  //   .catch(handleNetworkError(`comments for ${postId}`))
  //   .then(getResponseWithApiErrorHandling(`comments for ${postId}`));

  // return fetch(`http://localhost:8000/comments/by-post/${postId}`)
  //   .catch(handleNetworkError(`comments for ${postId}`))
  //   .then(getResponseWithApiErrorHandling(`comments for ${postId}`));
}

export function apiUpdateComment(body) {
  return auxApiPostCall(
    `comments/update-comment`,
    `update comment with comment_id=${body.comment_id}`,
    body
  );
}

export function apiUpdatePostLike(body) {
  return auxApiPostCall(
    `posts/update/like`,
    `update post like, post_id=${body.post_id}`,
    body,
    {},
    "include"
  );
}
