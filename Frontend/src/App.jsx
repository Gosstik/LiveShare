import { React } from "react";

import { BrowserRouter, Route, Routes } from "react-router-dom";

// import "./api/server";

import {
  homeUrl,
  signinUrl,
  authCallbackUrl,
  postsUrl,
  postUrl,
  signupUrl,
} from "./api/urls";

import Sidebar from "./components/Sidebar/Sidebar";

import Header from "./components/Header/Header";
import Posts from "./components/Posts/Posts";
import PostRouterWrapper from "./components/Posts/PostRouterWrapper";
import NotFound from "./components/NotFound/NotFound";
import Home from "./components/Home/Home";
import Auth from "./components/Auth/Auth";
import Signin from "./components/Auth/Signin";
import Signup from "./components/Auth/Signup";
import TestComponent from "./components/TestComponent/TestComponent";
// import AuthRedirect from "./components/Auth/AuthRedirect";
import AuthCallback from "./components/Auth/AuthCallback";
// import NavigationBar from "./components/NavigationBar/NavigationBar"
import { AuthProvider } from "./components/AuthProvider/AuthProvider";

import { UrlNotFound } from "./components/NotFound/NotFound";

import style from "./components/Sidebar/Sidebar.module.scss";

function App() {
  return (
    <AuthProvider>
      <BrowserRouter>
        <Sidebar />
        <div className={style.bodyOutOfSidebar}>
          <Header />
          {/* <NavigationBar /> */}
          <Routes>
            <Route path={homeUrl} element={<Home />} />
            <Route path={"/auth"} element={<Auth />} />
            <Route path={signinUrl} element={<Signin />} />
            <Route path={signupUrl} element={<Signup />} />
            <Route
              path={authCallbackUrl}
              element={<AuthCallback />}
              onEnter={() => console.log(`Entered ${authCallbackUrl}`)}
            />

            <Route path={postsUrl} element={<Posts />}></Route>

            <Route path={postUrl} element={<PostRouterWrapper />}></Route>

            <Route path={"/test"} element={<TestComponent />}></Route>

            <Route
              path="*"
              element={<NotFound messageComponent={UrlNotFound} />}
            ></Route>
          </Routes>
        </div>
      </BrowserRouter>
    </AuthProvider>
  );
}

export default App;
