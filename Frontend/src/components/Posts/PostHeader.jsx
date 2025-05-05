import { React, useState, useEffect } from "react";
import { useSelector, useDispatch } from "react-redux";
import { useNavigate } from "react-router-dom";

import TextField from "@mui/material/TextField";
import InputAdornment from "@mui/material/InputAdornment";
import FormControl from "@mui/material/FormControl";
import Select from "@mui/material/Select";
import MenuItem from "@mui/material/MenuItem";
import InputLabel from "@mui/material/InputLabel";

import IssueAuth from "../Modal/IssueAuth";
import { selectPostTitle } from "../Redux/Reducers/Posts";
import { useAuth } from "../AuthProvider/AuthProvider";
import { useApi } from "../ApiProvider/ApiProvider";
import { postsLoad } from "../Redux/Reducers/Posts";

import style from "./PostHeader.module.scss";

import {
  trashImg,
  newTabImg,
  searchImg,
  arrowUpImg,
  arrowDownImg,
} from "../Consts/Consts";

let searchTimeout = null;

export default function PostHeader(props) {
  const { postId, isSinglePost, onPostRemove, userId } = props;
  const dispatch = useDispatch();
  const apiClient = useApi();

  const { isAuthenticated } = useAuth();
  const title = useSelector((state) =>
    postId ? selectPostTitle(postId)(state) : null
  );

  const navigate = useNavigate();
  const onNewTab = () => navigate(`/posts/${postId}`);

  const [isModalOpened, setIsModalOpened] = useState(false);
  const openModal = () => setIsModalOpened(true);
  const closeModal = () => setIsModalOpened(false);

  // New state for filters
  const [searchText, setSearchText] = useState("");
  const [sortField, setSortField] = useState("");
  const [sortOrder, setSortOrder] = useState("desc");

  const makeRequestParams = () => {
    const requestParams = {
      apiClient,
    };

    if (userId) {
      requestParams.author_id = userId;
    }

    if (sortOrder) {
      requestParams.sort_type = sortOrder;
    }

    if (searchText.trim()) {
      requestParams.post_title_search_str = searchText;
    }

    if (sortField) {
      requestParams.sort_field_name = sortField;
    }

    return requestParams;
  };

  const loadPosts = (params = {}) => {
    const requestParams = makeRequestParams();
    dispatch(postsLoad(requestParams));
  };

  // Handle search with debounce
  useEffect(() => {
    if (searchTimeout) {
      clearTimeout(searchTimeout);
    }

    searchTimeout = setTimeout(() => {
      loadPosts();
    }, 500);

    return () => {
      if (searchTimeout) {
        clearTimeout(searchTimeout);
      }
    };
  }, [searchText]); // eslint-disable-line react-hooks/exhaustive-deps

  // Handle search without debounce
  useEffect(() => {
    loadPosts();
  }, [sortField, sortOrder]); // eslint-disable-line react-hooks/exhaustive-deps

  const handleSortFieldChange = (event) => {
    const newSortField = event.target.value;
    setSortField(newSortField);
  };

  const toggleSortOrder = () => {
    const newSortOrder = sortOrder === "asc" ? "desc" : "asc";
    setSortOrder(newSortOrder);
  };

  if (isSinglePost && title) {
    return (
      <div className={style.postHeader}>
        <div className={style.title}> {title} </div>
        <div className={style.rightProps}>
          <img
            src={trashImg}
            alt={"remove post"}
            onClick={isAuthenticated ? onPostRemove : openModal}
            draggable="false"
          />
          {isModalOpened && <IssueAuth onOkClick={closeModal} />}
        </div>
      </div>
    );
  }

  const fontSize = '14px';

  // List view - only show filters
  return (
    <div className={style.postHeader}>
      <div className={style.filters}>
        <div className={style.leftFilters}>
          <div className={style.sortOrder} onClick={toggleSortOrder}>
            <img
              src={sortOrder === "asc" ? arrowUpImg : arrowDownImg}
              alt={sortOrder === "asc" ? "Sort ascending" : "Sort descending"}
            />
          </div>

          <TextField
            placeholder="Search by title"
            value={searchText}
            onChange={(e) => setSearchText(e.target.value)}
            InputProps={{
              startAdornment: (
                <InputAdornment position="start">
                  <img src={searchImg} alt="Search" />
                </InputAdornment>
              ),
              style: { fontSize }
            }}
            size="small"
          />
        </div>

        <div className={style.rightFilters}>
          <FormControl sx={{ minWidth: 120 }} size="small">
            <InputLabel style={{ fontSize }}>Sort by</InputLabel>
            <Select
              value={sortField}
              label="Sort by"
              onChange={handleSortFieldChange}
              style={{ fontSize }}
            >
              <MenuItem value="" style={{ fontSize }}>None</MenuItem>
              <MenuItem value="created_at" style={{ fontSize }}>Date</MenuItem>
              <MenuItem value="likes_count" style={{ fontSize }}>Likes</MenuItem>
              <MenuItem value="comments_count" style={{ fontSize }}>Comments</MenuItem>
            </Select>
          </FormControl>
        </div>
      </div>
    </div>
  );
}
