import React from "react";
import SearchInput from "./SearchInput";
import SearchPopover from "./SearchPopover";
import { useAsyncSearch } from "../../hooks/useAsyncSearch";
import { Box } from "@radix-ui/themes";
import { useState } from "react";
export default function AsyncSearchableSelect({
  urlPath,
  textFieldProps,
  searchHandler,
  searchValue,
  selectHandler,
  queryParams,
  searchLabel,
  selectDropdownOpen,
  handleOpenDropdown,
  isAdded,
}) {
  const { options } = useAsyncSearch({
    urlPath,
    searchValue,
    queryParams,
  });

  const [isSearching, setIsSearching] = useState(false);
  function handleSearchFocus() {
    handleOpenDropdown();
    setIsSearching(true);
  }
  const formattedOptions = options.map((option) => ({
    ...option,
    label: option.symbol, // Stock ticker symbol
    description: option.name || "No name available", // Fallback for missing name
    additionalInfo:
      option.sector && option.sector !== 0 ? option.sector : "Unknown sector", // Handle missing sector
  }));

  return (
    <Box position={"relative"}>
      {searchLabel}
      <SearchInput
        searchHandler={searchHandler}
        searchValue={searchValue}
        textFieldProps={textFieldProps}
        focusHandler={handleSearchFocus}
        clickHandler={handleOpenDropdown}
      />
      {selectDropdownOpen && isSearching && formattedOptions.length > 0 && (
        <SearchPopover
          options={formattedOptions}
          selectHandler={selectHandler}
          isAdded={isAdded}
        />
      )}
    </Box>
  );
}
