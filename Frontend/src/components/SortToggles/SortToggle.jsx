import { React } from "react";
import { useDispatch, useSelector } from "react-redux";
import classNames from "classnames/bind";

import { sortAscImg, sortDescImg, sortInactiveImg } from "../Consts/Consts";

function getSortImg(isAscending) {
  if (isAscending === null) {
    return sortInactiveImg;
  }
  return isAscending ? sortAscImg : sortDescImg;
}

export default function SortToggle(props) {
  const {
    name,
    localSortFieldName,
    sortReducer,
    sortTogglesSelector,
    toggleStyle,
  } = props;

  const cx = classNames.bind(toggleStyle);

  const dispatch = useDispatch();
  const { sortFieldName, isAscending } = useSelector(sortTogglesSelector);
  const isSortedByCurrent = sortFieldName === localSortFieldName;


  const onClick = () => {
    const newIsAscending =
      sortFieldName !== localSortFieldName ? true : !isAscending;
    dispatch(
      sortReducer({
        sortFieldName: localSortFieldName,
        isAscending: newIsAscending,
      })
    );
  };

  return (
    <div
      className={cx(toggleStyle.sortToggle, {
        inactiveSortToggle: sortFieldName !== localSortFieldName,
      })}
    >
      <img
        src={getSortImg(isSortedByCurrent ? isAscending : null)}
        alt={sortFieldName}
        onClick={onClick}
      />
      <div className={toggleStyle.toggleName} onClick={onClick}>
        {name}
      </div>
    </div>
  );
}
