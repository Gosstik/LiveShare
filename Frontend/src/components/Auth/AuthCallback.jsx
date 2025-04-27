import { useContext, useEffect, useRef, useState } from "react";

import { signinUrl } from "../../api/urls";
import { current } from "@reduxjs/toolkit";
import { useNavigate } from "react-router-dom";
import { AuthContext } from "../AuthProvider/AuthProvider";

import { authBackendUrl } from "../../api/urls";

export default function AuthCallback() {
  console.log("AuthCallback start");

  //////////////////////////////////

  // if (!window.YaSendSuggestToken) {
  //   console.log(`!!! NOT AN OBJECT`)
  //   console.log(`window.YaSendSuggestToken=${window.YaSendSuggestToken}`)
  //   return <div>NOT AN OBJECT</div>;
  // }

  // window.YaSendSuggestToken(`http://localhost:3000${authUrl}`, {
  //   flag: true,
  //   kek: true,
  // });

  const called = useRef(false);
  const { checkLoginState, loggedIn } = useContext(AuthContext);
  const navigate = useNavigate();
  useEffect(() => {
    console.log(`AuthCallback start useEffect`);
    (async () => {
      console.log(`inside async: loggedIn=${loggedIn}`);
      if (loggedIn === false) {
        console.log("inside if loggedIn === false");
        try {
          console.log("start try");
          if (called.current) return; // prevent rerender caused by StrictMode
          console.log("called.current");
          called.current = true;
          console.log(`http://localhost:8000/auth/oauth/google/token/login${window.location.search}`)
          const res = await fetch(
            // `${authBackendUrl}/auth/token${window.location.search}`,
            `http://localhost:8000/auth/oauth/google/token/login${window.location.search}`,
            {
              method: "GET",
              credentials: "include",
            }
          );
          console.log("response: ", res);
          checkLoginState();
          navigate("/");
        } catch (err) {
          console.error("err in async", err);
          navigate("/");
        }
      } else if (loggedIn === true) {
        navigate("/");
      }
    })();
  }, [checkLoginState, loggedIn, navigate]);

  // fetch(``).then(() => {
  //   console.log("AuthCallback fetch finished");
  // });

  console.log("AuthCallback finished");

  return <div>Auth redirection...</div>;
}
