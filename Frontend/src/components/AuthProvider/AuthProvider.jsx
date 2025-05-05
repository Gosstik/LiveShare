import React, {
  createContext,
  useCallback,
  useContext,
  useEffect,
  useState,
} from "react";
import Cookies from "js-cookie";

import { ENV } from "../../config";

import {
  saveAccessTokenData,
  saveRefreshTokenData,
  isAccessTokenExpired,
  isRefreshedTokenExpired,
  removeTokensData,
} from "./Tokens";
import { exploreUrl } from "../../api/urls";

////////////////////////////////////////////////////////////////////////////////

//// For authenticate functions (oauth, signin, signup)

export const updateTokensInLocalStorage = async (
  onError = () => {},
  refreshTokens = false
) => {
  const apiAuthInfo = new ApiAuthInfo();
  const userInfoResponse = refreshTokens
    ? await apiAuthInfo.refreshUserTokens()
    : await apiAuthInfo.getAuthUserInfo();
  if (userInfoResponse.status !== 200) {
    onError();
    return null;
  }

  const userInfoJson = await userInfoResponse.json();
  const { accessTokenExpiration, refreshTokenExpiration, user } = userInfoJson;

  saveAccessTokenData(accessTokenExpiration.secondsLeft);
  saveRefreshTokenData(refreshTokenExpiration.secondsLeft);

  return user;
};

////////////////////////////////////////////////////////////////////////////////

//// ApiAuthInfo

export class ApiAuthInfo {
  constructor() {
    this.headers = {
      "x-csrftoken": Cookies.get("csrftoken"),
    };
  }

  async getAuthUserInfo() {
    return fetch(`${ENV.BACKEND_BASE_URL}/auth/user/info`, {
      method: "GET",
      headers: this.headers,
      credentials: "include",
      // credentials: "same-origin",
    });
  }

  async refreshUserTokens() {
    return fetch(`${ENV.BACKEND_BASE_URL}/auth/token/refresh`, {
      method: "POST",
      headers: this.headers,
      credentials: "include",
      // credentials: "same-origin",
    });
  }
}

// TODO: remove export
export class UserData {
  // TODO: replace all with null
  constructor() {
    this.id = 0;
    this.email = "";
    this.firstName = "";
    this.lastName = "";
    this.profileIconUrl = null;
  }
}

const initialUserData = new UserData();

export const LoginStates = {
  AUTH_LOADING: "auth_loading",
  AUTHENTICATED: "authenticated",
  GUEST: "guest",
};

// export const AuthContext = createContext({
//   userData: initialUserData,
//   setUserData: (value) => {},
// });

export const AuthContext = createContext();

export function AuthProvider({ children }) {
  // TODO: add SetPeriod to automatically refresh tokens
  const [loginState, setLoginState] = useState(LoginStates.AUTH_LOADING);
  const [user, setUser] = useState(initialUserData);

  const isAuthenticated = loginState === LoginStates.AUTHENTICATED;
  const isGuest = loginState === LoginStates.GUEST;
  const isAuthLoading = loginState === LoginStates.AUTH_LOADING;

  const updateLoginState = useCallback(async () => {
    // Check if refresh token is expired
    if (isRefreshedTokenExpired()) {
      setLoginState(LoginStates.GUEST);
      return;
    }

    // Get user info (and update access token if it is expired)
    let user = null;
    if (isAccessTokenExpired()) {
      user = await updateTokensInLocalStorage(
        () => setLoginState(LoginStates.GUEST),
        true
      );
    } else {
      user = await updateTokensInLocalStorage(() =>
        setLoginState(LoginStates.GUEST)
      );
    }

    if (user !== null) {
      setLoginState(LoginStates.AUTHENTICATED);
      setUser(user);
    }
  }, []);

  const logoutUser = () => {
    removeTokensData();
    window.location.href = `${ENV.FRONTEND_BASE_URL}${exploreUrl}`
  };

  useEffect(() => {
    updateLoginState();
  }, [updateLoginState]);

  return (
    <AuthContext.Provider
      value={{
        isAuthenticated,
        isGuest,
        isAuthLoading,
        updateLoginState,
        logoutUser,
        user,
      }}
    >
      {children}
    </AuthContext.Provider>
  );
}

// Hook for using Auth provider
export const useAuth = () => {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error("useAuth must be used within an AuthProvider");
  }
  return context;
};
