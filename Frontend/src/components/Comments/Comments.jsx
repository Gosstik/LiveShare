import React, { useEffect } from "react";
import { useDispatch, useSelector } from "react-redux";

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

import style from "./Comments.module.scss";

function RenderComments(props) {
  const { postId } = props;

  const commentEls = useSelector(selectCommentEls(postId));
  const isLoadFailed = useSelector(selectCommentsIsLoadFailed(postId));

  if (isLoadFailed) {
    return (
      <div className={style.apiErrorMessage}>
        Something went wrong while loading comments.
        <br />
        Try to reopen comments.
      </div>
    );
  }

  return (
    <>
      {commentEls.map((comment, index) => {
        if (comment === null) {
          return <LoadingComment key={-index} />;
        }

        return (
          <React.Fragment key={comment.commentId}>
            <div className={style.comment}>
              <Comment postId={postId} comment={comment} />
            </div>
            <div style={{ display: "flex", justifyContent: "center" }}>
              {commentEls.length !== index + 1 && <hr />}
            </div>
          </React.Fragment>
        );
      })}
    </>
  );
}

export default function Comments(props) {
  const { post, onCommentsClose } = props;

  const dispatch = useDispatch();
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
    dispatch(commentsLoad(postId));
  }, []); // eslint-disable-line react-hooks/exhaustive-deps

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
