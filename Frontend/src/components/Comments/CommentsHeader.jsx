import { React } from "react";

import style from "./Comments.module.scss";

import { crossCloseImg } from "../Consts/Consts";

export default function CommentsHeader(props) {
  const { onCommentsClose } = props;

  return (
    <div className={style.commentsHeader}>
      <div className={style.title}>Comments</div>
      <div className={style.close}>
        <img src={crossCloseImg} alt="close comments" onClick={onCommentsClose} />
      </div>
    </div>
  );
}
