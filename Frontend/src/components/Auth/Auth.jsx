import { useNavigate } from "react-router-dom";
import { useApi } from "../ApiProvider/ApiProvider";
import { ENV } from "../../config";

// https://oauth.yandex.ru/
// https://console.cloud.google.com/auth
// https://console.cloud.google.com/apis/credentials
export const googleOAuthOnClick = () => {
  try {
    // TODO: replace localhost with backend constant
    window.location.assign(`${ENV.BACKEND_BASE_URL}/auth/oauth/google/redirect`);
  } catch (err) {
    console.log("Failed to redirect to google oauth");
    console.log(err);
  }
};
