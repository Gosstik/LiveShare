import { useContext, useEffect, useRef, useState } from "react";

import { signinUrl } from "../../api/urls";
import { current } from "@reduxjs/toolkit";
import { useNavigate } from "react-router-dom";
import { AuthContext, LoginStates } from "../AuthProvider/AuthProvider";
import { useAuth } from "../AuthProvider/AuthProvider";

import { afterAuthPath } from "../../api/urls";

import {
  updateTokensInLocalStorage,
} from "../AuthProvider/AuthProvider";

export default function AuthCallback() {
  const navigate = useNavigate();
  const { updateLoginState } = useAuth();

  useEffect(() => {
    const fetchUserInfo = async () => {
      console.log(`AuthCallback start useEffect`);

      await updateTokensInLocalStorage();
      updateLoginState();
      navigate(afterAuthPath);
    };

    fetchUserInfo();
  // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  console.log("AuthCallback finished");

  return <div>Auth redirection...</div>;
}
