import { React } from "react";
import { useState } from "react";
import { useSelector, useDispatch } from "react-redux";
import classNames from "classnames/bind";

import PostHeader from "./PostHeader";
import PostFooterProps from "./PostFooterProps";
import PostForm from "./PostForm";
import Comments from "../Comments/Comments";
import CommentsForm from "../Comments/CommentsForm";

import { postFormUpdate, postRemove } from "../Redux/Reducers/Posts";
import { selectPost, selectPostText } from "../Redux/Reducers/Posts";

import style from "./Posts.module.scss";

export const cx = classNames.bind(style);

export default function Post(props) {
  const { postId, isSinglePost } = props;

  const dispatch = useDispatch();

  const post = useSelector(selectPost(postId));

  const curText = useSelector(selectPostText(postId));
  const [isModalOpened, setIsModalOpened] = useState(false);

  const onPostEdit = () => setIsModalOpened(true);

  const onFormSubmit = ({ newTitle, newText }) => {
    dispatch(
      postFormUpdate({
        postId,
        newTitle,
        newText,
      })
    );
    setIsModalOpened(false);
  };

  const onFormCancel = () => setIsModalOpened(false);

  const onPostRemove = () => dispatch(postRemove({ postId }));

  const [areCommentsShown, setAreCommentsShown] = useState(false);
  const swapIsCommentShown = () => setAreCommentsShown(!areCommentsShown);

  return (
    <>
      <PostHeader
        postId={postId}
        isSinglePost={isSinglePost}
        onPostRemove={onPostRemove}
      />

      <div className={style.postMain}>
        <div
          className={cx({
            text: !areCommentsShown,
            textBeforeComments: areCommentsShown,
          })}
        >
          {curText}
        </div>

        {areCommentsShown && (
          <Comments post={post} onCommentsClose={swapIsCommentShown} />
        )}
      </div>

      <div className={style.postFooter}>
        {areCommentsShown && <CommentsForm postId={postId} />}

        {!areCommentsShown && (
          <PostFooterProps
            postId={postId}
            onCommentClick={swapIsCommentShown}
            onPostEdit={onPostEdit}
            isSinglePost={isSinglePost}
          />
        )}
      </div>

      {isModalOpened && (
        <PostForm
          formTitle={"Editing post"}
          postId={post.postId}
          onFormSubmit={onFormSubmit}
          onFormCancel={onFormCancel}
        />
      )}
    </>
  );
}
