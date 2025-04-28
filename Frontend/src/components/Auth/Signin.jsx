import style from "./Auth.module.scss";

import { appIconImg, yaEngImg, googleImg } from "../Consts/Consts";
import { afterAuthPath } from "../../api/urls";
import React, { useContext, useState } from "react";
import { useNavigate } from "react-router-dom";
import { useApi } from "../ApiProvider/ApiProvider";
import { useAuth, updateTokensInLocalStorage } from "../AuthProvider/AuthProvider";

import Divider from '@mui/joy/Divider';

import { googleOAuthOnClick } from "./Auth";

function OAuthButton(props) {
  const { icon, name, onClick } = props;
  return (
    <div className={style.oauthButton} onClick={onClick}>
      <img src={icon} alt={name} draggable={false} />
      <div className={style.name}>{name}</div>
    </div>
  );
}

export default function Signin() {
  const navigate = useNavigate();
  const apiClient = useApi();

  const { isAuthenticated, updateLoginState } = useAuth();
  const [formData, setFormData] = useState({
    email: '',
    password: ''
  });
  const [error, setError] = useState('');

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');

    try {
      const response = await apiClient.authPasswordSignIn(formData);
      if (response.ok) {
        await updateTokensInLocalStorage();
        updateLoginState();
        navigate(afterAuthPath);
      } else {
        const data = await response.json();
        if (data.code && ['email_does_not_exist', 'invalid_password'].includes(data.code)) {
          setError(data.detail);
        } else {
          setError('Sign in failed. Please try again.');
        }
      }
    } catch (error) {
      setError('Error during sign in. Please try again.');
      console.error('Error during sign in:', error);
    }
  };

  return (
    <div className={style.mainContent}>
      {isAuthenticated && <div>You are already logged in !!!</div>}
      <img
        className={style.appIcon}
        src={appIconImg}
        alt={"app-icon"}
        draggable={false}
      />
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
      <Divider>Visual indicator</Divider>
      <form onSubmit={handleSubmit} className={style.signupForm}>
        {error && <div className={style.errorMessage}>{error}</div>}
        
        <div className={style.formField}>
          <label htmlFor="email">Email:</label>
          <input
            type="email"
            id="email"
            name="email"
            value={formData.email}
            onChange={handleInputChange}
            required
          />
        </div>

        <div className={style.formField}>
          <label htmlFor="password">Password:</label>
          <input
            type="password"
            id="password"
            name="password"
            value={formData.password}
            onChange={handleInputChange}
            required
          />
        </div>

        <button type="submit" className={style.submitButton}>
          Sign in
        </button>
      </form>
    </div>
  );
}
