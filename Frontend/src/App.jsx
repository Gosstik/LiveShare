import { React } from "react";

import { BrowserRouter, Route, Routes } from "react-router-dom";

// import "./api/server";

import {
  homeUrl,
  aboutUrl,
  signinUrl,
  authCallbackUrl,
  postsUrl,
  postUrl,
  postCreateUrl,
  signupUrl,
  exploreUrl,
  singlePostUrl,
  createPostUrl,
  editPostUrl,
  friendsUrl,
} from "./api/urls";

import Sidebar from "./components/Sidebar/Sidebar";

import Header from "./components/Header/Header";
import Posts from "./components/Posts/Posts";
import PostRouterWrapper from "./components/Posts/PostRouterWrapper";
import NotFound from "./components/NotFound/NotFound";
import About from "./components/About/About";
import Signin from "./components/Auth/Signin";
import Signup from "./components/Auth/Signup";
import TestComponent from "./components/TestComponent/TestComponent";
import PostShow from "./components/Posts/PostShow/PostShow";
import AuthCallback from "./components/Auth/AuthCallback";

////////////////////////
//// New components

import Home from "./components/Home/Home";
// import Explore from "./components/Explore/Explore";
import SinglePost from "./components/SinglePost/SinglePost";
import CreatePost from "./components/CreatePost/CreatePost";
import EditPost from "./components/EditPost/EditPost";
import Friends from "./components/Friends/Friends";

////////////////////////

// import NavigationBar from "./components/NavigationBar/NavigationBar"
import { AuthProvider } from "./components/AuthProvider/AuthProvider";
import { ApiProvider } from "./components/ApiProvider/ApiProvider";

import { UrlNotFound } from "./components/NotFound/NotFound";

import style from "./components/Sidebar/Sidebar.module.scss";

import { ENV } from "./config";

function App() {
  console.log(`You are running this application in ${ENV.NODE_ENV} mode.`)
  return (
    <AuthProvider>
      <ApiProvider>
        <BrowserRouter>
          <Sidebar />
          <div className={style.bodyOutOfSidebar}>
            <Header />
            {/* <NavigationBar /> */}
            <Routes>
              {/* New components */}
              <Route path={homeUrl} element={<Home />} />
              {/* <Route path={exploreUrl} element={<Explore />} /> */}
              <Route path={exploreUrl} element={<Posts />} />
              <Route path={singlePostUrl} element={<SinglePost />} />
              <Route path={createPostUrl} element={<CreatePost />} />
              <Route path={editPostUrl} element={<EditPost />} />
              <Route path={friendsUrl} element={<Friends />} />

              <Route path={aboutUrl} element={<About />} />

              {/* Auth */}

              <Route path={signinUrl} element={<Signin />} />
              <Route path={signupUrl} element={<Signup />} />
              <Route
                path={authCallbackUrl}
                element={<AuthCallback />}
              />

              {/* TODO: About, Not Found */}

              {/* Old components */}

              {/* <Route path={postUrl} element={<PostRouterWrapper />}></Route> */}
              <Route path={postUrl} element={<PostShow />}></Route>

              <Route path={"/test"} element={<TestComponent />}></Route>

              <Route
                path="*"
                element={<NotFound messageComponent={UrlNotFound} />}
              ></Route>
            </Routes>
          </div>
        </BrowserRouter>
      </ApiProvider>
    </AuthProvider>
  );
}

export default App;
