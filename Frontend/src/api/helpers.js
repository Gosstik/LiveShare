import comments from "../assets/comments.json";

const COMMENTS_LOAD_DURATION = 100;

function selectByPostId(arr, id) {
  return arr.filter((item) => item.postId.toString() === id.toString());
}

export function getComments(postId) {
  return new Promise((resolve) => {
    const targetComments = selectByPostId(comments, postId);
    setTimeout(() => resolve(targetComments), COMMENTS_LOAD_DURATION);
  });
}
