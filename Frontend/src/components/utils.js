export const LoadingState = {
  NOT_STARTED: "not_started",
  LOADING: "loading",
  SUCCESS: "success",
  FAILURE: "failure",
};

export const PostsSortOptions = {
  LIKES: "likes",
  CREATED_AT: "createdAt",
  COMMENTS: "comments",
}

export const getSortedArray = (values, lessCmp, isAscending = true) => {
  return values.slice().sort((lhs, rhs) => {
    if (lhs === null) {
      return 1;
    }
    if (rhs === null) {
      return -1;
    }
    let res = lessCmp(lhs, rhs) ? 1 : -1;
    return res * (isAscending ? 1 : -1);
  });
};

export const likesLessSort = (lhs, rhs) =>
  lhs.likes + lhs.isLiked < rhs.likes + lhs.isLiked;

export const fieldLessSort = (fieldName) => (lhs, rhs) =>
  lhs[fieldName] < rhs[fieldName];

export const generateNewId = (arrData, idFieldName) => {
  const maxId = arrData.reduce((prevId, cur) => {
    const curId = cur[idFieldName];
    return prevId < curId ? curId : prevId;
  }, 0);

  return maxId + 1;
};
