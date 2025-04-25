import { React, useReducer } from "react";
import classNames from "classnames/bind";
import { useSelector } from "react-redux";

import Modal from "../Modal/Modal";
import InvalidInputTooShort from "../Invalid/InvalidInputTooShort";

import { selectPostTitle, selectPostText } from "../Redux/Reducers/Posts";

import style from "./Posts.module.scss";

const cx = classNames.bind(style);

function inputReducer(state, action) {
  const { type } = action;

  switch (type) {
    case "updateTitle":
      return {
        ...state,
        title: action.title,
        isTitleValid: action.isTitleValid,
      };
    case "updateText":
      return {
        ...state,
        text: action.text,
        isTextValid: action.isTextValid,
      };
    default:
      console.warn("PostForm: inputReducer: unknown type: ", type);
      return state;
  }
}

const getIsValidInput = (inputValue) => inputValue.trim().length !== 0;

export default function PostForm(props) {
  const { formTitle, postId, onFormSubmit, onFormCancel } = props;

  const title = useSelector(selectPostTitle(postId));
  const text = useSelector(selectPostText(postId));

  const [inputState, inputDispatch] = useReducer(inputReducer, {
    title,
    text,
    isTitleValid: getIsValidInput(title),
    isTextValid: getIsValidInput(text),
  });

  // Title

  const onTitleChange = (event) => {
    inputDispatch({
      type: "updateTitle",
      title: event.target.value,
      isTitleValid: getIsValidInput(event.target.value),
    });
  };

  // Text

  const onTextChange = (event) => {
    inputDispatch({
      type: "updateText",
      text: event.target.value,
      isTextValid: getIsValidInput(event.target.value),
    });
  };

  const isSubmitActive = inputState.isTitleValid && inputState.isTextValid;
  const submitType = isSubmitActive ? "active" : "inactive";

  const onSubmit = () => {
    if (!isSubmitActive) {
      return;
    }
    onFormSubmit({
      newTitle: inputState.title.trim(),
      newText: inputState.text.trim(),
    });
  };

  const modalContent = (
    <>
      <div className={style.postFormTitle}>{formTitle}</div>

      <div className={style.postTextInput}>
        <div className={style.textInputName}>Title:</div>
        <textarea
          type="text"
          value={inputState.title}
          onChange={onTitleChange}
          required
        />
        {!inputState.isTitleValid && (
          <InvalidInputTooShort warningStyle={style.warning} />
        )}
      </div>

      <div className={style.postTextInput}>
        <div className={style.textInputName}>Text:</div>
        <textarea type="text" value={inputState.text} onChange={onTextChange} />
        {!inputState.isTextValid && (
          <InvalidInputTooShort warningStyle={style.warning} />
        )}
      </div>

      <div className={style.postFormButtons}>
        <div
          className={cx("formCancelButton", "button-active")}
          onClick={onFormCancel}
        >
          Cancel
        </div>
        <div
          className={cx("formSubmitButton", `button-${submitType}`)}
          onClick={onSubmit}
        >
          Submit
        </div>
      </div>
    </>
  );

  return (
    <Modal
      content={modalContent}
      onClose={() => {}}
      width={"600px"}
      height={"500px"}
    />
  );
}
