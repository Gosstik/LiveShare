import { Link } from "react-router-dom";
import { useEffect, useState } from "react";

import { postsUrl } from "../../api/urls";

import style from "./About.module.scss";

export default function Home() {
  const postsLink = (
    <Link to={postsUrl}>
      <span>here</span>
    </Link>
  );

  return (
    <>
      <div className={style.main}>
        <h1>Welcome!</h1>
        <div>Click {postsLink} to see posts.</div>
      </div>
    </>
  );
}
