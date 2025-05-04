import { useDispatch, useSelector } from "react-redux";

import { postUpdateCommentsCount } from "../Redux/Reducers/Posts";

import {
  selectCommentsCount,
  selectCommentLikesCountW,
  selectCommentIsLiked,
  commentRemove,
  commentLike,
} from "../Redux/Reducers/Comments";

import { useApi } from "../ApiProvider/ApiProvider"

import style from "./Comments.module.scss";

import {
  trashImg,
  redLikeImg,
  greyLikeImg,
  editImg,
  checkImg,
} from "../Consts/Consts";

function CommentProperty(props) {
  const { image, alt, onClick } = props;

  return (
    <div className={style.commentProperty}>
      <img src={image} alt={alt} onClick={onClick} />
    </div>
  );
}

function CommentCountProperty(props) {
  const { image, alt, onClick, count } = props;

  return (
    <div className={style.commentCountProperty}>
      <img src={image} alt={alt} onClick={onClick} />
      <div className={style.count}>{count}</div>
    </div>
  );
}

export default function CommentProperties(props) {
  const { postId, comment, onCommentEdit, isEditingComment } = props;

  const dispatch = useDispatch();
  const apiClient = useApi();

  const commentsCount = useSelector(selectCommentsCount(postId));
  const commentLikes = useSelector(
    selectCommentLikesCountW(postId, comment.commentId)
  );
  const commentIsLiked = useSelector(
    selectCommentIsLiked(postId, comment.commentId)
  );

  const onCommentRemove = () => {
    dispatch(postUpdateCommentsCount({ postId, newCommentsCount: commentsCount - 1 }));
    dispatch(
      commentRemove({
        postId,
        commentId: comment.commentId,
        apiClient,
      })
    );
  };

  // Likes

  const onLikeClick = () => {
    dispatch(
      commentLike({
        postId,
        commentId: comment.commentId,
        isLiked: !commentIsLiked,
        apiClient,
      })
    );
  };

  return (
    <div className={style.commentProperties}>
      <CommentProperty
        image={isEditingComment ? checkImg : editImg}
        alt="edit comment text"
        onClick={onCommentEdit}
      />
      <CommentProperty
        image={trashImg}
        alt="remove comment"
        onClick={onCommentRemove}
      />
      <CommentCountProperty
        image={commentIsLiked ? redLikeImg : greyLikeImg}
        alt="comment"
        onClick={onLikeClick}
        count={commentLikes}
      />
    </div>
  );
}
