import { React, useReducer } from "react";
import { useDispatch, useSelector } from "react-redux";
import classNames from "classnames/bind";

import { generateNewId } from "../utils";

import { postUpdateCommentsCount } from "../Redux/Reducers/Posts";

import { commentAdd } from "../Redux/Reducers/Comments";
import {
  selectCommentEls,
  selectCommentsCount,
  selectCommentsIsLoadFailed,
} from "../Redux/Reducers/Comments";

import style from "./Comments.module.scss";
import buttonStyle from "../Properties/Properties.module.scss";

import { sendCommentImg } from "../Consts/Consts";

const cxb = classNames.bind(buttonStyle);

function formInputReducer(state, action) {
  const { type } = action;

  switch (type) {
    case "text":
      return {
        ...state,
        text: action.newText,
        isInvalid: action.isInvalid,
      };
    case "erase":
      return {
        ...state,
        text: "",
        isInvalid: true,
      };
    default:
      console.warn("comments: formInputReducer: unknown type: ", type);
      return state;
  }
}

function isInputInvalid({ value }) {
  return value.trim().length === 0;
}

export default function CommentsForm(props) {
  const { postId } = props;

  const dispatch = useDispatch();

  const commentEls = useSelector(selectCommentEls(postId));

  const [inputState, inputDispatch] = useReducer(formInputReducer, {
    text: "",
    isInvalid: true,
  });

  const onInputTextChange = (event) => {
    const isInvalid = isInputInvalid({ value: event.target.value });
    inputDispatch({ type: "text", newText: event.target.value, isInvalid });
  };

  const prevCount = useSelector(selectCommentsCount(postId));

  const onCommentSend = () => {
    if (inputState.isInvalid) {
      return;
    }
    dispatch(
      postUpdateCommentsCount({ postId, newCommentsCount: prevCount + 1 })
    );
    dispatch(
      commentAdd({
        postId,
        comment: {
          commentId: generateNewId(commentEls, "commentId"),
          author: "Me", // TODO: replace with auth user
          text: inputState.text,
          likes: 0,
          isLiked: false,
          createdAt: Date.now(),
        },
      })
    );

    inputDispatch({ type: "erase" });
  };

  const onKeyDown = (event) => {
    if (event.key === "Enter") {
      onCommentSend();
    }
  };

  const isLoadFailed = useSelector(selectCommentsIsLoadFailed(postId));
  const buttonName = isLoadFailed ? "inactive" : "active";

  return (
    <div className={style.footerCommentForm}>
      <input className={cxb({"button-inactive": isLoadFailed})}
        type="text"
        value={inputState.text}
        onChange={onInputTextChange}
        onKeyDown={onKeyDown}
        placeholder="Your comment..."
        disabled={isLoadFailed}
      />
      <img className={cxb(`button-${buttonName}`)}
        src={sendCommentImg}
        alt="send comment"
        onClick={onCommentSend}
      />
    </div>
  );
}
