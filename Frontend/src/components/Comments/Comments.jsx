import React, { useEffect } from "react";
import { useDispatch, useSelector } from "react-redux";
import Divider from '@mui/joy/Divider';

import LoadingComment from "./LoadingComment";
import Comment from "./Comment";
import SortToggles from "../SortToggles/SortToggles";
import CommentsHeader from "./CommentsHeader";

import {
  commentsLoading,
  commentsLoad,
  commentsSortWrapper,
} from "../Redux/Reducers/Comments";
import {
  selectCommentEls,
  selectCommentsIsLoadFailed,
  selectCommentsSortToggles,
} from "../Redux/Reducers/Comments";

import { useApi } from "../ApiProvider/ApiProvider"

import style from "./Comments.module.scss";

function RenderComments(props) {
  const { postId } = props;

  const commentEls = useSelector(selectCommentEls(postId));
  const isLoadFailed = useSelector(selectCommentsIsLoadFailed(postId));

  if (isLoadFailed) {
    return (
      <div className={style.apiErrorMessage}>
        Something went wrong while loading comments :(
        <br />
        Try to reopen.
      </div>
    );
  }

  // TODO: redesign comments while loading
  return (
    <>
      {commentEls.map((comment, index) => {
        if (comment === null) {
          return <LoadingComment key={-index} />;
        }

        return (
          <React.Fragment key={comment.commentId}>
            <Comment postId={postId} comment={comment} />
            {commentEls.length !== index + 1 && (
              <Divider sx={{ my: 1 }} />
            )}
          </React.Fragment>
        );
      })}
    </>
  );
}

export default function Comments(props) {
  const { post, onCommentsClose, shouldReloadComments, setShouldReloadComments } = props;

  const dispatch = useDispatch();
  const apiClient = useApi();
  const postId = post.postId;

  const commentEls = useSelector(selectCommentEls(postId));
  if (commentEls === null) {
    dispatch(
      commentsLoading({
        postId,
        loadingComments: Array(post.commentsCount).fill(null),
      })
    );
  }

  useEffect(() => {
    dispatch(commentsLoad(apiClient, postId));
    setShouldReloadComments(false);
  }, [shouldReloadComments]); // eslint-disable-line react-hooks/exhaustive-deps

  return (
    <div className={style.commentsSection}>
      <CommentsHeader onCommentsClose={onCommentsClose} />

      <div className={style.commentsSortToggles}>
        <SortToggles
          sortReducer={commentsSortWrapper(postId)}
          sortTogglesSelector={selectCommentsSortToggles(postId)}
          togglesData={[
            { name: "date", fieldName: "createdAt" },
            { name: "likes", fieldName: "likes" },
          ]}
          togglesStyle={style}
        />
      </div>

      <div className={style.commentsMain}>
        <RenderComments postId={postId} />
      </div>
    </div>
  );
}
