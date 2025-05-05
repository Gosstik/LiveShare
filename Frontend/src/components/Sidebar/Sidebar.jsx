// TODO: blackout

import React, { useState, useRef, useEffect } from "react";

import { useNavigate } from "react-router-dom";

import classNames from "classnames/bind";

import { Settings } from "lucide-react";

import style from "./Sidebar.module.scss";
import { current } from "@reduxjs/toolkit";

import {
  homeUrl,
  createPostUrl,
  friendsUrl,
  exploreUrl,
} from "../../api/urls";

const cx = classNames.bind(style);

export default function Sidebar({ children }) {
  const navigate = useNavigate();
  const [isSidebarOpened, setIsSidebarOpened] = useState(false);
  const sidebar = useRef(null);

  const openSidebar = () => {
    // console.log("OPEN SIDEBAR");
    sidebar.current.classList.add("opened");
    setIsSidebarOpened(true);
  };
  const closeSidebar = () => {
    if (isSidebarOpened) {
      // console.log("CLOSE SIDEBAR");
      sidebar.current.classList.remove("opened");
      setIsSidebarOpened(false);
    }
  };

  useEffect(() => {
    const sidebarElem = sidebar.current;
    sidebarElem.addEventListener("mouseenter", openSidebar);
    sidebarElem.addEventListener("mouseleave", closeSidebar);
    return () => {
      sidebarElem.removeEventListener("mouseenter", openSidebar);
      sidebarElem.removeEventListener("mouseleave", closeSidebar);
    };
  }, [sidebar, isSidebarOpened]);

  return (
    <div
      className={cx(style.sidebar, { opened: isSidebarOpened })}
      ref={sidebar}
    >
      <div className={style.menuButtonBlock}>
        <div className={style.menuButton}>
          <div className={style.menuIcon}></div>
        </div>
      </div>
      <ul>
        <li>
          <div onClick={() => navigate(homeUrl)}>Home</div>
        </li>
        <li>
          <div onClick={() => navigate(exploreUrl)}>Explore</div>
        </li>
        <li>
          <div onClick={() => navigate(createPostUrl)}>Create Post</div>
        </li>
        <li>
          <div onClick={() => navigate(friendsUrl)}>Friends</div>
        </li>
        {/* TODO: About, SignIn, SignUp */}
      </ul>
    </div>
  );
}
