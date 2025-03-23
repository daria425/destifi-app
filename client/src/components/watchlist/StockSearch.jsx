import AsyncSearchableSelect from "../common/AsyncSearchableSelect";
import InputLabel from "../common/InputLabel";
export default function StockSearch({
  stockSymbol,
  stockSearchHandler,
  stockSelectHandler,
  selectDropdownOpen,
  handleOpenDropdown,
  isAdded,
}) {
  return (
    <AsyncSearchableSelect
      urlPath={"/equities"}
      searchHandler={stockSearchHandler}
      selectHandler={stockSelectHandler}
      searchValue={stockSymbol}
      queryParams={"ticker"}
      isAdded={isAdded}
      textFieldProps={{
        placeholder: "Search stocks by ticker",
        name: "stock-search",
        id: "stock-search",
      }}
      handleOpenDropdown={handleOpenDropdown}
      selectDropdownOpen={selectDropdownOpen}
      searchLabel={<InputLabel labelText="Add Stocks" inputId="stock-search" />}
    />
  );
}
