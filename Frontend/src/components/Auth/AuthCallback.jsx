import { useEffect, useState } from "react";

import { useNavigate } from "react-router-dom";
import { useAuth } from "../AuthProvider/AuthProvider";

import { afterAuthPath } from "../../api/urls";

import { updateTokensInLocalStorage } from "../AuthProvider/AuthProvider";

export default function AuthCallback() {
  const navigate = useNavigate();
  const { updateLoginState, isAuthenticated } = useAuth();

  useEffect(() => {
    const fetchUserInfo = async () => {
      await updateTokensInLocalStorage();
      updateLoginState();
    };

    fetchUserInfo();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  useEffect(() => {
    if (isAuthenticated) {
      navigate(afterAuthPath);
    }
  }, [isAuthenticated]);

  return <div>Auth redirection...</div>;
}
