import { ENV } from "../../config";

const TOKEN_STORAGE_KEY = {
  ACCESS: "access_token_data",
  REFRESH: "refresh_token_data",
};

const saveTokenData = (type, secondsLeft) => {
  const data = {
    last_update_time: new Date().getTime(),
    seconds_left: secondsLeft,
  };
  localStorage.setItem(type, JSON.stringify(data));
};

const saveAccessTokenData = (secondsLeft) => saveTokenData(TOKEN_STORAGE_KEY.ACCESS, secondsLeft);
const saveRefreshTokenData = (secondsLeft) => saveTokenData(TOKEN_STORAGE_KEY.REFRESH, secondsLeft);

const getTokenData = (type) => {
  const data = localStorage.getItem(type);
  if (!data) return null;
  return JSON.parse(data);
};

const getAccessTokenData = () => getTokenData(TOKEN_STORAGE_KEY.ACCESS);
const getRefreshTokenData = () => getTokenData(TOKEN_STORAGE_KEY.REFRESH);

const isTokenExpired = (tokenData, bufferSeconds = 0) => {
  if (!tokenData) {
    return true;
  }
  const now = new Date().getTime();
  const expirationTime =
    tokenData.last_update_time + tokenData.seconds_left * 1000;
  return now > expirationTime - bufferSeconds * 1000;
};

const isAccessTokenExpired = () => isTokenExpired(TOKEN_STORAGE_KEY.ACCESS, ENV.ACCESS_TOKEN_BUFFER_SEC);
const isRefreshedTokenExpired = () => isTokenExpired(TOKEN_STORAGE_KEY.REFRESH);

const removeTokensData = () => {
  localStorage.removeItem(TOKEN_STORAGE_KEY.ACCESS);
  localStorage.removeItem(TOKEN_STORAGE_KEY.REFRESH);
}

export {
  saveAccessTokenData,
  saveRefreshTokenData,
  getAccessTokenData,
  getRefreshTokenData,
  isAccessTokenExpired,
  isRefreshedTokenExpired,
  removeTokensData,
}
