import { useLocation, Link } from "react-router-dom";

import style from "./NotFound.module.scss"

export function UrlNotFound() {
  const location = useLocation();

  const url = (
    <span style={{ fontWeight: 'bold'}}>{location.pathname}</span>
  )

  return <p>The requested URL {url} was not found.</p>
}

////////////////////////////////////////////////////////////////////////////////

export function PostNotFound(props) {
  const { postId } = props;

  const postIdElem = (
    <span style={{ fontWeight: 'bold'}}>{postId}</span>
  )

  return <p>The requested post {postIdElem} was not found.</p>
}

////////////////////////////////////////////////////////////////////////////////

export default function NotFound(props) {
  const { messageComponent } = props;

  const message = messageComponent();

  const home = (
    <Link to="/">
      <span style={{ fontWeight: 'bold'}}>home</span>
    </Link>
  )

  return (
    <div className={style.main}>
      <h1>404</h1>
      {message}
      <p>Return to {home} page.</p>
    </div>
  );
}
