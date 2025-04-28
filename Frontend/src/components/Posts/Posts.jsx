import { React, useEffect } from "react";
import { useDispatch, useSelector } from "react-redux";
import { useParams } from "react-router-dom";

import Post from "./Post";
import LoadingPost from "./LoadingPost";
import SortToggles from "../SortToggles/SortToggles";
import NotFound from "../NotFound/NotFound";
import { PostNotFound } from "../NotFound/NotFound";
import { useApi } from "../ApiProvider/ApiProvider";

import {
  postsLoading,
  postsLoad,
  postsSort,
  selectPost,
} from "../Redux/Reducers/Posts";
import {
  selectPostEls,
  selectPostsAreLoading,
  selectPostsLoaded,
  selectPostsLoadFailed,
  selectPostsSortToggles,
} from "../Redux/Reducers/Posts";

import style from "./Posts.module.scss";

const filterById = (postId) => (post) => Number(post.postId) === Number(postId);

export default function Posts() {
  const dispatch = useDispatch();
  const apiClient = useApi();

  // Handle single post

  const params = useParams();
  const postId = params?.postId ?? null;
  const isSinglePost = postId !== null;

  // Loading

  const areLoading = useSelector(selectPostsAreLoading);
  const areLoaded = useSelector(selectPostsLoaded);
  const isLoadFailed = useSelector(selectPostsLoadFailed);
  if (!areLoaded && !areLoading && !isLoadFailed) {
    dispatch(postsLoad(apiClient));
    dispatch(
      postsLoading({
        loadingPosts: Array(isSinglePost ? 1 : 5).fill(null),
      })
    );
  }

  const postEls = useSelector(selectPostEls);
  const post = useSelector(selectPost(postId));

  // Log single post

  useEffect(() => {
    if (isSinglePost && areLoaded) {
      console.groupCollapsed(`Visit post with postId=${postId}`);

      console.groupCollapsed("title");
      console.log(post.title);
      console.groupEnd();

      console.groupCollapsed("createdAt");
      console.log(post.createdAt);
      console.groupEnd();

      console.groupCollapsed("post");
      console.log(post);
      console.groupEnd();

      console.groupEnd();
    }
  }, [areLoaded]); // eslint-disable-line react-hooks/exhaustive-deps

  if (isLoadFailed) {
    // TODO: 500
    return (
      <div className={style.postLoadFailedContainer}>
        <div className={style.postLoadFailed}>
          Something went wrong :(
          <br />
          Try to reload page.
        </div>
      </div>
    );
  }

  // Choose posts filter

  const filter = isSinglePost ? filterById(postId) : () => true;
  const filteredPosts = areLoaded ? postEls.filter(filter) : postEls;

  if (areLoaded && isSinglePost && filteredPosts.length === 0) {
    return <NotFound messageComponent={() => PostNotFound({ postId })} />;
  }

  return (
    <div className={style.posts}>
      {!isSinglePost && (
        <div className={style.postsHeader}>
          <div className={style.postsSortToggles}>
            <SortToggles
              sortReducer={(payload) => dispatch(postsSort(payload))}
              sortTogglesSelector={selectPostsSortToggles}
              togglesData={[
                { name: "date", fieldName: "createdAt" },
                { name: "likes", fieldName: "likes" },
              ]}
              togglesStyle={style}
            />
          </div>
        </div>
      )}

      <div className={style.postsMain}>
        {filteredPosts.map((post, index) => {
          if (post === null) {
            return <LoadingPost key={-index} />;
          }
          return (
            <div className={style.post} key={post.postId}>
              <Post postId={post.postId} isSinglePost={isSinglePost} />
            </div>
          );
        })}
      </div>
    </div>
  );
}
