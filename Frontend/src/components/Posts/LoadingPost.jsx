import headerStyle from "./PostHeader.module.scss";
import postsStyle from "./Posts.module.scss";

export default function LoadingPost() {
  return (
    <div className={postsStyle.post}>
      <div className={headerStyle.postHeader}>
        <div className={headerStyle.title}> {"loading..."} </div>
      </div>
      <div className={postsStyle.postMain}>
        <div className={postsStyle.text}> {"loading..."} </div>
      </div>
    </div>
  );
}
