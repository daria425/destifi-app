import { useState } from "react";
import SearchInput from "./SearchInput";
import SearchPopover from "./SearchPopover";
import { useAsyncSearch } from "../../hooks/useAsyncSearch";

export default function AsyncSearchableSelect({
  urlPath,
  textFieldProps,
  searchHandler,
  searchValue,
  queryParams,
}) {
  console.log(searchValue);
  const { options, loading, error } = useAsyncSearch({
    urlPath,
    searchValue,
    queryParams,
  });
  console.log("Options from API", options);

  return (
    <>
      <SearchInput
        searchHandler={searchHandler}
        searchValue={searchValue}
        textFieldProps={textFieldProps}
      />
      {/* <SearchPopover options={options}/> */}
    </>
  );
}
