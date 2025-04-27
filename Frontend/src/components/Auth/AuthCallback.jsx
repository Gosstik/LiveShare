import { useEffect } from "react";

import { useNavigate } from "react-router-dom";
import { useAuth } from "../AuthProvider/AuthProvider";

import { afterAuthPath } from "../../api/urls";

import { updateTokensInLocalStorage } from "../AuthProvider/AuthProvider";

export default function AuthCallback() {
  const navigate = useNavigate();
  const { updateLoginState } = useAuth();

  useEffect(() => {
    const fetchUserInfo = async () => {
      await updateTokensInLocalStorage();
      updateLoginState();
      navigate(afterAuthPath);
    };

    fetchUserInfo();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  return <div>Auth redirection...</div>;
}
