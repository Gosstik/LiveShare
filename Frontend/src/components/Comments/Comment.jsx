import { useState, useReducer, useRef, useEffect } from "react";
import { useDispatch } from "react-redux";
import moment from "moment";

import CommentProperties from "./CommentProperties";

import { commentUpdateText } from "../Redux/Reducers/Comments";
import { apiUpdateComment } from "../../api/client";

import style from "./Comments.module.scss";

function inputReducer(state, action) {
  const { type } = action;

  switch (type) {
    case "updateText":
      return {
        ...state,
        text: action.newText,
        isInvalid: action.isInvalid,
      };
    default:
      console.warn("comments: editInputReducer: unknown type: ", type);
      return state;
  }
}

export default function Comment(props) {
  const { postId, comment } = props;

  const dispatch = useDispatch();
  const textbox = useRef(null);

  // Text

  const [inputState, inputDispatch] = useReducer(inputReducer, {
    text: comment.text,
    isInvalid: false,
  });

  const onInputChange = (event) => {
    inputDispatch({
      type: "updateText",
      newText: event.target.value,
      isInvalid: event.target.value.trim().length === 0,
    });
  };

  const [isEditingComment, setIsEditingComment] = useState(false);

  useEffect(() => {
    if (isEditingComment) {
      textbox.current.style.height = "inherit";
      textbox.current.style.height = `${textbox.current.scrollHeight}px`;
    }
  }, [isEditingComment, inputState.text]);

  const onFocus = (event) => {
    var prev = event.target.value;
    event.target.value = "";
    event.target.value = prev;
  };

  const onClickEdit = () => {
    if (isEditingComment) {
      if (inputState.isInvalid) {
        return;
      }

      const newText = inputState.text.trim();
      inputDispatch({
        type: "updateText",
        newText,
        isInvalid: false,
      });
      dispatch(
        commentUpdateText({
          postId,
          commentId: comment.commentId,
          text: newText,
        })
      );
      (async () => apiUpdateComment({
        "comment_id": comment.commentId,
        "text": newText,
      }))();
    }

    setIsEditingComment(!isEditingComment);
  };

  const onKeyDown = (event) => {
    if (event.key === "Enter" && !event.shiftKey) {
      onClickEdit();
    }
  };

  // CreatedAt

  let createdAtStr = moment(comment.createdAt).fromNow();

  // Result

  return (
    <div className={style.comment}>
      <div className={style.author}> {comment.author} </div>
      {isEditingComment && (
        <>
          <textarea
            type="text"
            autoFocus
            ref={textbox}
            value={inputState.text}
            onChange={onInputChange}
            onKeyDown={onKeyDown}
            onFocus={onFocus}
          />
          {inputState.isInvalid && (
            <div className={style.warning}>
              Comment must contain at least one non-whitespace character
            </div>
          )}
        </>
      )}
      {!isEditingComment && (
        <div className={style.commentText}> {inputState.text} </div>
      )}

      <div className={style.commentBottom}>
        <div className={style.commentCreatedAt}>{createdAtStr}</div>
        <CommentProperties
          postId={postId}
          comment={comment}
          onCommentEdit={onClickEdit}
          isEditingComment={isEditingComment}
        />
      </div>
    </div>
  );
}
