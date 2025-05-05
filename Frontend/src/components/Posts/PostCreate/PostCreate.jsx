import React, { useState, useRef, useEffect } from 'react';
import styles from './PostCreate.module.scss';
import { useApi } from '../../ApiProvider/ApiProvider';
import { adjustTextareaHeight } from '../../utils';

const PostCreate = () => {
  const [title, setTitle] = useState('');
  const textareaRef = useRef(null);
  const [textContent, setTextContent] = useState('');

  useEffect(() => {
    if (textareaRef.current) {
      adjustTextareaHeight(textareaRef.current);
    }
  }, []);
  const [attachedImage, setAttachedImage] = useState(null);
  const [error, setError] = useState(null);
  const apiClient = useApi();

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
      await apiClient.postsV1PostCreate(formData);
      // Clear form after successful submission
      setTitle('');
      setTextContent('');
      setAttachedImage(null);
      // Reset file input
      const fileInput = document.querySelector('input[type="file"]');
      if (fileInput) fileInput.value = '';
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
      <h2>Create New Post</h2>
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
            ref={textareaRef}
            onChange={(e) => {
              setTextContent(e.target.value);
              adjustTextareaHeight(e.target);
            }}
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

export default PostCreate;
