import React, { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';
import axios from 'axios';
import Cookies from 'js-cookie';
import styles from './PostShow.module.scss';

const PostShow = () => {
  const { postId } = useParams();
  const [post, setPost] = useState(null);
  const [error, setError] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchPost = async () => {
      try {
        const response = await axios.get(`http://localhost:8000/posts/v1/post/${postId}`, {
          headers: {
            'X-CSRFToken': Cookies.get('csrftoken'),
          },
          withCredentials: true,
        });
        setPost(response.data);
        setError(null);
      } catch (err) {
        setError(err.response?.data?.error || 'Failed to load post');
        setPost(null);
      } finally {
        setLoading(false);
      }
    };

    fetchPost();
  }, [postId]);

  if (loading) {
    return <div className={styles.loading}>Loading...</div>;
  }

  if (error) {
    return <div className={styles.error}>{error}</div>;
  }

  if (!post) {
    return <div className={styles.error}>Post not found</div>;
  }

  return (
    <div className={styles.container}>
      <article className={styles.post}>
        <header className={styles.header}>
          <h1>{post.title}</h1>
          <div className={styles.meta}>
            <span>By {post.author.displayed_name}</span>
            <span>Created: {new Date(post.created_at).toLocaleDateString()}</span>
            {post.edited_at !== post.created_at && (
              <span>Edited: {new Date(post.edited_at).toLocaleDateString()}</span>
            )}
          </div>
        </header>

        {post.attached_image_url && (
          <div className={styles.imageContainer}>
            <img 
              src={post.attached_image_url} 
              alt="Post attachment" 
              className={styles.image}
            />
          </div>
        )}

        <div className={styles.content}>
          {post.text_content}
        </div>

        <footer className={styles.footer}>
          <div className={styles.stats}>
            <span>{post.likes_count} likes</span>
            <span>{post.comments_count} comments</span>
          </div>
        </footer>
      </article>
    </div>
  );
};

export default PostShow;
