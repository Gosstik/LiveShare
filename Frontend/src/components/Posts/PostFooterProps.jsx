import { React, useContext, useState } from "react";
import { useDispatch, useSelector } from "react-redux";
import moment from "moment";

import {
  selectPostCommentsCount,
  selectPostIsLiked,
  selectPostLikes,
  selectPostCreatedAt,
} from "../Redux/Reducers/Posts";
import { postLike } from "../Redux/Reducers/Posts";
import { AuthContext } from "../AuthProvider/AuthProvider";
import IssueAuth from "../Modal/IssueAuth";
import { useApi } from "../ApiProvider/ApiProvider";
import { useAuth } from "../AuthProvider/AuthProvider";

import style from "./PostFooter.module.scss";

import { redLikeImg, greyLikeImg, commentImg, editImg } from "../Consts/Consts";


function PostProperty(props) {
  const { image, alt, onClick } = props;

  return (
    <div className={style.simpleProp}>
      <img src={image} alt={alt} onClick={onClick} draggable="false" />
    </div>
  );
}

function PostCountProperty(props) {
  const { image, alt, onClick, count } = props;

  const { user, isAuthenticated } = useAuth();

  // TODO: modal with auth
  const [isModalOpened, setIsModalOpened] = useState(false);

  const openModal = () => setIsModalOpened(true)
  const closeModal = () => setIsModalOpened(false)

  return (
    <div className={style.countProp}>
      {isAuthenticated && <img src={image} alt={alt} onClick={onClick} draggable="false" />}
      {!isAuthenticated && <img src={image} alt={alt} onClick={openModal} draggable="false" />}
      {isModalOpened && <IssueAuth onOkClick={closeModal} />}
      <div className={style.count}>{count}</div>
    </div>
  );
}

export default function PostFooterProps(props) {
  const {
    postId,
    onCommentClick,
    onPostEdit,
    isSinglePost,
  } = props;

  const dispatch = useDispatch();
  const apiClient = useApi();

  // Likes

  const likes = useSelector(selectPostLikes(postId));
  const isLiked = useSelector(selectPostIsLiked(postId));

  const onLikeClick = () => {
    dispatch(
      postLike({
        postId, apiClient
      })
    );
  };

  const createdAt = useSelector(selectPostCreatedAt(postId))

  const createdAtDisplay = moment(createdAt).fromNow();
  // TODO: if diff > month - print YYYY:MM:DD
  // console.log(`!!! createdAtDisplay: ${createdAtDisplay}`);

  const commentsCount = useSelector(selectPostCommentsCount(postId));

  return (
    <div className={style.footerPostData}>
      <div className={style.createdAt}>{createdAtDisplay}</div>
      <div className={style.props}>
        {isSinglePost && (
          <PostProperty image={editImg} alt="edit text" onClick={onPostEdit} />
        )}
        <PostCountProperty
          image={commentImg}
          alt="comment"
          onClick={onCommentClick}
          count={commentsCount}
        />
        <PostCountProperty
          image={isLiked ? redLikeImg : greyLikeImg}
          alt="likes"
          onClick={onLikeClick}
          count={likes}
        />
      </div>
    </div>
  );
}
