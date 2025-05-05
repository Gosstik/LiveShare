import React, { useContext } from "react";
import Cookies from "js-cookie";
import { useNavigate } from "react-router-dom";

import Avatar from "@mui/joy/Avatar";
import Box from "@mui/joy/Box";

import style from "./Header.module.scss";

import { AuthContext } from "../AuthProvider/AuthProvider";
import { useAuth } from "../AuthProvider/AuthProvider";
import { useApi } from "../ApiProvider/ApiProvider";

import defaultAvatar from "../../images/default-avatar.png";
import src from "@emotion/styled";
import {
  createPostUrl,
  exploreUrl,
  homeUrl,
  signinUrl,
  signupUrl,
} from "../../api/urls";

export default function Header() {
  const { user, isAuthenticated, isGuest, isAuthLoading, logoutUser } =
    useAuth();
  const apiClient = useApi();

  const navigate = useNavigate();

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
        <button
          className={style.simpleButton}
          onClick={() => navigate(exploreUrl)}
        >
          Explore
        </button>
        <button
          className={style.simpleButton}
          onClick={() => navigate(homeUrl)}
        >
          Home
        </button>
        <button
          className={style.createPostButton}
          onClick={() => navigate(createPostUrl)}
        >
          Create post
        </button>
        {isGuest && (
          <button
            className={style.loginButton}
            onClick={() => navigate(signinUrl)}
          >
            Sign in
          </button>
        )}
        {isGuest && (
          <button
            className={style.loginButton}
            onClick={() => navigate(signupUrl)}
          >
            Sign up
          </button>
        )}
        {isAuthenticated && (
          <button className={style.logoutButton} onClick={logout}>
            Logout
          </button>
        )}
        {/* {isAuthenticated && (
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
        )} */}
        {isAuthenticated && (
          <Box sx={{ display: "flex", gap: 1 }}>
            {user?.profileIconUrl ? (
              <Avatar size="sm" src={user?.profileIconUrl} />
            ) : (
              <Avatar />
            )}
            {/* <Avatar>JG</Avatar> */}
            {/* <Avatar alt="Remy Sharp" src="/static/images/avatar/1.jpg" /> */}
          </Box>
        )}
      </div>
    </header>
  );
}
