import { applyMiddleware, createSlice } from "@reduxjs/toolkit";
import { thunk as thunkMiddleware } from "redux-thunk";
import { composeWithDevTools } from "@redux-devtools/extension";

import { getSortedArray, likesLessSort, fieldLessSort } from "../../utils";
import { apiGetPosts, apiUpdatePostLike } from "../../../api/client";

import { LoadingState, PostsSortOptions } from "../../utils";

const composedEnhancer = composeWithDevTools(applyMiddleware(thunkMiddleware));

const initialState = {
  postsData: [],
  loadingState: LoadingState.NOT_STARTED,
  sortToggles: {
    sortOption: PostsSortOptions.CREATED_AT,
    isAscending: true,
  },
  defaultPost: {
      id: 15,
      author: {
          id: 2,
          email: "goshikvash@gmail.com",
          firstName: "First",
          lastName: "LastName",
          displayedName: "First LastName",
          profileIconUrl: ""
      },
      title: "Post 0 Title",
      textContent: "Lorem ipsum is placeholder text commonly used in the graphic, print, and publishing industries.",
      createdAt: "2025-04-27T15:31:19.257000+03:00",
      editedAt: "2025-04-27T15:31:19.259724+03:00",
      likesCount: 0,
      isLikedByUser: false,
      commentsCount: 0,
      attachedImageUrl: ""
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

        const fieldName = state.sortToggles.sortOption;
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

        const fieldName = state.sortToggles.sortOption;
        const lessCmp =
          fieldName === "likes" ? likesLessSort : fieldLessSort(fieldName);
        state.posts = getSortedArray(state.posts, lessCmp, isAscending);

        state.sortToggles = {
          sortOption: sortFieldName,
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

///////////////////////////

const getInnerPostById = (state, postId) =>
  state.posts.find((post) => post.postId === postId);

// const initialState = {
//   posts: [],
//   areLoading: false,
//   loaded: false,
//   loadFailed: false, // TODO: add error handling in UI
//   sortToggles: {
//     sortFieldName: "createdAt",
//     isAscending: true,
//   },
// };

const postsSliceOld = createSlice(
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

        const fieldName = state.sortToggles.sortOption;
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

        const fieldName = state.sortToggles.sortOption;
        const lessCmp =
          fieldName === "likes" ? likesLessSort : fieldLessSort(fieldName);
        state.posts = getSortedArray(state.posts, lessCmp, isAscending);

        state.sortToggles = {
          sortOption: sortFieldName,
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
      // TODO: replace API
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
    // TODO: replace API
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

export const selectPost = (postId) => (state) => getPostById(state, postId);

//// Old

const getPostById = (state, postId) => {
  if (postId === 0) {
    return state.posts.defaultPost;
  }
  return state.posts.posts.find((post) => Number(post?.postId) === Number(postId))
}

export const selectPostEls = (state) => state.posts.posts;

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
