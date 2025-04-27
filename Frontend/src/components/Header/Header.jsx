import React, { useContext } from "react";
import Cookies from "js-cookie";
import { useNavigate } from "react-router-dom";

import style from "./Header.module.scss";

import { AuthContext } from "../AuthProvider/AuthProvider";
import { useAuth } from "../AuthProvider/AuthProvider";
import { useApi } from "../ApiProvider/ApiProvider";

import defaultAvatar from "../../images/default-avatar.png";


// function LoginButton() {}

export default function Header() {
  // const { user, loggedIn, checkLoginState } = useContext(AuthContext);
  const { user, isAuthenticated, isGuest, isAuthLoading, logoutUser} = useAuth();
  const apiClient = useApi();

  const navigate = useNavigate();

  const posts = () => {
    navigate("/posts");
  };

  const home = () => {
    navigate("/");
  };

  const signin = () => {
    navigate("/signin");
  };

  const signup = () => {
    navigate("/signup");
  };

  const logout = async () => {
    if (isAuthenticated) {
      try {
        apiClient.authLogout();
        logoutUser();
      } catch (err) {
        console.error(`Logout error: ${err}`);
      }
    }
  };

  return (
    <header className={style.header}>
      <div className={style.appTitle}>LiveShare</div>
      <div className={style.buttons}>
        <button className={style.simpleButton} onClick={posts}>
          Posts
        </button>
        <button className={style.simpleButton} onClick={home}>
          Home
        </button>
        <button className={style.createPostButton}>Create post</button>
        {isGuest && (
          <button className={style.loginButton} onClick={signin}>
            Sign in
          </button>
        )}
        {isGuest && (
          <button className={style.loginButton} onClick={signup}>
            Sign up
          </button>
        )}
        {isAuthenticated && (
          <button className={style.logoutButton} onClick={logout}>
            Logout
          </button>
        )}
        {isAuthenticated && (
          <>
            <img
              src={user?.profile_icon_url || defaultAvatar}
              onError={(e) => {
                console.error("Error loading profile icon:", e);
                e.target.src = defaultAvatar;
              }}
              alt="Profile"
              className={style.profileIcon}
              width={50}
              height={50}
            />
            <div>{user?.displayed_name || "Guest"}</div>
          </>
        )}
      </div>
    </header>
  );
}
