import React, { useContext } from "react";
import Cookies from "js-cookie";
import { useNavigate } from "react-router-dom";

import style from "./Header.module.scss";

import { AuthContext } from "../AuthProvider/AuthProvider";

import { authBackendUrl } from "../../api/urls";

function LoginButton() {}

export default function Header() {
  const { user, loggedIn, checkLoginState } = useContext(AuthContext);

  const navigate = useNavigate();

  const posts = () => {
    navigate("/posts");
  };

  const home = () => {
    navigate("/");
  };

  const login = () => {
    navigate("/auth");
  };

  const logout = async () => {
    console.log(`logout cb`);
    if (loggedIn) {
      try {
        // TODO: make client
        // TODO: add csrf header
        const headers = {
          "x-csrftoken": Cookies.get("csrftoken"),
        };
        await fetch(
          // `${authBackendUrl}/auth/logout`,
          `http://localhost:8000/auth/logout`,
          {
            method: "POST",
            headers,
            credentials: "include",
          }
        );
        // Check login state again
        checkLoginState();
      } catch (err) {
        console.error(`!!! logout err: `, err);
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
        {!loggedIn && (
          <button className={style.loginButton} onClick={login}>
            log in
          </button>
        )}
        {loggedIn && (
          <button className={style.logoutButton} onClick={logout}>
            logout
          </button>
        )}
        {loggedIn && (
          <div className={style.loginBlock}>
            <div>Logged as:</div>
            <div>{user.email}</div>
          </div>
        )}
      </div>
    </header>
  );
}
