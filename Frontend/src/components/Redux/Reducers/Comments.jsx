import { applyMiddleware, createSlice } from "@reduxjs/toolkit";
import { thunk as thunkMiddleware } from "redux-thunk";
import { composeWithDevTools } from "@redux-devtools/extension";

import { fieldLessSort, getSortedArray, likesLessSort } from "../../utils";
import { apiGetPostComments } from "../../../api/client";
import { getUrlWithParams } from "../../ApiProvider/ApiClient";

const composedEnhancer = composeWithDevTools(applyMiddleware(thunkMiddleware));

const initialState = {
  commentGroups: {},
  defaultSortToggles: {
    sortFieldName: "createdAt",
    isAscending: true,
  },
};

const getInitialCommentGroup = (state, loadingComments) => {
  return {
    commentEls: loadingComments,
    sortToggles: state.defaultSortToggles,
    areLoading: true,
    loaded: false,
    isLoadFailed: false,
  };
};

// TODO: use createAsyncThunk
// https://redux.js.org/tutorials/fundamentals/part-8-modern-redux#using-createasyncthunk

const commentsSlice = createSlice(
  {
    name: "comments",
    initialState,
    reducers: {
      commentsLoading(state, action) {
        const { postId, loadingComments } = action.payload;
        if (!state.commentGroups.hasOwnProperty(postId)) {
          state.commentGroups[postId] = getInitialCommentGroup(
            state,
            loadingComments
          );
        }
      },
      commentsLoaded(state, action) {
        const { postId, commentEls } = action.payload;
        const group = state.commentGroups[postId];

        const fieldName = group.sortToggles.sortFieldName;
        const lessCmp =
          fieldName === "likes" ? likesLessSort : fieldLessSort(fieldName);
        const sortedCommentEls = getSortedArray(
          commentEls,
          lessCmp,
          state.defaultSortToggles.isAscending
        );
        state.commentGroups[postId] = {
          ...state.commentGroups[postId],
          commentEls: sortedCommentEls,
          sortToggles: state.defaultSortToggles,
          areLoading: false,
          loaded: true,
          isLoadFailed: false,
        };
      },
      commentsLoadFailed(state, action) {
        const { postId } = action.payload;

        state.commentGroups[postId] = {
          ...state.commentGroups[postId],
          areLoading: false,
          loaded: false,
          isLoadFailed: true,
        };
      },
      commentsSort(state, action) {
        const { postId, sortFieldName, isAscending } = action.payload;
        const group = state.commentGroups[postId];

        const fieldName = sortFieldName;
        const lessCmp =
          fieldName === "likes" ? likesLessSort : fieldLessSort(fieldName);
        group.commentEls = getSortedArray(
          group.commentEls,
          lessCmp,
          isAscending
        );

        group.sortToggles = {
          sortFieldName,
          isAscending,
        };
      },
      commentUpdateTextSync(state, action) {
        const { postId, commentId, text } = action.payload;
        const group = state.commentGroups[postId];

        const commentEl = group.commentEls.find(
          (comment) => comment.commentId === commentId
        );
        commentEl.text = text;
      },
      commentRemoveSync(state, action) {
        const { postId, commentId } = action.payload;
        const group = state.commentGroups[postId];

        group.commentEls = group.commentEls.filter(
          (comment) => comment.commentId !== commentId
        );
      },
      commentLikeSync(state, action) {
        const { postId, commentId, newIsLiked } = action.payload;
        const group = state.commentGroups[postId];

        const comment = group.commentEls.find((c) => c.commentId === commentId);
        if (comment.isLiked !== newIsLiked) {
          comment.isLiked = newIsLiked;
        }
      },
      commentCreateSync(state, action) {
        // TODO: add commentId after it appears on backend
        // const { postId } = action.payload;
        // const group = state.commentGroups[postId];

        // console.log(comment); // !!!
        // group.commentEls = [...group.commentEls, comment];
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

export function commentsLoad(apiClient, postId) {
  return async function thunk(dispatch, getState) {
    const loaded = getState().comments.commentGroups[postId]?.loaded ?? false;
    // if (!loaded) {
      apiClient.commentsV1ForPost(postId, {}).then(async (response) => {
        const body = await response.json();
        const commentEls = Array.from(body.comments, (comment) => ({
          postId: postId,
          commentId: comment.id,
          author: {
            id: comment.author.id,
            email: comment.author.email,
            firstName: comment.author.firstName,
            lastName: comment.author.lastName,
            displayedName: comment.author.displayedName,
            profileIconUrl: comment.author.profileIconUrl,
          },
          text: comment.textContent,
          likes: comment.likesCount,
          isLiked: comment.isLikedByUser ?? false,
          createdAt: comment.createdAt,
        }));
        dispatch(
          commentsLoaded({
            postId,
            commentEls,
          })
        );
      }).catch(() => {
        dispatch(
          commentsLoadFailed({
            postId,
          })
        );
      });
    // }
  };
}

export function commentUpdateText(payload) {
  const { postId, commentId, text, apiClient } = payload;
  return async function thunk(dispatch, getState) {
    await apiClient.commentsV1CommentPatch(commentId, {
      textContent: text,
    });
    dispatch(
      commentUpdateTextSync({
        postId, commentId, text,
      })
    );
  }
}

export function commentRemove(payload) {
  const { postId, commentId, apiClient } = payload;
  return async function thunk(dispatch, getState) {
    await apiClient.commentsV1CommentDelete(commentId);
    dispatch(
      commentRemoveSync({
        postId, commentId,
      })
    );
  }
}

export function commentLike(payload) {
  const { postId, commentId, apiClient } = payload;
  return async function thunk(dispatch, getState) {
    const isLiked = selectCommentIsLiked(postId, commentId)(getState());
    const newIsLiked = !isLiked;
    if (newIsLiked) {
      await apiClient.commentsV1CommentLike(commentId);
    } else {
      await apiClient.commentsV1CommentUnlike(commentId);
    }
    dispatch(
      commentLikeSync({
        postId, commentId, newIsLiked
      })
    );
  }
}

export function commentCreate(payload) {
  const { postId, textContent, apiClient } = payload;
  return async function thunk(dispatch, getState) {
    // TODO: handle errors as in promises
    const response = await apiClient.commentsV1CommentCreate({
      postId,
      textContent,
    });
    // TODO: send commentId from backend for drawing

    dispatch(
      commentCreateSync({
        postId,
      })
    );
  }
}

export const commentsSortWrapper = (postId) => (payload) => {
  return function thunk(dispatch, getState) {
    dispatch(
      commentsSort({
        ...payload,
        postId,
      })
    );
  };
};

// commentsV1ForPost(postId, params) {
//   const url = getUrlWithParams(`/comments/v1/for-post/${postId}`, params);
//   return this.get(url);
// }

////////////////////////////////////////////////////////////////////////////////

// Selectors

export const selectCommentEls = (postId) => (state) => {
  return state.comments.commentGroups[postId]?.commentEls ?? null;
};

export const selectCommentsIsLoadFailed = (postId) => (state) => {
  return state.comments.commentGroups[postId]?.isLoadFailed ?? false;
};

export const selectCommentsSortToggles = (postId) => (state) =>
  state.comments.commentGroups[postId]?.sortToggles || // TODO: replace with ??
  state.comments.defaultSortToggles;

export const selectCommentsCount = (postId) => (state) =>
  Object.keys(state.comments.commentGroups[postId].commentEls).length;

export const selectCommentLikesCountW = (postId, commentId) => (state) => {
  const comment = state.comments.commentGroups[postId].commentEls.find(
    (comment) => comment.commentId === commentId
  );
  return comment.likes;
};

export const selectCommentIsLiked = (postId, commentId) => (state) => {
  const comment = state.comments.commentGroups[postId].commentEls.find(
    (comment) => comment.commentId === commentId
  );
  return comment.isLiked;
};

////////////////////////////////////////////////////////////////////////////////

export const {
  commentsLoading,
  commentsLoaded,
  commentsLoadFailed,
  commentsSort,
  commentUpdateTextSync,
  commentRemoveSync,
  commentLikeSync,
  commentCreateSync,
  commentAdded,
} = commentsSlice.actions;

export default commentsSlice.reducer;
