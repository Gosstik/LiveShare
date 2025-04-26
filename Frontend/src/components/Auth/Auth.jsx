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

export default function Auth() {
  console.log("Auth start");

  // const [scriptIsAdded, setScriptIsAdded] = useState(false);

  // useEffect(() => {
  //   const script = document.createElement("script");

  //   script.src =
  //     "https://yastatic.net/s3/passport-sdk/autofill/v1/sdk-suggest-with-polyfills-latest.js";
  //   script.async = true;

  //   document.body.appendChild(script);

  //   setScriptIsAdded(true);

  //   return () => {
  //     document.body.removeChild(script);
  //   };
  // }, []);

  // useEffect(() => {
  //   if (!scriptIsAdded) {
  //     console.log("!!! !scriptIsAdded");
  //     return;
  //   }
  //   if (!window.YaAuthSuggest) {
  //     console.log("!!! !window.YaAuthSuggest");
  //   }
  //   window.YaAuthSuggest.init(
  //     {
  //       client_id: "72c9e0f728954a2e9b4ebf26ae35d248",
  //       response_type: "token",
  //       redirect_uri: `http://localhost:3000${authRedirectUrl}`,
  //     },
  //     "http://localhost:3000",
  //     {
  //       view: "button",
  //       parentId: "buttonContainerId",
  //       buttonSize: "m",
  //       buttonView: "main",
  //       buttonTheme: "light",
  //       buttonBorderRadius: "0",
  //       buttonIcon: "ya",
  //     }
  //   )
  //     .then(({ handler }) => handler())
  //     .then((data) => console.log("Сообщение с токеном", data))
  //     .catch((error) => console.log("Обработка ошибки", error));
  // }, [scriptIsAdded]);

  //////////////////////////////////

  console.log("Auth after");

  // https://oauth.yandex.ru/
  // https://console.cloud.google.com/auth
  // https://console.cloud.google.com/apis/credentials
  const googleOAuthOnClick = async () => {
    console.log("start googleOAuthOnClick");

    // Gets authentication url from backend server
    try {
      console.log(1);
      // const data = await fetch(`${authBackendUrl}/api/auth/oauth/google`); # TODO: remove
    //   const data = await fetch(`http://localhost:8000/auth/oauth/google/url`); // Django
      window.location.assign(`http://localhost:8000/auth/oauth/google/redirect`);

      //// Previous flow
      // const data = await fetch(`http://localhost:8000/auth/oauth/google/redirect`); // Django

      // console.log(`####### returned redirect`)
      // console.log(`####### data=${JSON.stringify(data)}`)
      // console.log(`!!! received: JSON.stringify(data)=${JSON.stringify(data)}`);
      // const body = await data.json();
      // console.log(2);
      // console.log(`!!! JSON.stringify(body)=${JSON.stringify(body)}`);
      // console.log(3);
      // window.location.assign(body.url);
    } catch (err) {
      console.log("failed to make request to api/auth/oauth/google");
      console.log(err);
    }

    // const form = document.createElement('form');

    // form.setAttribute('method', 'GET'); // Send as a GET request.
    // form.setAttribute('action', `${authBackendUrl}/api/auth/oauth/google`);

    // document.body.appendChild(form);
    // form.submit();
  };

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
