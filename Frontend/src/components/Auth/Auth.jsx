import style from "./Auth.module.scss";

import { appIconImg, yaEngImg, googleImg } from "../Consts/Consts";
import { authCallbackUrl, authBackendUrl } from "../../api/urls";
import { useContext, useEffect } from "react";
import { AuthContext } from "../AuthProvider/AuthProvider";

function OAuthButton(props) {
  const { icon, name, onClick } = props;
  return (
    <div className={style.oauthButton} onClick={onClick}>
      <img src={icon} alt={name} draggable={false} />
      <div className={style.name}>{name}</div>
    </div>
  );
}

// TODO
// backendUrl = process.env.REACT_APP_BACKEND_URL;
// const backendUrl = `http://localhost:3000`;
// const authBackendUrl = `http://localhost:5000`;

const yandexOAuthOnClick = async () => {
  console.log("start yandexOAuthOnClick");

  const form = document.createElement("form");

  form.setAttribute("method", "GET"); // Send as a GET request.
  form.setAttribute("action", `${authBackendUrl}/api/auth/oauth/yandex`);

  document.body.appendChild(form);
  form.submit();
};

// https://oauth.yandex.ru/
// https://console.cloud.google.com/auth
// https://console.cloud.google.com/apis/credentials
export const googleOAuthOnClick = () => {
  console.log("!!! start googleOAuthOnClick");

  try {
    // TODO: replace localhost with backend constant
    window.location.assign(`http://localhost:8000/auth/oauth/google/redirect`);
  } catch (err) {
    console.log("Failed to redirect to google oauth");
    console.log(err);
  }
};

export default function Auth() {
  console.log("Auth start");

  console.log("Auth after");

  const { user, loggedIn, checkLoginState } = useContext(AuthContext);

  useEffect(() => {
    (async () => {
      if (loggedIn === true) {
        try {
          // Get posts from server
          const {
            data: { my_data },
          } = await fetch(`${authBackendUrl}/user/info`, { method: "GET" });
          console.log(`received: my_data=${my_data}`);
        } catch (err) {
          console.error(err);
        }
      }
    })();
  }, [loggedIn]);

  return (
    <div className={style.mainContent}>
      {loggedIn && <div>You are already logged in !!!</div>}
      <img
        className={style.appIcon}
        src={appIconImg}
        alt={"app-icon"}
        draggable={false}
      />
      {/* <h1 className={style.mainText}>Welcome to LiveShare!</h1> */}
      <h1 className={style.mainText}>Choose way to authorize:</h1>
      <div className={style.oauthButtons}>
        {/* <OAuthButton
          icon={yaEngImg}
          name={"Yandex ID"}
          onClick={yandexOAuthOnClick}
        /> */}
        <OAuthButton
          icon={googleImg}
          name={"Google"}
          onClick={googleOAuthOnClick}
        />
      </div>
    </div>
  );
}
