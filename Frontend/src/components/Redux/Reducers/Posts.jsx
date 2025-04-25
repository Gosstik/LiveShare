import { applyMiddleware, createSlice } from "@reduxjs/toolkit";
import { thunk as thunkMiddleware } from "redux-thunk";
import { composeWithDevTools } from "@redux-devtools/extension";

import { getSortedArray, likesLessSort, fieldLessSort } from "../../utils";
import { apiGetPosts, apiUpdatePostLike } from "../../../api/client";

const composedEnhancer = composeWithDevTools(applyMiddleware(thunkMiddleware));

const getInnerPostById = (state, postId) =>
  state.posts.find((post) => post.postId === postId);

const initialState = {
  posts: [],
  areLoading: false,
  loaded: false,
  loadFailed: false, // TODO: add error handling in UI
  sortToggles: {
    sortFieldName: "createdAt",
    isAscending: true,
  },
};

const postsSlice = createSlice(
  {
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

        const fieldName = state.sortToggles.sortFieldName;
        const lessCmp =
          fieldName === "likes" ? likesLessSort : fieldLessSort(fieldName);
        state.posts = getSortedArray(
          postEls,
          lessCmp,
          state.sortToggles.isAscending
        );

        state.areLoading = false;
        state.loaded = true;
      },
      postsLoadFailed(state) {
        state.areLoading = false;
        state.loaded = false;
        state.loadFailed = true;
      },
      postsSort(state, action) {
        const { sortFieldName, isAscending } = action.payload;

        const fieldName = state.sortToggles.sortFieldName;
        const lessCmp =
          fieldName === "likes" ? likesLessSort : fieldLessSort(fieldName);
        state.posts = getSortedArray(state.posts, lessCmp, isAscending);

        state.sortToggles = {
          sortFieldName,
          isAscending,
        };
      },
      postFormUpdate(state, action) {
        const { postId, newText, newTitle } = action.payload;

        const post = getInnerPostById(state, postId);
        post.text = newText;
        post.title = newTitle;
      },
      postRemove(state, action) {
        const { postId } = action.payload;

        state.posts = state.posts.filter((post) => post.postId !== postId);
        // TODO: api call
      },
      postLikeSync(state, action) {
        const { postId, newIsLiked } = action.payload;

        const post = state.posts.find((post) => post.postId === postId);
        if (post.isLiked !== newIsLiked) {
          post.isLiked = newIsLiked;
          post.likes += (newIsLiked ? 1 : -1)
        }
      },
      postUpdateCommentsCount(state, action) {
        const { postId, newCommentsCount } = action.payload;

        const post = getInnerPostById(state, postId);
        post.commentsCount = newCommentsCount;
      },
      postAdd(state, action) {
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

export function postsLoad() {
  // return async function thunk(dispatch, getState) {
  //   const loaded = getState().posts.loaded;
  //   if (!loaded) {
  //     apiGetPosts().then((postEls) => {
  //       dispatch(
  //         postsLoaded({
  //           postEls,
  //         })
  //       );
  //     }).catch(() => {
  //       dispatch(postsLoadFailed())
  //     });
  //   }
  // };

  return async function thunk(dispatch, getState) {
    const loaded = getState().posts.loaded;
    if (!loaded) {
      apiGetPosts()
        .then((response_body) => {
          const postEls = Array.from(response_body.posts, (post) => ({
            postId: post.post_id,
            authorEmail: post.author_email, // TODO: add handler
            title: post.title,
            text: post.text,
            likes: post.likes_count,
            isLiked: post.is_liked_by_user ?? false,
            commentsCount: post.comments_count,
            createdAt: post.created_at,
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
    }
  };
}

export function postLike(payload) {
  const { postId } = payload;
  return async function thunk(dispatch, getState) {
    const isLiked = selectPostIsLiked(postId)(getState());
    (async () => apiUpdatePostLike({
      post_id: postId,
      set_like: !isLiked,
    }))();
    dispatch(
      postLikeSync({
        postId, newIsLiked: !isLiked
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

export const selectPostsSortToggles = (state) => state.posts.sortToggles;

////////////////////////////////////////////////////////////////////////////////

export const {
  postsLoading,
  postsLoaded,
  postsLoadFailed,
  postsSort,
  postFormUpdate,
  postRemove,
  postLikeSync,
  postUpdateCommentsCount,
} = postsSlice.actions;

export default postsSlice.reducer;
