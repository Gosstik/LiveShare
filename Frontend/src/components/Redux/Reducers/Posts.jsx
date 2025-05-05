import { applyMiddleware, createSlice } from "@reduxjs/toolkit";
import { thunk as thunkMiddleware } from "redux-thunk";
import { composeWithDevTools } from "@redux-devtools/extension";

import { getSortedArray, likesLessSort, fieldLessSort } from "../../utils";

const composedEnhancer = composeWithDevTools(applyMiddleware(thunkMiddleware));

const getInnerPostById = (state, postId) =>
  state.posts.find((post) => post.postId === postId);

const initialState = {
  posts: [],
  areLoading: false,
  loaded: false,
  loadFailed: false, // TODO: add error handling in UI
};

const postsSlice = createSlice(
  {
    // TODO: send data to backend for all tasks
    name: "posts",
    initialState,
    reducers: {
      postsLoading(state, action) {
        const { loadingPosts } = action.payload;
        if (!state.loaded) {
          state.posts = loadingPosts;
          state.areLoading = true;
        }
      },
      postsLoaded(state, action) {
        const { postEls } = action.payload;
        state.posts = postEls;
        state.areLoading = false;
        state.loaded = true;
      },
      postsLoadFailed(state) {
        state.areLoading = false;
        state.loaded = false;
        state.loadFailed = true;
      },
      postFormUpdateSync(state, action) {
        const { postId, newText, newTitle } = action.payload;

        const post = getInnerPostById(state, postId);
        post.text = newText;
        post.title = newTitle;
      },
      postRemoveSync(state, action) {
        const { postId } = action.payload;

        state.posts = state.posts.filter((post) => post.postId !== postId);
      },
      postLikeSync(state, action) {
        const { postId, newIsLiked } = action.payload;

        const post = state.posts.find((post) => post.postId === postId);
        if (post.isLiked !== newIsLiked) {
          post.isLiked = newIsLiked;
          post.likes += newIsLiked ? 1 : -1;
        }
      },
      postUpdateCommentsCount(state, action) {
        const { postId, newCommentsCount } = action.payload;

        const post = getInnerPostById(state, postId);
        post.commentsCount = newCommentsCount;
      },
      postAdd(state, action) {
        // TODO: add apiClient
        // TODO: add UI
        // const { postId } = action.payload;
        // const post = {}
        // state.posts = [...state.posts, post];
        // TODO: send POST request to server
      },
      commentAdded() {
        // TODO: accept id from server
      },
    },
  },
  composedEnhancer
);

////////////////////////////////////////////////////////////////////////////////

// Middlewares

export function postsLoad(props) {
  const { apiClient } = props;
  delete props.apiClient;
  return async function thunk(dispatch, getState) {
    apiClient
      .postsV1ByFilters(props)
      .then(async (response) => {
        const body = await response.json();
        const postEls = Array.from(body.posts, (post) => ({
          postId: post.id,
          author: {
            id: post.author.id,
            email: post.author.email,
            firstName: post.author.firstName,
            lastName: post.author.lastName,
            displayedName: post.author.displayedName,
            profileIconUrl: post.author.profileIconUrl,
          },
          title: post.title,
          text: post.textContent,
          createdAt: post.createdAt,
          editedAt: post.editedAt,
          likes: post.likesCount,
          isLiked: post.isLikedByUser ?? false,
          commentsCount: post.commentsCount,
          attachedImageUrl: post.attachedImageUrl,
        }));
        dispatch(
          postsLoaded({
            postEls,
          })
        );
      })
      .catch(() => {
        dispatch(postsLoadFailed());
      });
  };
}

export function postFormUpdate(payload) {
  const { postId, newText, newTitle, apiClient } = payload;
  return async function thunk(dispatch, getState) {
    apiClient.postsV1PostPatch(postId, {
      title: newTitle,
      textContent: newText,
    });
    dispatch(
      postFormUpdateSync({
        postId, newText, newTitle,
      })
    );
  }
}

export function postRemove(payload) {
  const { postId, apiClient } = payload;
  return async function thunk(dispatch, getState) {
    apiClient.postsV1PostDelete(postId);
    dispatch(
      postRemoveSync({
        postId,
      })
    );
  }
}

export function postLike(payload) {
  const { postId, apiClient } = payload;
  return async function thunk(dispatch, getState) {
    const isLiked = selectPostIsLiked(postId)(getState());
    const newIsLiked = !isLiked;
    if (newIsLiked) {
      apiClient.postsV1PostLike(postId);
    } else {
      apiClient.postsV1PostUnlike(postId);
    }
    dispatch(
      postLikeSync({
        postId, newIsLiked,
      })
    );
  };
}

////////////////////////////////////////////////////////////////////////////////

// Selectors

const getPostById = (state, postId) =>
  state.posts.posts.find((post) => Number(post?.postId) === Number(postId));

export const selectPostEls = (state) => state.posts.posts;

export const selectPost = (postId) => (state) => getPostById(state, postId);

export const selectPostCommentsCount = (postId) => (state) =>
  getPostById(state, postId).commentsCount;

export const selectPostLikes = (postId) => (state) => {
  const post = getPostById(state, postId);
  return post.likes;
};

export const selectPostIsLiked = (postId) => (state) =>
  getPostById(state, postId).isLiked;

export const selectPostTitle = (postId) => (state) =>
  getPostById(state, postId).title;

export const selectPostText = (postId) => (state) =>
  getPostById(state, postId).text;

export const selectPostCreatedAt = (postId) => (state) =>
  getPostById(state, postId).createdAt;

export const selectPostsAreLoading = (state) => state.posts.areLoading;
export const selectPostsLoaded = (state) => state.posts.loaded;
export const selectPostsLoadFailed = (state) => state.posts.loadFailed;

////////////////////////////////////////////////////////////////////////////////

export const {
  postsLoading,
  postsLoaded,
  postsLoadFailed,
  postFormUpdateSync,
  postRemoveSync,
  postLikeSync,
  postUpdateCommentsCount,
} = postsSlice.actions;

export default postsSlice.reducer;
