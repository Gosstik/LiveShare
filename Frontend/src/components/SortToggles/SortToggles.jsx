import { React } from "react";

import SortToggle from "./SortToggle";

export default function SortToggles(props) {
  const { sortReducer, togglesData, sortTogglesSelector, togglesStyle } = props;

  return (
    <>
      {togglesData.map((toggle) => {
        return (
          <SortToggle
            key={toggle.name}
            name={toggle.name}
            localSortFieldName={toggle.fieldName}
            sortReducer={sortReducer}
            sortTogglesSelector={sortTogglesSelector}
            toggleStyle={togglesStyle}
          />
        );
      })}
    </>
  );
}
