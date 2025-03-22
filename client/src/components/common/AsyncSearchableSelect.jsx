import { apiConfig } from "../../config/api.config";
import { useState, useEffect } from "react";
import SearchInput from "./SearchInput";
import SearchPopover from "./SearchPopover";

export default function AsyncSearchableSelect({ searchUrl, textFieldProps }) {
  const [searchValue, setSearchValue] = useState("");

  const handleSearch = (e) => {
    setSearchValue(e.target.value);
  };

  return (
    <>
      <SearchInput
        searchHandler={handleSearch}
        searchValue={searchValue}
        textFieldProps={textFieldProps}
      />
      {/* <SearchPopover options={options}/> */}
    </>
  );
}
