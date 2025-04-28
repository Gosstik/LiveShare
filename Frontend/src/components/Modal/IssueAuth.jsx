import Modal from "./Modal";

import postsStyle from "../Posts/Posts.module.scss";
import style from "./IssueAuth.module.scss";


export default function IssueAuth(props) {
  const { onOkClick } = props;
  const modalContent = (
    <>
      <div className={postsStyle.postFormTitle}>
        That feature is allowed only for authorized users.
      </div>
      <div className={style.okButton} onClick={onOkClick}>
        Ok
      </div>
    </>
  );

  return (
    <Modal
      content={modalContent}
      onClose={() => {}}
      width={"400px"}
      height={"180px"}
    />
  );
}
