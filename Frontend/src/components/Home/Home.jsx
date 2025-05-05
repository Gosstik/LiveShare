import { useState, useEffect } from 'react';
import { Link, CircularProgress } from '@mui/material';
import { useAuth } from "../AuthProvider/AuthProvider";
import Posts from '../Posts/Posts';
import ModalRequireAuth from '../ModalRequireAuth/ModalRequireAuth';
import styles from './Home.module.scss';

export default function Home() {
  const { isGuest, isAuthLoading, user } = useAuth();
  const [showAuthModal, setShowAuthModal] = useState(false);

  useEffect(() => {
    if (!isAuthLoading && isGuest) {
      setShowAuthModal(true);
    }
  }, [isGuest, isAuthLoading]);

  if (isAuthLoading) {
    return (
      <div className={styles.container}>
        <div className={styles.loading}>
          <Link
            component="button"
            variant="plain"
            startDecorator={<CircularProgress />}
            sx={{ p: 1 }}
          >
            Loading...
          </Link>
        </div>
      </div>
    );
  }

  return (
    <div className={styles.container}>
      {showAuthModal && (
        <ModalRequireAuth
          onClose={() => setShowAuthModal(false)}
          shallRedirect={true}
        />
      )}
      <Posts userId={user?.id} />
    </div>
  );
}
