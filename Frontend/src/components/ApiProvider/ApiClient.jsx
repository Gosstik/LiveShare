import Cookies, { get } from "js-cookie";
// import { toast } from 'react-toastify'; // Or your preferred notification library

import { ENV } from "../../config";
import { useAuth } from "../AuthProvider/AuthProvider";

////////////////////////////////////////////////////////////////////////////////

//// Utils

const handleNetworkError = (apiRequestName) => (error) => {
  console.log(
    `%cAPI call '${apiRequestName}' failed: network error`,
    "color: red"
  );
  Promise.reject(error);
};

const getResponseWithApiErrorHandling = (method) => async (response) => {
  if (response.ok) {
    return response;
  }

  if (response.status === 401) {
    // TODO: manually update token and repeat request

    // // Token is invalid or expired
    // this.authTokenProvider.clearToken();

    // // Notify the user
    // toast.error("Your session has expired. Please log in again.");

    // // Redirect to login page
    // window.location.href = "/signin";
    return;
  }

  const body = await response.json();

  console.groupCollapsed(
    `%c${method} ${response.url} [${response.status}]`,
    "color: red"
  );

  console.log(`Status: ${response.status}`);
  console.log(`Date: ${new Date(Date.now()).toISOString()}`);
  console.log("response:", response);
  console.log("body:", body);

  console.groupEnd();

  throw new Error(response);
};

function getContentTypeHeader(headers) {
  if (!headers || typeof headers !== "object") {
    return null;
  }

  // Convert all keys to lowercase for comparison
  const normalizedHeaders = Object.keys(headers).reduce((acc, key) => {
    acc[key.toLowerCase()] = headers[key];
    return acc;
  }, {});

  return normalizedHeaders["content-type"] || null;
}

const getUrlWithParams = (url, params) => {
  if (!params || Object.keys(params).length === 0) {
    return url;
  }
  const searchParams = new URLSearchParams();

  for (const [key, value] of Object.entries(params)) {
    searchParams.append(key, value);
  }

  return `${url}?${searchParams.toString()}`;
}

////////////////////////////////////////////////////////////////////////////////

//// ApiClient

class ApiClient {
  constructor(baseURL = ENV.BACKEND_BASE_URL) {
    this.baseURL = baseURL;
  }

  // Main request method
  async request(
    path,
    { method = "GET", body = null, headers = {}, options = {} }
  ) {
    // Prepare request options
    const requestOptions = {
      method,
      headers: {
        "X-CSRFToken": Cookies.get("csrftoken"),
        ...headers,
      },
      credentials: "include",
      ...options,
    };

    if (body && ["POST", "PUT", "PATCH"].includes(method)) {
      // TODO: handle form data
      // 'Content-Type': 'application/json',
      const contentType = getContentTypeHeader(headers);
      // TODO: remove that action and just set body ???
      if (contentType && contentType === "application/json") {
        requestOptions.body = JSON.stringify(body);
      } else {
        requestOptions.body = body;
      }
    }

    // Make request with error handling
    const requestUrl = `${this.baseURL}${path}`;
    const response = await fetch(requestUrl, requestOptions)
      .catch(handleNetworkError(`${method} ${requestUrl}`))
      .then(getResponseWithApiErrorHandling(method));

    // Returning response
    return response;
  }

  //////////////////////////////////////////////////////////////////////////////

  // HTTP method shortcuts

  async get(path, headers = {}) {
    return this.request(path, {
      method: "GET",
      headers,
    });
  }

  async post(path, { body = null, headers = {} } = {}) {
    return this.request(path, {
      method: "POST",
      body,
      headers,
    });
  }

  async put(path, { body, headers = {} }) {
    return this.request(path, {
      method: "PUT",
      body,
      headers,
    });
  }

  async patch(path, { body, headers = {} }) {
    return this.request(path, {
      method: "PATCH",
      body,
      headers,
    });
  }

  async delete(path, headers = {}) {
    return this.request(path, {
      method: "DELETE",
      headers,
    });
  }

  //////////////////////////////////////////////////////////////////////////////

  // Concrete API calls

  authLogout() {
    return this.post(`/auth/logout`);
  }

  authOAuthGoogleRedirect() {
    return this.get(`/auth/oauth/google/redirect`);
  }

  authPasswordSignIn({ email, password }) {
    return this.post(`/auth/password/signin`, {
      body: {
        email,
        password,
      },
      headers: {
        "Content-Type": "application/json",
      },
    });
  }

  authPasswordSignUp(body) {
    return this.post(`/auth/password/signup`, {
      body,
    });
  }

  //////////////////////////////////////////////////////////////////////////////

  // Comments

  commentsV1CommentPatch(commentId, body) {
    return this.patch(`/comments/v1/comment/${commentId}`, {
      body,
      headers: {
        "Content-Type": "application/json",
      },
    });
  }

  commentsV1CommentDelete(commentId) {
    return this.delete(`/comments/v1/comment/${commentId}`);
  }

  commentsV1CommentLike(commentId) {
    return this.post(`/comments/v1/comment/${commentId}/like`);
  }

  commentsV1CommentUnlike(commentId) {
    return this.post(`/comments/v1/comment/${commentId}/unlike`);
  }

  commentsV1CommentCreate(body) {
    return this.post(`/comments/v1/comment/create`, {
      body,
    });
  }

  commentsV1ForPost(postId, params) {
    const url = getUrlWithParams(`/comments/v1/for-post/${postId}`, params);
    return this.get(url);
  }

  //////////////////////////////////////////////////////////////////////////////

  // Posts

  postsV1ByFilters(params) {
    const url = getUrlWithParams(`/posts/v1/by-filters`, params);
    return this.get(url);
  }

  postsV1PostGet(postId) {
    return this.get(`/posts/v1/post/${postId}`);
  }

  postsV1PostPatch(postId, body) {
    return this.patch(`/posts/v1/post/${postId}`, {
      body,
    });
  }

  postsV1PostDelete(postId) {
    return this.delete(`/posts/v1/post/${postId}`);
  }

  postsV1PostLike(postId) {
    return this.post(`/posts/v1/post/${postId}/like`);
  }

  postsV1PostUnlike(postId) {
    return this.post(`/posts/v1/post/${postId}/unlike`);
  }

  postsV1PostCreate(body) {
    return this.post(`/posts/v1/post/create`, {
      body,
    });
  }

  //////////////////////////////////////////////////////////////////////////////

  // Users

  usersV1FriendsDelete(otherUserId) {
    return this.delete(`/users/v1/friends/${otherUserId}`)
  }

  usersV1FriendsInvitePost(otherUserId) {
    return this.post(`/users/v1/friends/invite/${otherUserId}`);
  }

  usersV1FriendsInviteDelete(otherUserId) {
    return this.delete(`/users/v1/friends/invite/${otherUserId}`);
  }

  usersV1FriendsInviteAccept(otherUserId) {
    return this.post(`/users/v1/friends/invite/accept/${otherUserId}`);
  }

  usersV1FriendsInviteReject(otherUserId) {
    return this.post(`/users/v1/friends/invite/reject/${otherUserId}`);
  }

  usersV1Search(params) {
    const url = getUrlWithParams(`/users/v1/search`, params);
    return this.get(url);
  }
}

export default ApiClient; // TODO: move to the end of file

////////////////////////////////////////////////////////////////////////////////

//// Legacy

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
