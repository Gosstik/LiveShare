import { applyMiddleware, createSlice } from "@reduxjs/toolkit";
import { thunk as thunkMiddleware } from "redux-thunk";
import { composeWithDevTools } from "@redux-devtools/extension";

import { fieldLessSort, getSortedArray, likesLessSort } from "../../utils";
import { apiGetPostComments } from "../../../api/client";

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
        }
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
      commentUpdateText(state, action) {
        const { postId, commentId, text } = action.payload;
        const group = state.commentGroups[postId];

        const commentEl = group.commentEls.find(
          (comment) => comment.commentId === commentId
        );
        commentEl.text = text;
      },
      commentRemove(state, action) {
        const { postId, commentId } = action.payload;
        const group = state.commentGroups[postId];

        group.commentEls = group.commentEls.filter(
          (comment) => comment.commentId !== commentId
        );
      },
      commentLike(state, action) {
        const { postId, commentId, isLiked } = action.payload;
        const group = state.commentGroups[postId];

        const comment = group.commentEls.find((c) => c.commentId === commentId);
        if (comment.isLiked !== isLiked) {
          comment.isLiked = isLiked;
        }
      },
      commentAdd(state, action) {
        const { postId, comment } = action.payload;
        const group = state.commentGroups[postId];

        console.log(comment) // !!!
        group.commentEls = [...group.commentEls, comment];

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

export function commentsLoad(postId) {
  return async function thunk(dispatch, getState) {
    const loaded = getState().comments.commentGroups[postId]?.loaded ?? false;
    if (!loaded) {
      apiGetPostComments(postId).then((response_body) => {
        const commentEls = Array.from(response_body.comments, (comment) => ({
          "postId": comment.post_id,
          "commentId": comment.comment_id,
          "author": comment.author_email.split('@')[0],
          "text": comment.text,
          "likes": comment.likes_count,
          "isLiked": comment.is_liked_by_user ?? false,
          "createdAt": comment.created_at,
        }));
        dispatch(
          commentsLoaded({
            postId,
            commentEls,
          })
        );
      }).catch(() => {
        dispatch(commentsLoadFailed({
          postId
        }))
      });
    }
  };
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
  return comment.likes + comment.isLiked;
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
  commentUpdateText,
  commentRemove,
  commentLike,
  commentAdd,
  commentAdded,
} = commentsSlice.actions;

export default commentsSlice.reducer;
