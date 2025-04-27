import style from "./Auth.module.scss";

import { appIconImg, yaEngImg, googleImg } from "../Consts/Consts";
import { useContext, useState } from "react";
import { useNavigate } from "react-router-dom";
import { AuthContext } from "../AuthProvider/AuthProvider";

import { googleOAuthOnClick } from "./Auth"

function OAuthButton(props) {
  const { icon, name, onClick } = props;
  return (
    <div className={style.oauthButton} onClick={onClick}>
      <img src={icon} alt={name} draggable={false} />
      <div className={style.name}>{name}</div>
    </div>
  );
}

// TODO
// backendUrl = process.env.REACT_APP_BACKEND_URL;
// const backendUrl = `http://localhost:3000`;
// const authBackendUrl = `http://localhost:5000`;

export default function Signup() {
  const navigate = useNavigate();
  const { user, loggedIn, checkLoginState } = useContext(AuthContext);
  const [formData, setFormData] = useState({
    profileIcon: null,
    firstName: '',
    lastName: '',
    email: '',
    password: '',
    repeatPassword: ''
  });

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value
    }));
  };

  const handleImageChange = (e) => {
    const file = e.target.files[0];
    if (file && file.type === 'image/jpeg') {
      setFormData(prev => ({
        ...prev,
        profileIcon: file
      }));
    }
  };

  const [error, setError] = useState('');

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    
    const formDataToSend = new FormData();
    if (formData.profileIcon) {
      formDataToSend.append('profile_icon', formData.profileIcon);
    }
    formDataToSend.append('first_name', formData.firstName);
    formDataToSend.append('last_name', formData.lastName);
    formDataToSend.append('email', formData.email);
    formDataToSend.append('password', formData.password);

    try {
      const response = await fetch('http://localhost:8000/auth/password/signup', {
        method: 'POST',
        credentials: 'include',
        body: formDataToSend
      });
      
      if (response.ok) {
        // Navigate to home page after successful signup
        navigate('/');
      } else {
        // TODO: change to code
        const data = await response.json();
        if (data.code === 'email_already_exists') {
          // TODO: maybe some additional logic?
          setError(data.detail);
        } else {
          // setError(data.detail);
          setError('Signup failed. Please try again.');
        }
      }
    } catch (error) {
      setError('Error during signup. Please try again.');
      console.error('Error during signup:', error);
    }
  };

  return (
    <div className={style.mainContent}>
      {loggedIn && <div>You are already logged in !!!</div>}
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
      <h1 className={style.mainText}>---- or -----</h1>
      <form onSubmit={handleSubmit} className={style.signupForm}>
        {error && <div className={style.errorMessage}>{error}</div>}
        <div className={style.formField}>
          <label htmlFor="profileIcon">Profile Icon (JPG):</label>
          <input
            type="file"
            id="profileIcon"
            accept=".jpg,image/jpeg"
            onChange={handleImageChange}
          />
        </div>

        <div className={style.formField}>
          <label htmlFor="firstName">First Name:</label>
          <input
            type="text"
            id="firstName"
            name="firstName"
            value={formData.firstName}
            onChange={handleInputChange}
            required
          />
        </div>

        <div className={style.formField}>
          <label htmlFor="lastName">Last Name:</label>
          <input
            type="text"
            id="lastName"
            name="lastName"
            value={formData.lastName}
            onChange={handleInputChange}
            required
          />
        </div>

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

        <div className={style.formField}>
          <label htmlFor="repeatPassword">Repeat Password:</label>
          <input
            type="password"
            id="repeatPassword"
            name="repeatPassword"
            value={formData.repeatPassword}
            onChange={handleInputChange}
            required
          />
        </div>

        <button type="submit" className={style.submitButton}>
          Sign up
        </button>
      </form>
    </div>
  );
}
