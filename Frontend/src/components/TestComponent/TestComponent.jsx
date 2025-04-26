import { React, useEffect, useContext } from "react";
import { useDispatch, useSelector } from "react-redux";
import { useParams } from "react-router-dom";
import { AuthContext } from "../AuthProvider/AuthProvider";
import { authBackendUrl } from "../../api/urls";
import defaultAvatar from "../../images/default-avatar.png";

import style from "./TestComponent.module.scss";

export default function TestComponent() {
  const { user } = useContext(AuthContext);

  useEffect(() => {
    console.log(`!!! useEffect in TestComponent`)
  }, []); // eslint-disable-line react-hooks/exhaustive-deps

  return (
    <div className={style.outerDiv}>
      <div>I am here!!!</div>
      <div className={style.profileSection}>
        <img 
          src={user?.profile_icon_url || defaultAvatar}
          onError={(e) => {
            console.error('Error loading profile icon:', e);
            e.target.src = defaultAvatar;
          }}
          alt="Profile" 
          className={style.profileIcon}
        />
        <div>{user?.displayed_name || 'Guest'}</div>
      </div>
    </div>
  );
}
