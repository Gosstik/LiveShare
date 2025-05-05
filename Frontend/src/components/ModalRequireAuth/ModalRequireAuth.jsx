import { useEffect } from "react";
import { useNavigate } from "react-router-dom";
import classNames from "classnames/bind";

import Modal from "../Modal/Modal";
import { signinUrl, signupUrl, exploreUrl } from "../../api/urls";
import style from "./ModalRequireAuth.module.scss";

const cx = classNames.bind(style);

export default function ModalRequireAuth({ onClose, shallRedirect = false }) {
  const navigate = useNavigate();

  useEffect(() => {
    const handleEscPress = (event) => {
      if (event.key === "Escape") {
        handleClose();
      }
    };

    document.addEventListener("keydown", handleEscPress);
    return () => document.removeEventListener("keydown", handleEscPress);
  }, []);

  const handleClose = () => {
    if (shallRedirect) {
      navigate(exploreUrl);
    }
    onClose();
  };

  const handleSignin = () => {
    navigate(signinUrl);
    onClose();
  };

  const handleSignup = () => {
    navigate(signupUrl);
    onClose();
  };

  const modalContent = (
    <div className={style.container}>
      <div className={style.closeButton} onClick={handleClose}>
        ✕
      </div>
      <div className={style.content}>
        <h2 className={style.title}>Authorization Required</h2>
        <p className={style.message}>
          This feature is only available to authorized users. Please sign in or
          create a new account to continue.
        </p>
        <div className={style.buttons}>
          <button className={cx("button", "secondary")} onClick={handleSignin}>
            Sign in
          </button>
          <button className={cx("button", "primary")} onClick={handleSignup}>
            Sign up
          </button>
        </div>
      </div>
    </div>
  );

  return (
    <Modal
      content={modalContent}
      onClose={handleClose}
      width="400px"
      height="250px"
    />
  );
}
