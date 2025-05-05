import { React, useState, useEffect } from "react";
import { useSelector, useDispatch } from "react-redux";
import { useNavigate } from "react-router-dom";
import classNames from "classnames/bind";
import moment from "moment";
import Avatar from "@mui/joy/Avatar";
import IconButton from "@mui/material/IconButton";
import Menu from "@mui/material/Menu";
import MenuItem from "@mui/material/MenuItem";
import ListItemIcon from "@mui/material/ListItemIcon";
import Typography from "@mui/material/Typography";

import Comments from "../Comments/Comments";
import CommentsForm from "../Comments/CommentsForm";
import { useApi } from "../ApiProvider/ApiProvider";
import { useAuth } from "../AuthProvider/AuthProvider";

import { postFormUpdate, postRemove } from "../Redux/Reducers/Posts";
import {
  selectPost,
  selectPostText,
  selectPostCreatedAt,
} from "../Redux/Reducers/Posts";
import PostFooterProps from "./PostFooterProps";

import style from "./Posts.module.scss";
import defaultAvatar from "../../images/default-avatar.png";
import { newTabImg, trashImg, editImg } from "../Consts/Consts";
import { editPostUrl } from "../../api/urls";

export const cx = classNames.bind(style);

export default function Post(props) {
  const { postId, isSinglePost } = props;

  const dispatch = useDispatch();
  const navigate = useNavigate();
  const apiClient = useApi();
  const { user, isAuthenticated } = useAuth();

  const post = useSelector(selectPost(postId));
  const curText = useSelector(selectPostText(postId));
  const createdAt = useSelector(selectPostCreatedAt(postId));
  const [relativeTime, setRelativeTime] = useState(moment(createdAt).fromNow());

  // Update relative time every second if needed
  useEffect(() => {
    const timer = setInterval(() => {
      const newRelativeTime = moment(createdAt).fromNow();
      if (newRelativeTime !== relativeTime) {
        setRelativeTime(newRelativeTime);
      }
    }, 1000);

    return () => clearInterval(timer);
  }, [createdAt, relativeTime]);

  // Menu state and handlers
  const [anchorEl, setAnchorEl] = useState(null);
  const open = Boolean(anchorEl);
  const handleMenuClick = (event) => {
    setAnchorEl(event.currentTarget);
  };
  const handleMenuClose = () => {
    setAnchorEl(null);
  };

  const [areCommentsShown, setAreCommentsShown] = useState(false);

  const onPostEdit = () => {
    navigate(editPostUrl.replace(':postId', postId));
    handleMenuClose();
  };

  const onPostRemove = () => {
    dispatch(postRemove({ postId, apiClient }));
    handleMenuClose();
  };

  const onNewTab = () => {
    navigate(`/posts/${postId}`);
    handleMenuClose();
  };

  const swapIsCommentShown = () => setAreCommentsShown(!areCommentsShown);

  let canModifyPost = false;
  if (isAuthenticated) {
    canModifyPost = user.id === post.author.id;
  }

  const fontSize = '14px';

  return (
    <>
      <div className={style.postHeader}>
        <div className={style.authorInfo}>
          <Avatar
            src={post.author.profileIconUrl || defaultAvatar}
            alt={post.author.displayedName}
            size="sm"
          />
          <div className={style.authorMeta}>
            <div className={style.authorName}>{post.author.displayedName}</div>
            <div className={style.postDate}>{relativeTime}</div>
          </div>
        </div>
        <div className={style.menuButton}>
          <IconButton
            aria-label="more"
            id="post-menu-button"
            aria-controls={open ? "post-menu" : undefined}
            aria-expanded={open ? "true" : undefined}
            aria-haspopup="true"
            onClick={handleMenuClick}
          >
            <svg
              width="24"
              height="24"
              viewBox="0 0 24 24"
              style={{ fill: "currentColor" }}
            >
              <path d="M12 8c1.1 0 2-.9 2-2s-.9-2-2-2-2 .9-2 2 .9 2 2 2zm0 2c-1.1 0-2 .9-2 2s.9 2 2 2 2-.9 2-2-.9-2-2-2zm0 6c-1.1 0-2 .9-2 2s.9 2 2 2 2-.9 2-2-.9-2-2-2z" />
            </svg>
          </IconButton>
          <Menu
            id="post-menu"
            anchorEl={anchorEl}
            open={open}
            onClose={handleMenuClose}
            MenuListProps={{
              "aria-labelledby": "post-menu-button",
            }}
          >
            <MenuItem onClick={onNewTab}>
              <ListItemIcon>
                <img
                  src={newTabImg}
                  alt="open in new tab"
                  width="20"
                  height="20"
                />
              </ListItemIcon>
              <Typography variant="body2" style={{ fontSize }}>Open full</Typography>
            </MenuItem>
            {canModifyPost && <MenuItem onClick={onPostEdit}>
              <ListItemIcon>
                <img src={editImg} alt="edit" width="20" height="20" />
              </ListItemIcon>
              <Typography variant="body2" style={{ fontSize }}>Edit</Typography>
            </MenuItem>}
            {canModifyPost && <MenuItem onClick={onPostRemove} sx={{ color: "red" }}>
              <ListItemIcon>
                <img
                  src={trashImg}
                  alt="remove"
                  width="20"
                  height="20"
                  style={{
                    filter:
                      "invert(27%) sepia(91%) saturate(2352%) hue-rotate(346deg) brightness(74%) contrast(97%)",
                  }}
                />
              </ListItemIcon>
              <Typography variant="body2" color="error" style={{ fontSize }}>
                Remove
              </Typography>
            </MenuItem>}
          </Menu>
        </div>
      </div>

      <div className={cx('postContent', { dimmed: areCommentsShown })}>
        <div className={style.postMain}>
          {post.attachedImageUrl && (
            <div className={style.postImage}>
              <img src={post.attachedImageUrl} alt="Post attachment" />
            </div>
          )}
          <div className={style.postTitle}>{post.title}</div>
          <div
            className={cx({
              text: !areCommentsShown,
              textBeforeComments: areCommentsShown,
            })}
          >
            {curText}
          </div>

          {areCommentsShown && (
            <div className={cx('commentsOverlay', { visible: areCommentsShown })}>
              <Comments post={post} onCommentsClose={swapIsCommentShown} />
              <CommentsForm postId={postId} />
            </div>
          )}
        </div>

        <div className={style.postFooter}>
          {!areCommentsShown && (
            <PostFooterProps
              postId={postId}
              onCommentClick={swapIsCommentShown}
              onPostEdit={onPostEdit}
              isSinglePost={isSinglePost}
            />
          )}
        </div>
      </div>

    </>
  );
}
