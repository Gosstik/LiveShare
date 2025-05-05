import React, { useState, useEffect, useRef } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { useSelector, useDispatch } from 'react-redux';
import { selectPost, postsLoad, selectPostsLoaded } from '../Redux/Reducers/Posts';
import { useApi } from '../ApiProvider/ApiProvider';
import { singlePostUrl } from '../../api/urls';
import styles from './EditPost.module.scss';
import { adjustTextareaHeight } from '../utils';

export default function EditPost() {
  const { postId } = useParams();
  const dispatch = useDispatch();
  const navigate = useNavigate();
  const apiClient = useApi();
  
  const post = useSelector(selectPost(postId));
  const postsLoaded = useSelector(selectPostsLoaded);

  useEffect(() => {
    if (!postsLoaded) {
      dispatch(postsLoad({ apiClient, post_id: postId }));
    }
  }, [dispatch, apiClient, postId, postsLoaded]);
  
  const [title, setTitle] = useState('');
  const textareaRef = useRef(null);
  const [textContent, setTextContent] = useState('');
  const [attachedImage, setAttachedImage] = useState(null);
  const [currentImage, setCurrentImage] = useState(null);
  const [error, setError] = useState(null);

  useEffect(() => {
    if (post) {
      setTitle(post.title);
      setTextContent(post.text);
      // Adjust height after content is set
      setTimeout(() => {
        if (textareaRef.current) {
          adjustTextareaHeight(textareaRef.current);
        }
      }, 0);
      setCurrentImage(post.attachedImageUrl);
    }
  }, [post]);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError(null);

    const body = new FormData();
    if (title !== post.title) {
      body.append('title', title);
    }
    if (textContent !== post.text) {
      body.append('text_content', textContent);
    }
    if (attachedImage) {
      body.append('attached_image', attachedImage);
    }

    try {
      await apiClient.postsV1PostPatch(postId, body);
      navigate(singlePostUrl.replace(':postId', postId));
    } catch (err) {
      setError('An error occurred while updating the post');
    }
  };

  const handleImageChange = (e) => {
    if (e.target.files && e.target.files[0]) {
      setAttachedImage(e.target.files[0]);
    }
  };

  if (!postsLoaded) {
    return <div>Loading...</div>;
  }

  if (!post) {
    return <div>Post not found</div>;
  }

  return (
    <div className={styles.container}>
      <h2>Edit Post</h2>
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
          <label htmlFor="attachedImage">Image:</label>
          {currentImage && (
            <div className={styles.currentImage}>
              <img src={currentImage} alt="Current attachment" />
            </div>
          )}
          <input
            type="file"
            id="attachedImage"
            accept="image/*"
            onChange={handleImageChange}
          />
        </div>

        <button type="submit" className={styles.submitButton}>
          Save Changes
        </button>
      </form>
    </div>
  );
}
