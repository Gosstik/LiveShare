import { useNavigate } from "react-router-dom";
import { useApi } from "../ApiProvider/ApiProvider";

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
