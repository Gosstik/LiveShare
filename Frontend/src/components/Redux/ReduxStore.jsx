import { configureStore } from "@reduxjs/toolkit";

import postsReducer from "./Reducers/Posts";
import commentsReducer from "./Reducers/Comments";

const store = configureStore({
  reducer: {
    posts: postsReducer,
    comments: commentsReducer,
  },
  devTools: true,
});

export default store;
