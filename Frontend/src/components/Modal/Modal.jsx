import classNames from "classnames/bind";

import style from "./Modal.module.scss";

const cx = classNames.bind(style);

export default function Modal(props) {
  const {content, onClose, width, height} = props;

  const sizes = {
    width: width,
    height: height
  }

  return (
    <div className={style.modalContainer} onClose={onClose}>
      <div className={style.modal} style={sizes}>{content}</div>
    </div>
  );
}
