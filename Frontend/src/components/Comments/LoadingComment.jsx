import style from "./Comments.module.scss";

export default function LoadingComment() {
  return (
    <div className={style.comment}>
      <div className={style.author}> {"loading..."} </div>
      <div className={style.commentText}> {"loading..."} </div>
    </div>
  );
}
