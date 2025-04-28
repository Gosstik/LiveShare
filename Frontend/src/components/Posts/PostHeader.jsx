import { React, useState } from "react";
import { useSelector } from "react-redux";
import { useNavigate } from "react-router-dom";

import IssueAuth from "../Modal/IssueAuth";
import { selectPostTitle } from "../Redux/Reducers/Posts";
import { useAuth } from "../AuthProvider/AuthProvider";

import style from "./PostHeader.module.scss";

import { trashImg, newTabImg } from "../Consts/Consts";

export default function PostHeader(props) {
  const { postId, isSinglePost, onPostRemove } = props;

  const { isAuthenticated } = useAuth();

  const title = useSelector(selectPostTitle(postId));

  const navigate = useNavigate();
  const onNewTab = () => navigate(`/posts/${postId}`);

  const [isModalOpened, setIsModalOpened] = useState(false);
  const openModal = () => setIsModalOpened(true);
  const closeModal = () => setIsModalOpened(false);

  return (
    <div className={style.postHeader}>
      <div className={style.title}> {title} </div>
      <div className={style.leftProps}>
        {!isSinglePost && (
          <img src={newTabImg} alt={"new tab"} onClick={onNewTab} />
        )}
      </div>
      <div className={style.rightProps}>
        <img
          src={trashImg}
          alt={"remove post"}
          onClick={isAuthenticated ? onPostRemove : openModal}
          draggable="false"
        />
        {isModalOpened && <IssueAuth onOkClick={closeModal} />}
      </div>
    </div>
  );
}
