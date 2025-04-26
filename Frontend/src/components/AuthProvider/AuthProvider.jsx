import React, { createContext, useCallback, useEffect, useState } from "react";
import Cookies from "js-cookie";
import { authBackendUrl } from "../../api/urls";

// /**
//  * User data holder to embed in context
//  */
// export class UserData {
//   /**
//    * Full constructor
//    * @param {number} id User ID
//    * @param {string} firstName User first name
//    * @param {string} lastName User last name
//    * @param {string} patronymic User patronymic
//    * @param {string} email User email
//    * @param {string} defaultRole User default role
//    */
//   constructor(
//       id,
//       firstName = '',
//       lastName = '',
//       patronymic = '',
//       email = '',
//       defaultRole) {
//     this.id = id;
//     this.firstName = firstName;
//     this.lastName = lastName;
//     this.patronymic = patronymic;
//     this.email = email;
//     this.defaultRole = defaultRole;
//   }
// }

export class UserData {
  constructor(my_data) {
    this.email = "";
    this.first_name = "";
    this.last_name = "";
  }
}

const initialUserData = new UserData();

// export const AuthContext = createContext({
//   userData: initialUserData,
//   setUserData: (value) => {},
// });

export const AuthContext = createContext();

export function AuthProvider({ children }) {
  // TODO: use only AuthContext
  // const [userData, setUserData] = useState(initialUserData);

  // const fetchUserData = async () => {
  //   try {
  //     // const response = await fetch(`${backendUrl}/user/info`, {
  //     const response = await fetch(`${backendUrl}/auth/logged_in`, {
  //       method: "GET",
  //       headers: {
  //         "Content-Type": "application/json",
  //       },
  //       credentials: "include",
  //     });

  //     if (!response.ok) {
  //       throw new Error(`HTTP error! Status: ${response.status}`);
  //     }

  //     const data = await response.json();
  //     const user = data.result;

  //     if (user) {
  //       setUserData(new UserData(user.my_data));
  //       // setUserData(new UserData(
  //       //     user.id,
  //       //     user.firstName,
  //       //     user.lastName,
  //       //     user.patronymic,
  //       //     user.email,
  //       //     user.defaultRole
  //       // ));
  //     }
  //   } catch (error) {
  //     console.error("Error fetching user data:", error);
  //   }
  // };

  // useEffect(() => {
  //   if (!userData.my_data) {
  //     fetchUserData();
  //   }
  // }, [userData]);

  // const [userData, setUserData] = useState(initialUserData);
  const [loggedIn, setLoggedIn] = useState(false);
  const [user, setUser] = useState(initialUserData);

  // TODO: remove useCallback
  const checkLoginState = useCallback(async () => {
    try {
      // const {
      //   data: { loggedIn: logged_in, user },
      // } = await axios.get(`${serverUrl}/auth/logged_in`)
      // TODO: add catch
      // const res = await fetch(`${authBackendUrl}/auth/logged_in`, {
      //   method: "GET",
      //   credentials: "include",
      // });
      const headers = {
        "x-csrftoken": Cookies.get("csrftoken"),
      };
      let res = await fetch(`http://localhost:8000/auth/user/info`, {
        method: "GET",
        headers: headers,
        credentials: "include",
        // credentials: "same-origin",
      });

      if (res.status === 401) {
        // TODO: add expiration check before sending
        await fetch(`http://localhost:8000/auth/token/refresh`, {
          method: "POST",
          headers: headers,
          credentials: "include",
          // credentials: "same-origin",
        });

        res = await fetch(`http://localhost:8000/auth/user/info`, {
          method: "GET",
          headers: headers,
          credentials: "include",
          // credentials: "same-origin",
        });
      }

      const isAuthenticated = res.status === 200
      console.log(`logged_in res=${JSON.stringify(res)}`);
      const res_json = await res.json();
      console.log(`logged_in res_json=${res_json}`);

      // const { is_authenticated, user } = res_json;
      const { access_token_expiration, user } = res_json;
      console.log(`!!! access_token_expiration=${JSON.stringify(access_token_expiration)}`)

      console.log(
        `!!! is_authenticated fetched: ${JSON.stringify(isAuthenticated)}`
      );
      console.log(`!!! logged_in fetched (user): ${JSON.stringify(user)}`);
      // TODO
      setLoggedIn(isAuthenticated);
      setUser(user);
    } catch (err) {
      console.error(err);
    }
  }, []);

  useEffect(() => {
    checkLoginState();
  }, [checkLoginState]);

  return (
    <AuthContext.Provider value={{ loggedIn, checkLoginState, user }}>
      {children}
    </AuthContext.Provider>
  );
}
