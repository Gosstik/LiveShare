import React, { useState, useEffect } from 'react';
import { useNavigate } from "react-router-dom";

import styles from './CreatePost.module.scss';

import { useApi } from "../ApiProvider/ApiProvider"
import { useAuth } from "../AuthProvider/AuthProvider"
import { homeUrl, signinUrl } from '../../api/urls';

export default function CreatePost() {
  const navigate = useNavigate();
  const apiClient = useApi();
  const { isGuest } = useAuth();
  const [title, setTitle] = useState('');
  const [textContent, setTextContent] = useState('');
  const [attachedImage, setAttachedImage] = useState(null);
  const [error, setError] = useState(null);

  useEffect(() => {
    if (isGuest) {
      // TODO: add modal that user has to authorize before creating a post
      navigate(signinUrl);
    }
  }, [isGuest]);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError(null);

    const formData = new FormData();
    formData.append('title', title);
    formData.append('text_content', textContent);
    if (attachedImage) {
      formData.append('attached_image', attachedImage);
    }

    try {
      apiClient.postsV1PostCreate(formData);
      navigate(homeUrl);
      // // Clear form after successful submission
      // setTitle('');
      // setTextContent('');
      // setAttachedImage(null);
      // // Reset file input
      // const fileInput = document.querySelector('input[type="file"]');
      // if (fileInput) fileInput.value = '';
    } catch (err) {
      setError(err.response?.data?.error || 'An error occurred while creating the post');
    }
  };

  const handleImageChange = (e) => {
    if (e.target.files && e.target.files[0]) {
      setAttachedImage(e.target.files[0]);
    }
  };

  return (
    <div className={styles.container}>
      <h2 className={styles.createPostTitle}>Create New Post</h2>
      {error && <div className={styles.error}>{error}</div>}
      <form onSubmit={handleSubmit} className={styles.form}>
        <div className={styles.formGroup}>
          <label htmlFor="title">Title:</label>
          <input
            type="text"
            id="title"
            value={title}
            onChange={(e) => setTitle(e.target.value)}
            required
          />
        </div>

        <div className={styles.formGroup}>
          <label htmlFor="textContent">Content:</label>
          <textarea
            id="textContent"
            value={textContent}
            onChange={(e) => setTextContent(e.target.value)}
            required
          />
        </div>

        <div className={styles.formGroup}>
          <label htmlFor="attachedImage">Image (optional):</label>
          <input
            type="file"
            id="attachedImage"
            accept="image/*"
            onChange={handleImageChange}
          />
        </div>

        <button type="submit" className={styles.submitButton}>
          Create Post
        </button>
      </form>
    </div>
  );
};
