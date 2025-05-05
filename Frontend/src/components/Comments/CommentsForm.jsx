import { React, useReducer, useRef, useEffect } from "react";
import { useDispatch, useSelector } from "react-redux";
import Avatar from "@mui/joy/Avatar";
import { postUpdateCommentsCount } from "../Redux/Reducers/Posts";
import { sendCommentImg } from "../Consts/Consts";
import { commentCreate } from "../Redux/Reducers/Comments";
import {
  selectCommentEls,
  selectCommentsCount,
  selectCommentsIsLoadFailed,
} from "../Redux/Reducers/Comments";

import { useApi } from "../ApiProvider/ApiProvider";
import { useAuth } from "../AuthProvider/AuthProvider";

import defaultAvatar from "../../images/default-avatar.png";
import style from "./Comments.module.scss";

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
  const { postId, setShouldReloadComments } = props;
  const textareaRef = useRef(null);
  const { user } = useAuth();

  const dispatch = useDispatch();
  const apiClient = useApi();

  const [inputState, inputDispatch] = useReducer(formInputReducer, {
    text: "",
    isInvalid: true,
  });

  const hiddenDivRef = useRef(null);

  useEffect(() => {
    if (textareaRef.current) {
      // Reset height to get accurate scrollHeight
      textareaRef.current.style.height = '0px';
      // Set new height based on content
      const height = Math.min(textareaRef.current.scrollHeight, 150);
      textareaRef.current.style.height = `${height}px`;
    }
  }, [inputState.text]);

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
      commentCreate({
        postId,
        textContent: inputState.text,
        apiClient,
      })
    );
    inputDispatch({ type: "erase" });
    setShouldReloadComments(true);
  };

  const onKeyDown = (event) => {
    if (event.key === "Enter" && !event.shiftKey) {
      event.preventDefault();
      onCommentSend();
    }
  };

  const isLoadFailed = useSelector(selectCommentsIsLoadFailed(postId));

  return (
    <div className={style.commentForm}>
      <div className={style.avatarContainer}>
        <Avatar
          src={user?.profileIconUrl || defaultAvatar}
          alt={user?.displayedName}
          sx={{ width: 30, height: 30 }}
        />
      </div>
      
      <div className={style.inputContainer}>
        <textarea
          ref={textareaRef}
          value={inputState.text}
          onChange={onInputTextChange}
          onKeyDown={onKeyDown}
          placeholder="Write a comment..."
          disabled={isLoadFailed}
        />
      </div>

      <div className={style.sendButton}>
        <img
          src={sendCommentImg}
          alt="send comment"
          onClick={onCommentSend}
          className={isLoadFailed || inputState.isInvalid ? style.disabled : style.enabled}
        />
      </div>
    </div>
  );
}
